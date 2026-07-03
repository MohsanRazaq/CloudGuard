# tests/test_check_bucket_acl.py
import boto3
from moto import mock_aws
from cloudguard.security_checks.check_bucket_acl import check_bucket_acl

@mock_aws
def test_acl_public_allusers_is_flagged():
    fake_s3 = boto3.client("s3", region_name="us-east-1")
    fake_bucket = "my-fake-public-acl-bucket"
    fake_s3.create_bucket(Bucket=fake_bucket)
    fake_s3.put_bucket_acl(
        Bucket=fake_bucket,
        AccessControlPolicy={
            "Owner": {"ID": "owner-id"},
            "Grants": [{
                "Grantee": {
                    "Type": "Group",
                    "URI": "http://acs.amazonaws.com/groups/global/AllUsers"
                },
                "Permission": "READ"
            }]
        }
    )
    result = check_bucket_acl(fake_bucket, fake_s3)
    assert result.passed is False

@mock_aws
def test_acl_private_passes():
    fake_s3 = boto3.client("s3", region_name="us-east-1")
    fake_bucket = "my-fake-private-acl-bucket"
    fake_s3.create_bucket(Bucket=fake_bucket)
    result = check_bucket_acl(fake_bucket, fake_s3)
    assert result.passed is True