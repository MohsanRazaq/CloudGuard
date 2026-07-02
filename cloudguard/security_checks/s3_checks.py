
from cloudguard.findings import Finding

def check_bucket_versioning(bucket_name:str,s3_client):
    

    try:
        response = s3_client.get_bucket_versioning(
            Bucket=bucket_name
        )

        status = response.get("Status", "Disabled")

        if status != "Enabled":
            return Finding(
                check="versioning",
                resource=bucket_name,
                passed=False,
                severity="Medium",
                issue="Bucket Versioning Disabled or Suspended",
                recommendation='Enable S3 Versioning using s3_client.put_bucket_versioning()'
            )

        return Finding(check='Versioning', resource=bucket_name, passed=True,severity='',issue='',recommendation='')

    except Exception as e:
        print(e)
        return None
    