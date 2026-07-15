from cloudguard.utils.logger import feeder
from cloudguard.constants import SEPARATOR
from cloudguard.findings import COLORS
from cloudguard.security_checks.s3 import S3_SECURITY_CHECKS

def list_buckets(s3_client):
    """Return a list of all S3 bucket names."""

    response = s3_client.list_buckets()

    return [bucket["Name"] for bucket in response["Buckets"]]


def scan_s3_buckets(session):
    """
    Scan every S3 bucket and execute all registered S3 security checks.

    Returns:
        tuple:
            (findings, bucket_count)
    """

    s3_client = session.client("s3")

    findings = []

    feeder("\n" + SEPARATOR)
    feeder(f"{COLORS['BOLD']}S3 SECURITY ASSESSMENT{COLORS['RESET']}")
    feeder(SEPARATOR)

    buckets = list_buckets(s3_client)

    bucket_count = len(buckets)

    for bucket in buckets:

        feeder(
            f"\n{COLORS['BLUE']}[RESOURCE]{COLORS['RESET']} {bucket}\n"
        )

        bucket_findings = [
            check(bucket, s3_client)
            for check in S3_SECURITY_CHECKS
        ]

        for finding in bucket_findings:
            feeder(finding)

        findings.extend(bucket_findings)

    return findings, {
    "bucket_count": bucket_count}