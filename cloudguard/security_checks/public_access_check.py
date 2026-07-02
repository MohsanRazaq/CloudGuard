from cloudguard.findings import Finding
from botocore.exceptions import ClientError
from cloudguard.constants import ALL_USERS_URI,AUTH_USERS_URI

def check_bucket_acl(bucket_name:str,s3_client):
    try:
        response = s3_client.get_bucket_acl(Bucket=bucket_name)
        grants = response['Grants']
        
        for grant in grants:
            grantee = grant['Grantee']
            if 'URI' in grantee:
                public_url = grantee['URI']
                
                # AWS Canonical URL for the Public Internet
                if public_url == ALL_USERS_URI:
                    return Finding(
                        check="Public Access List",
                        resource=bucket_name,
                        passed=False,
                        severity='Critical',
                        issue='Public Internet Access via ACL',
                        recommendation="Block Access"
                    )
                
                # AWS Canonical URL for Any Authenticated AWS User
                elif public_url == AUTH_USERS_URI:
                    return Finding(
                        check="Public Access List",
                        resource=bucket_name,
                        passed=False,
                        severity='High',
                        issue='Any AWS Account Access via ACL',
                        recommendation="Block Access"
                    )
            
        return Finding(
            check="ACL",
            resource=bucket_name,
            passed=True,
            severity="",
            issue="",
            recommendation=""
        )
    except :
        raise 
