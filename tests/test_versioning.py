from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.security_checks.check_bucket_versioning import (
    check_bucket_versioning
)

for bucket in list_buckets():
    finding = check_bucket_versioning(bucket)

    if finding:
        print(finding)
    else:
        print(f"{bucket}: Versioning Enabled")