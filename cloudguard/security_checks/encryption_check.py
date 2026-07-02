
from cloudguard.findings import Finding

from botocore.exceptions import ClientError

def check_bucket_encryption(bucket_name:str,s3_client)->object:
    try:
        s3_client.get_bucket_encryption(Bucket=bucket_name)

        return Finding(
            check="Encryption",
            resource=bucket_name,
            passed=True,
            severity="",
            issue="",
            recommendation=""
        )

    except ClientError as e:

        error_code = e.response["Error"]["Code"]

        if error_code == "ServerSideEncryptionConfigurationNotFoundError":

            return Finding(
                check="Encryption",
                resource=bucket_name,
                passed=False,
                severity="High",
                issue="Bucket Encryption Disabled",
                recommendation="Enable Encryption"
            )

        elif error_code == "NoSuchBucket":
            return None

        else:
            raise