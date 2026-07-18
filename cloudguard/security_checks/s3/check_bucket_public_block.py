from cloudguard.findings import Finding
from botocore.exceptions import ClientError

def check_public_access_block(bucket_name: str, s3_client):
    try:
        response = s3_client.get_public_access_block(Bucket=bucket_name)
        PAB_config = response['PublicAccessBlockConfiguration']
        
        block_acls = PAB_config.get('BlockPublicAcls', False)
        ignore_acls = PAB_config.get('IgnorePublicAcls', False)
        block_policy = PAB_config.get('BlockPublicPolicy', False)
        restrict_buckets = PAB_config.get('RestrictPublicBuckets', False)
        
        if not (block_acls and ignore_acls and block_policy and restrict_buckets):
            return Finding(
                check='Public Access Block',
                resource=bucket_name,
                passed=False,
                severity='HIGH',
                issue='Public Access block is incomplete or disabled',
                recommendation='Enable All 4 public Access Block Settings'     
            )
        
        return Finding(
            check='Public Access Block',
            resource=bucket_name,
            passed=True,
            severity='',
            issue='Public access block settings are secure and complete.', # Cleaned up description text
            recommendation='No action required'     
        )
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            return Finding(
                check='Public Access Block',
                resource=bucket_name,
                passed=False,
                severity='HIGH',
                issue='Public Access block configuration is entirely missing.',
                recommendation='Deploy standard AWS Public Access Block controls.'
            )
        raise e
