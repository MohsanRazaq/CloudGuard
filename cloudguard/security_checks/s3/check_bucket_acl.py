from cloudguard.findings import Finding

def check_bucket_acl(bucket_name, s3_client):
    try:
        response = s3_client.get_bucket_acl(Bucket=bucket_name)
        grants = response.get('Grants', [])

        for grant in grants:
            if not isinstance(grant, dict):
                continue
            grantee = grant.get('Grantee', {})

            if grantee.get('Type', '') == 'Group':
                group_uri = grantee.get('URI', '')
                if "AllUsers" in group_uri:
                    return Finding(
                        check='Bucket ACL',
                        resource=bucket_name,
                        passed=False,
                        severity='HIGH',
                        issue='Insecure ACL exposed to Public Anonymous Access (AllUsers)',
                        recommendation='Disable ACLs entirely by enabling S3 Object Ownership (Bucket owner enforced)'
                    )
                elif "AuthenticatedUsers" in group_uri:
                    return Finding(
                        check='Bucket ACL',
                        resource=bucket_name,
                        passed=False,
                        severity='HIGH',
                        issue='Insecure ACL exposed to Any Authenticated AWS User Access',
                        recommendation='Disable ACLs entirely by enabling S3 Object Ownership (Bucket owner enforced)'
                    )

        return Finding(
            check='Bucket ACL',
            resource=bucket_name,
            passed=True,
            severity=None,
            issue='ACL secure. only owner has access',
            recommendation='No Action required'
        )

    except Exception as e:
        return Finding(
            check='ACL Review',
            resource=bucket_name,
            passed=False,
            severity='MEDIUM',
            issue=f'Failed to evaluate ACL: {str(e)}',
            recommendation='Verify s3:GetBucketAcl permissions.'
        )