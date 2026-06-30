from cloudguard.aws.session import create_session
from cloudguard.findings import Finding
from botocore.exceptions import ClientError

session = create_session()
s3 = session.client('s3')

def check_bucket_acl(bucket_name):
    try:
        response = s3.get_bucket_acl(Bucket=bucket_name)
        grant_list = response['Grants']
        
        for grant in grant_list:
            grantee = grant['Grantee']
            if 'URI' in grantee:
                public_url = grantee['URI']
                
                # AWS Canonical URL for the Public Internet
                if public_url == 'http://amazonaws.com':
                    return Finding(
                        check="Public Access List",
                        resource=bucket_name,
                        passed=False,
                        severity='Critical',
                        issue='Public Internet Access via ACL',
                        recommendation="Block Access"
                    )
                
                # AWS Canonical URL for Any Authenticated AWS User
                elif public_url == 'http://amazonaws.com':
                    return Finding(
                        check="Public Access List",
                        resource=bucket_name,
                        passed=False,
                        severity='High',
                        issue='Any AWS Account Access via ACL',
                        recommendation="Block Access"
                    )
                    
        print(f'Bucket:[{bucket_name}] is SAFE in ACL')
        return None
        
    except Exception as e:
        raise e
