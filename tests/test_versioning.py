# tests/test_versioning.py
import os
import boto3
from moto import mock_aws
from cloudguard.security_checks.check_bucket_versioning import check_bucket_versioning

@mock_aws
def test_versioning_disabled_is_flagged():
    fake_s3 = boto3.client("s3", region_name="us-east-1")
    fake_bucket = "my-fake-unversioned-bucket"
    fake_s3.create_bucket(Bucket=fake_bucket)

    result = check_bucket_versioning(fake_bucket, fake_s3)

    assert "[PASS]" not in str(result)

@mock_aws
def test_versioning_enabled_passes():
    fake_s3 = boto3.client("s3", region_name="us-east-1")
    fake_bucket = "my-fake-versioned-bucket"
    fake_s3.create_bucket(Bucket=fake_bucket)
    fake_s3.put_bucket_versioning(
        Bucket=fake_bucket,
        VersioningConfiguration={"Status": "Enabled"}
    )

    result = check_bucket_versioning(fake_bucket, fake_s3)

    assert "[PASS]" in str(result)