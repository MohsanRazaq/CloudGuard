from cloudguard.security_checks.s3.check_bucket_versioning import (
    check_bucket_versioning,
)
from cloudguard.security_checks.s3.check_bucket_encryption import (
    check_bucket_encryption,
)
from cloudguard.security_checks.s3.check_bucket_public_block import (
    check_public_access_block,
)
from cloudguard.security_checks.s3.check_bucket_logging import (
    check_bucket_logging,
)
from cloudguard.security_checks.s3.check_bucket_acl import (
    check_bucket_acl,
)
from cloudguard.security_checks.s3.check_bucket_policy import (
    check_bucket_policy,
)


S3_SECURITY_CHECKS = [
    check_bucket_versioning,
    check_bucket_encryption,
    check_public_access_block,
    check_bucket_logging,
    check_bucket_acl,
    check_bucket_policy,
]