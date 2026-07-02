from cloudguard.findings import Finding

def check_bucket_acl(bucket_name,s3_client):
    response=s3_client.get_bucket_acl(Bucket=bucket_name)
    try:
        is_public=False
        Exposure_type=''
        response = s3_client.get_bucket_acl(Bucket=bucket_name)
        grants = response.get('Grants',[])
        
        for grant in grants:
            if not isinstance(grant,dict):
                continue
            grantee=grant.get('Grantee',{})
            
            if grantee.get('Type','')=='Group':
                group_uri=grantee.get('URI','')
                if "Allusers" in group_uri:
                    is_public=True
                    Exposure_type="Public Anonymous Access (AllUsers)"
                    break
                elif "Authenticatedusers" in group_uri:
                    is_public=True
                    Exposure_type='Any Authenticated AWS User Access'
                    break
            if is_public:
                return Finding(
                    check='Bucket ACL',
                    resource=bucket_name,
                    passed=False,
                    severity='HIGH',
                    issue=f'Insecure ACL exposed to {Exposure_type}',
                    recommendation='Disable ACLs entirely by enabling S3 Object Ownership (Bucket owner enforced)'   
                )
                
        return Finding(
                check='Bucket ACL',
                resource=bucket_name,
                passed=True,
                severity=None,
                issue=f'ACL secure. only owner has access',
                recommendation='No Action required'   
            )
    
    except Exception as e:
        return Finding(
                    check='ACL Review',
                    resource=bucket_name,
                    passed=False,
                    severity='MEDIUM',
                    issue=f'Failed to evaluate ACl:  {str(e)}',
                    recommendation='Verify s3:GetBucketAcl permissions.'   
                )