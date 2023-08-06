from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
import sys
from awsglue.job import Job
import boto3
from string import Template
import re


class InvalidFileType(Exception):
    pass


def time_column_converter(dataframe: DataFrame, column: str, format: str):
    non_nulls = dataframe.agg(
        F.sum(F.when(F.col(column).isNotNull(), 1).otherwise(0))
    ).first()[0]
    dataframe = dataframe.withColumn(column, F.to_timestamp(column, format))
    converted = dataframe.agg(
        F.sum(F.when(F.col(column).isNotNull(), 1).otherwise(0))
    ).first()[0]
    if non_nulls != converted:
        print(
            f"Warning! {column} had {non_nulls} timestamps, "
            + f"and now has {converted} non_null timestamps!"
        )
    print("converted column " + column)
    return dataframe


def extraction_timestamp_formatter():
    format = "%Y%m%d%H%M%SZ"
    # mapping converts python dates to simple dates for java
    mapping = {
        "Y": "yyyy",
        "y": "yy",
        "m": "MM",
        "d": "dd",
        "H": "HH",
        "M": "mm",
        "SZ": "ss'Z'",
    }
    return_format = Template(format.replace("%", "$")).substitute(**mapping)
    return return_format


def date_converter(dataframe: DataFrame):
    dataframe = time_column_converter(
        dataframe=dataframe,
        column="extraction_timestamp",
        format=extraction_timestamp_formatter(),
    )
    return dataframe


def key_splitter(key: str):
    """
    Takes standard AWS Key, as output by boto3.client.list_objects_v2(),
    and splits the key into the databasename, filename + extension, and the file path.

    Arguments:
    key: str
        A key of the format path/to/file/filename.ext
    """
    key_list = key.split("/")
    filename = key_list.pop()
    database_key = [s for s in key_list if "database_name=" in s]
    table_key = [s for s in key_list if "table_name=" in s]
    extraction_key = [s for s in key_list if "extraction_timestamp=" in s]
    filetype = filename.split(".")[-1]
    # drop extraction timestamp before conjoining
    key_list.pop()
    filepath = "/".join(key_list) + "/"
    database_name = database_key[0].split("=")[-1]
    extraction_timestamp = extraction_key[0].split("=")[-1]
    table_name = table_key[0].split("=")[-1]
    if filetype not in ["csv", "json", "jsonl"]:
        raise InvalidFileType(
            f"The filetype, {filetype} is not supported by this operation"
        )
    return filepath, database_name, table_name, filetype, filename, extraction_timestamp


def replace_space_in_string(name: str) -> str:
    """
    If a string contains space inbetween, then replace by underscore
    """
    replaced_name = name.strip().replace(" ", "_")
    return replaced_name


def dynamic_frame_to_glue_catalog(
    path: str,
    table_name: str,
    database_name: str,
    dynamic_frame: DynamicFrame,
    glue_context: GlueContext,
):
    """
    Adds a given Glue DynamicFrame to the Glue Catalog,
    by writing it out to the supplied path

    Arguments:
    path: str
        A S3 path of the format s3://path/to/file/
    table_name: str
        The desired name of the table
    database name: str
        The name of the database which the table is to appear in.
    dynamic_frame: DynamicFrame
        A Glue DynamicFrame, including partitioning info, to be written out.
    glue_context:
        An AWS GlueContext
    """
    print("Attempting to register to Glue Catalogue")
    # recommended to use write_dynamic_frame.from_options() rather than getSink
    try:
        sink = glue_context.getSink(
            path=path,
            connection_type="s3",
            updateBehavior="UPDATE_IN_DATABASE",
            partitionKeys=["extraction_timestamp"],
            compression="snappy",
            enableUpdateCatalog=True,
            transformation_ctx="sink",
        )
        sink.setFormat("glueparquet", useGlueParquetWriter=True)
        sink.setCatalogInfo(catalogDatabase=database_name, catalogTableName=table_name)

        sink.writeFrame(dynamic_frame)
        print("Write out of file succeeded!")
    except Exception as e:
        print(f"Could not convert {path} to glue table, due to an error!")
        print(e)


def add_extraction_timestamp(df):
    df["extraction_timestamp"] = extraction_timestamp
    return df


def clean_dynamic_frame_fields(df):
    """
    Collects the field names from a Glue DynamicFrame, converts to lowercase
    and replaces any special characters (not [a-z0-9_]) with underscore; checks
    once for duplicate field names and adds a suffix to any found.

    For example, "AN.T" and "an@T" both become "an_t" then the second occurence
    is renamed "an_t_2". Hopefully this is sufficent to ensure no duplicates!

    Input:
    df: Glue DynamicFrame

    Output:
    df: Glue DynamicFrame
        With field names comprising only [a-z0-9_] characters.
    """
    # get list of fields from dynamic frame
    fields = list(df.schema().field_map.keys())
    # create backticked version to enable replacement of awkward special chars: .{}[]()
    fields_backticked = ["`" + field + "`" for field in fields]
    # create new names allowing only [a-z0-9_], replace special chars with "_"
    fields_clean = [re.sub("[^a-z0-9_]", "_", f.lower()) for f in fields]
    # strip underscores from start of field name
    fields_clean = [f.lstrip("_") for f in fields_clean]
    # check fields_clean for duplicate names; if any add suffix
    if len(set(fields_clean)) != len(fields_clean):
        counts = {}
        for i, field in enumerate(fields_clean):
            if field in counts:
                counts[field] += 1
                # add suffix if duplicate found
                fields_clean[i] = f"{field}_{counts[field]}"
            else:
                counts[field] = 1
    # rename every field if at least one field needs cleaning
    if fields != fields_clean:
        for old_name, clean_name in zip(fields_backticked, fields_clean):
            df = df.rename_field(old_name, clean_name)

    return df


def new_files_to_dynamic_frame(
    path: str,
    filetype: str,
    filename: str,
    source_bucket: str,
    destination_bucket: str,
    table_name: str,
    allow_data_conversion: str,
    extraction_timestamp: str,
    spark: SparkSession,
    glue_context: GlueContext,
):
    """
    Reads in a files at a filepath, and transforms them into
    a partitioned DynamicFrame using Spark and Glue.
    (Usually there is only one file under the extraction_timestamp subfolder)

    Arguments:
    path: str
        A S3 path of the format path/to/file/, not including any "s3://" prefixes
    filetype: str
        A filetype, currently only of the format "csv" or "json/jsonl"
    source_bucket: str
        The name of AWS bucket in which the files are contained.
    table_name: str
        The name of the table to be constructed.
    extraction_timestamp: str
        The timestamp of the extract
    spark: SparkSession
        A SparkSession to be used to construct a Dataframe,
        containing the partitioned data.
    glue_context:
        An AWS GlueContext

    Output:
    dynamic_frame: Glue Dynamic Frame
        A dynamic frame of the files read; can be null, with zero rows.
    """
    try:
        file_location = (
            "s3://" + source_bucket + "/" + path
            + "extraction_timestamp=" + extraction_timestamp
        )

        print("file location: ", file_location)
        if filetype == "csv":
            print("using csv")
            dynamic_frame = glue_context.create_dynamic_frame.from_options(
                format_options={"multiline": False, "withHeader": True},
                connection_type="s3",
                format="csv",
                connection_options={
                    "paths": [file_location],
                    "recurse": False,
                    "optimizePerformance": True
                },
                transformation_ctx="df_" + table_name + "_" + extraction_timestamp,
            )
        else:
            print("using json")
            dynamic_frame = glue_context.create_dynamic_frame.from_options(
                format_options={"multiline": True},
                connection_type="s3",
                format="json",
                connection_options={
                    "paths": [file_location],
                    "recurse": False,
                },
                transformation_ctx="df_" + table_name + "_" + extraction_timestamp,
            )

        # bookmarking is noted at the point of create_dynamic_frame above
        print(f"Successfully read files at {file_location} to Glue Dynamic Frame")
        # print("Dynamic Frame row count: ", dynamic_frame.count())

        # logic to apply further processing/printouts iff DynF rows not 0
        if dynamic_frame.count() > 0:
            # print("First 2 rows of Dynamic Frame:")
            # dynamic_frame.show(2)

            # add extraction_timestamp column, no bookmarking required
            dynamic_frame = dynamic_frame.map(
                f=add_extraction_timestamp,
            )
            # clean dynamic frame field names
            print("fields: ", list(dynamic_frame.schema().field_map.keys()))
            dynamic_frame = clean_dynamic_frame_fields(dynamic_frame)
            # check new fields
            print("clean fields: ", list(dynamic_frame.schema().field_map.keys()))

            # df = dynamic_frame.toDF()
            # print("First 2 rows of cleaned Dynamic Frame as Spark DF:")
            # df.show(2)

        return dynamic_frame

    except Exception as e:
        print(f"Could not convert {file_location} to dynamic_frame, due to an error!")
        print(e)


def setup_glue(inputs: dict):
    """
    Setup glue environment and create a spark session

    Returns a spark session, glue context and job
    """
    sc = SparkContext()
    glueContext = GlueContext(sc)
    job = Job(glueContext)
    job.init(inputs["JOB_NAME"], inputs)
    glueContext._jsc.hadoopConfiguration().set(
        "fs.s3.enableServerSideEncryption", "true"
    )
    glueContext._jsc.hadoopConfiguration().set(
        "fs.s3.canned.acl", "BucketOwnerFullControl"
    )
    spark = glueContext.spark_session

    return spark, glueContext, job


def job_inputs():
    return getResolvedOptions(
        sys.argv,
        [
            "JOB_NAME",
            "source_bucket",
            "destination_bucket",
            "stack_name",
            "multiple_db_in_bucket",
            "allow_data_conversion",
        ],
    )


def list_of_data_objects_to_process(bucket):
    """
    List all objects under the data/ path for a given bucket.
    Returns the full response from the list_object_v2 call.
    """
    client = boto3.client("s3")
    print("Listing Objects")
    paginator = client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(
        Bucket=bucket,
        Prefix="data/",
    )
    response = []
    try:
        for page in page_iterator:
            response += page["Contents"]
    except KeyError as e:
        print(f"No {e} key found in bucket contents – either the bucket")
        print(" is empty or the data folder isn't available")

    return response


def paths_to_tables(list_of_objects):
    """
    Takes the response from list of objects and
    loops over all keys and extracts the path to the table.
    A dictionary is created to store the file extension and table name
    per path to table.

    A dictionary is returned with a key for each path found.
    """
    paths = {}
    for item in list_of_objects:
        key = item["Key"]
        try:
            (
                input_path,
                database_name,
                table_name,
                filetype,
                filename,
                extraction_timestamp,
            ) = key_splitter(key=key)
            if input_path not in paths:
                paths[input_path] = {}
            paths[input_path]["filetype"] = filetype
            paths[input_path]["filename"] = filename
            paths[input_path]["table_name"] = table_name
            paths[input_path]["database_name"] = database_name
            if "extraction_timestamps" not in paths[input_path].keys():
                paths[input_path]["extraction_timestamps"] = []
            if extraction_timestamp not in paths[input_path]["extraction_timestamps"]:
                paths[input_path]["extraction_timestamps"].append(extraction_timestamp)
            else:
                continue
        except Exception as e:
            print(e)
            print(f"This is due to the file at {item['Key']}")
    return paths


def does_database_exist(client, database_name):
    """Determine if this database exists in the Data Catalog
    The Glue client will raise an exception if it does not exist.
    """
    try:
        client.get_database(Name=database_name)
        return True
    except client.exceptions.EntityNotFoundException:
        return False


def print_inputs(inputs: dict):
    print(
        f"Job name: {args['JOB_NAME']},",
        f"source_bucket: {args['source_bucket']},",
        f"destination_bucket: {args['destination_bucket']},",
        f"stack_name: {args['stack_name']},",
        f"multiple_db_in_bucket: {args['multiple_db_in_bucket']},",
        f"allow_data_conversion: {args['allow_data_conversion']},",
    )


if __name__ == "__main__":
    args = job_inputs()
    print("args: ", args)
    # set up spark, glueContext and initialise job
    spark, glueContext, job = setup_glue(inputs=args)

    stack_name = args["stack_name"]
    response = list_of_data_objects_to_process(bucket=args["source_bucket"])
    print("Objects in source bucket: ", len(response))

    if len(response) > 0:

        paths = paths_to_tables(list_of_objects=response)
        print("paths: ", paths)

        for path in paths:
            for extraction_timestamp in paths[path]["extraction_timestamps"]:

                desired_path = "s3://" + args["destination_bucket"] + "/" + path

                dynamic_frame = new_files_to_dynamic_frame(
                    path=path,
                    filetype=paths[path]["filetype"],
                    filename=paths[path]["filename"],
                    source_bucket=args["source_bucket"],
                    destination_bucket=args["destination_bucket"],
                    table_name=paths[path]["table_name"],
                    allow_data_conversion=args["allow_data_conversion"],
                    extraction_timestamp=extraction_timestamp,
                    glue_context=glueContext,
                    spark=spark,
                )

                if dynamic_frame.count() == 0:
                    print("No files to process; continuing to next iteration.\n")
                    continue
                else:
                    # if multiple_db_in_bucket then use
                    # databasename from 'database_name=xxx' else
                    # bucketname as databasename
                    # CREATE GLUE CATALOG USING BOTO
                    if args["multiple_db_in_bucket"] == "True":
                        db_name = (
                            args["stack_name"] + "_" + paths[path]["database_name"]
                        )
                    else:
                        db_name = args["stack_name"]

                    db_name = db_name.replace("-", "_")
                    print("database: ", db_name)

                    client = boto3.client("glue")

                    if (
                        not does_database_exist(client, db_name)
                        and args["multiple_db_in_bucket"] == "True"
                    ):
                        print("create database")
                        response = client.create_database(
                            DatabaseInput={
                                "Name": db_name,
                                "Description": "A Glue Database for tables from "
                                + args["stack_name"],
                            }
                        )
                    dynamic_frame_to_glue_catalog(
                        path=desired_path,
                        table_name=paths[path]["table_name"],
                        database_name=db_name,
                        dynamic_frame=dynamic_frame,
                        glue_context=glueContext,
                    )

    job.commit()
