
# to get buckets present on S3
def list_buckets(s3_client):
    """Fetches all bucket names using the provided S3 client."""
    response = s3_client.list_buckets()

    return [bucket["Name"] for bucket in response["Buckets"]]
