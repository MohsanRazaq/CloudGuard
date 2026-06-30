from cloudguard.aws.session import create_session
from cloudguard.findings import Finding
from botocore.exceptions import ClientError

session = create_session()
s3 = session.client('s3')


def check_public_access_block(bucket_name):
    try:
        response=s3.get_public_access_block(Bucket=bucket_name)
        PAB_config=response['PublicAccessBlockConfiguration']
        
        block_acls=PAB_config.get('BlockPublicAcls',False)
        ignore_acls=PAB_config.get('IgnorePublicAcls',False)
        block_policy=PAB_config.get('BlockPublicpolicy',False)
        restrict_buckets=PAB_config.get('RestrictPublicBuckets',False)
        
        if not(block_acls and ignore_acls and block_policy and restrict_buckets):
            return Finding(
                check='Public Access Block',
                resource=bucket_name,
                passed=False,
                severity='High',
                issue='Public Access block is incomplete or disabled',
                recommendation='Enable All 4 public Access Block Setting'     
            )
        
        return Finding(
                check='Public Access Block',
                resource=bucket_name,
                passed=True,
                severity='',
                issue='',
                recommendation='public Access Block Setting is ALready configured'     
            )
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code=='NoSuchPublicAccessBlockConfiguration':
            return  Finding(
                check='Public Access Block',
                resource=bucket_name,
                passed=False,
                severity='High',
                issue='Public Access block Configuration Does not exist',
                recommendation="Create and enable all 4 Public Access Block options")