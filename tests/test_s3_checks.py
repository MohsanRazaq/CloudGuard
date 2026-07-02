# tests/test_s3_checks.py
import os,logging
import pytest
import boto3
from moto import mock_aws
from cloudguard.security_checks.check_bucket_encryption import check_bucket_encryption

@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    """Sets dummy environment variables so Boto3 never hits real AWS."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@mock_aws
def test_encryption_check_with_fake_aws():
    # 1. Initialize a fake S3 client inside the Moto sandbox
    boto3.set_stream_logger(name="botocore.endpoint", level=logging.DEBUG)
    fake_s3 = boto3.client("s3", region_name="us-east-1")
    
    # 2. Setup a completely unencrypted fake bucket in memory
    fake_bucket = "my-fake-vulnerable-bucket"
    fake_s3.create_bucket(Bucket=fake_bucket)
    
    # 3. Test your real check function by injecting the fake client!
    result = check_bucket_encryption(fake_bucket, fake_s3)
    
    # 4. Assert that your check correctly spots the missing encryption
    assert "Bucket Encryption Disabled" in str(result)

