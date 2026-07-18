import json
from cloudguard.findings import Finding
from botocore.exceptions import ClientError

def check_bucket_policy(bucket_name: str, s3_client):
    try:
        response = s3_client.get_bucket_policy(Bucket=bucket_name)
        policy = json.loads(response['Policy'])
        
        for statement in policy.get('Statement', []):
            principal = statement.get('Principal', {})
            effect = statement.get('Effect', '')
            
            is_public_principal = (
                principal == "*" or 
                (isinstance(principal, dict) and principal.get('AWS') == "*") or
                (isinstance(principal, dict) and "*" in principal.get('AWS', []))
            )
            
            if is_public_principal and effect == "Allow":
                condition = statement.get('Condition', {})
                
                if not condition:
                    return Finding(
                        check="Bucket Policy",
                        resource=bucket_name,
                        passed=False,
                        severity="CRITICAL",
                        issue="Bucket policy allows unauthenticated public access",
                        recommendation='Restrict Principal to specific IAM identities or implement strict Conditions.'
                    )
        
        return Finding(
            check="Bucket Policy",
            resource=bucket_name,
            passed=True,
            severity="",
            issue="Bucket policy is safe or contains secure restrictions.",
            recommendation='No Action Needed'
        )
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            return Finding(
                check="Bucket Policy",
                resource=bucket_name,
                passed=True,
                severity="",
                issue="No explicit bucket policy attached (Safe by default if public access blocks are active).",
                recommendation='No Action Needed'
            )
        raise e
