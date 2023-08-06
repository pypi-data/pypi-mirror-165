from typing import Optional, Sequence
from data_engineering_pulumi_components.aws.buckets.bucket import (
    Bucket,
    BucketPutPermissionsArgs,
)
from data_engineering_pulumi_components.utils import Tagger
from pulumi import ResourceOptions
from pulumi_aws import Provider


class CuratedBucket(Bucket):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        put_permissions: Optional[Sequence[BucketPutPermissionsArgs]] = None,
        provider: Provider = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            name=name + "-curated",
            tagger=tagger,
            t="data-engineering-pulumi-components:aws:CuratedBucket",
            put_permissions=put_permissions,
            cors_rules=None,
            provider=provider,
            opts=opts,
        )
