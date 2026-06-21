from cloudguard.aws.session import create_session
from cloudguard.findings import Finding


def check_bucket_versioning(bucket_name):
    s3 = create_session()

    try:
        response = s3.get_bucket_versioning(
            Bucket=bucket_name
        )

        status = response.get("Status", "Disabled")

        if status != "Enabled":
            return Finding(
                resource=bucket_name,
                severity="Medium",
                issue="Bucket Versioning Disabled",
                recommendation="Enable S3 Versioning"
            )

        return None

    except Exception as e:
        print(e)
        return None