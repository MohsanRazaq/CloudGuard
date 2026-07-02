from cloudguard.findings import Finding

def check_bucket_logging(bucket_name:str,s3_client):
    try:
        response = s3_client.get_bucket_logging(Bucket=bucket_name)
    except Exception as e:        
        return Finding(
                check='Bucket Logging',
                resource=bucket_name,
                passed=False,
                severity='MEDIUM',
                issue=f'Failed to fetch configuration: {str(e)}',
                recommendation='Verify IAM permission for s3:GetBuckLogging'
                
            )
    
    if not response or "LoggingEnabled" not in response:
        return Finding(
                check='Bucket Logging',
                resource=bucket_name,
                passed=False,
                severity='HIGH',
                issue=f'Server access logging is not enabled on this bucket',
                recommendation='Enable S3 Server Access Logging and configure a dedicated log bucket.'
                
            )
        
    return Finding(
                check='Bucket Logging',
                resource=bucket_name,
                passed=True,
                severity='None',
                issue=f'Bucket logging is configured correctly',
                recommendation='No action required'
                
            )