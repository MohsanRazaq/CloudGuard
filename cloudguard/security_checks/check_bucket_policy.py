import json
from cloudguard.findings import Finding
from botocore.exceptions import ClientError


def check_bucket_policy(bucket_name:str,s3_client):
    try:
        response=s3_client.get_bucket_policy(Bucket=bucket_name)
        policy=json.loads(response['Policy'])
        for statement in policy['Statement']:
            principal=statement['Principal']
            effect=statement['Effect']
            if  principal=="*" and effect=="Allow":

                return Finding(
                check="Bucket Policy",
                resource=bucket_name,
                passed=False,
                severity="CRITICAL",
                issue="Bucket policy allows public access",
                recommendation='Restrict Principal to specific IAM identities'
            )
        return Finding(
                check="Bucket Policy",
                resource=bucket_name,
                passed=True,
                severity="",
                issue="",
                recommendation='No Action  Needed'
            )
    except ClientError  as e:
        if e.response['Error']['Code']=='NoSuchBucketPolicy':
            
            return Finding(
                    check="Bucket Policy",
                    resource=bucket_name,
                    passed=True,
                    severity="",
                    issue="",
                    recommendation=''
                )
        raise