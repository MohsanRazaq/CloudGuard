# tests/test_check_bucket_policy.py
import json
import boto3
from moto import mock_aws
from cloudguard.security_checks.s3.check_bucket_policy import check_bucket_policy

@mock_aws
def test_policy_public_is_flagged():
    fake_s3 = boto3.client("s3", region_name="us-east-1")
    fake_bucket = "my-fake-public-policy-bucket"
    fake_s3.create_bucket(Bucket=fake_bucket)
    public_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{fake_bucket}/*"
        }]
    }
    fake_s3.put_bucket_policy(Bucket=fake_bucket, Policy=json.dumps(public_policy))
    result = check_bucket_policy(fake_bucket, fake_s3)
    assert result.passed is False

@mock_aws
def test_policy_missing_passes():
    fake_s3 = boto3.client("s3", region_name="us-east-1")
    fake_bucket = "my-fake-no-policy-bucket"
    fake_s3.create_bucket(Bucket=fake_bucket)
    result = check_bucket_policy(fake_bucket, fake_s3)
    assert result.passed is True