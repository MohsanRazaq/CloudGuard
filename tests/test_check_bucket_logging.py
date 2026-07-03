# tests/test_check_bucket_logging.py
import boto3
from moto import mock_aws
from cloudguard.security_checks.check_bucket_logging import check_bucket_logging

@mock_aws
def test_logging_disabled_is_flagged():
    fake_s3 = boto3.client("s3", region_name="us-east-1")
    fake_bucket = "my-fake-unlogged-bucket"
    fake_s3.create_bucket(Bucket=fake_bucket)
    result = check_bucket_logging(fake_bucket, fake_s3)
    assert result.passed is False

@mock_aws
def test_logging_enabled_passes():
    fake_s3 = boto3.client("s3", region_name="us-east-1")
    fake_bucket = "my-fake-logged-bucket"
    target_bucket = "my-fake-target-log-bucket"
    fake_s3.create_bucket(Bucket=fake_bucket)
    fake_s3.create_bucket(Bucket=target_bucket)
    fake_s3.put_bucket_logging(
        Bucket=fake_bucket,
        BucketLoggingStatus={
            "LoggingEnabled": {
                "TargetBucket": target_bucket,
                "TargetPrefix": "logs/"
            }
        }
    )
    result = check_bucket_logging(fake_bucket, fake_s3)
    assert result.passed is True