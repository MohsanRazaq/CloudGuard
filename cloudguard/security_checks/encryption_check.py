
from cloudguard.aws.session import create_session
from cloudguard.findings import Finding

from botocore.exceptions import ClientError
session=create_session()
s3 =session.client('s3') 

def check_bucket_encryption(bucket_name):
    try:
        response = s3.get_bucket_encryption(Bucket=bucket_name)
        return None # If it succeeds  it has explicit config.
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        
        # case1: Bucket exists but has no encryption rules
        if error_code == "ServerSideEncryptionConfigurationNotFoundError":
            return Finding(
                check="Encryption",
                resource=bucket_name,
                passed=False,
                severity="High",
                issue="Bucket Encryption Disabled",
                recommendation="Enable Encryption"
            )
            
        # case2: Bucket was completely deleted
        elif error_code == "NoSuchBucket":
            print(f"Warning: Bucket {bucket_name} does not exist anymore.")
            return None
            
        # case3: Any other error
        else:
            raise e
