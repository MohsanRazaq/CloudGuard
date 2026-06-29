
from cloudguard.aws.session import create_session
from cloudguard.findings import Finding
from botocore.exceptions import ClientError
session = create_session()
s3 = session.client("s3")

def list_buckets():
    response = s3.list_buckets()
    return [bucket["Name"] for bucket in response["Buckets"]]


def check_bucket_encryption(bucket_name):
    try:
        response = s3.get_bucket_encryption(Bucket=bucket_name)
        return None
    except ClientError as e:
        if e.response["Error"]["Code"] == \
            "ServerSideEncryptionConfigurationNotFoundError":
            return Finding(
            resource=bucket_name,
            severity="High",
            issue="Bucket Encryption Disabled",
            recommendation="Enable Encryption")
        raise
