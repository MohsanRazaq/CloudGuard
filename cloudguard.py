from cloudguard.utils.config_loader import load_config
from cloudguard.utils.logger import write_log
from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.security_checks.s3_checks import (
    check_bucket_versioning
)
from cloudguard.aws.session import create_session
from cloudguard.constants import SEPARATOR
from cloudguard.security_checks.encryption_check import check_bucket_encryption
from cloudguard.security_checks.public_access_check import check_bucket_acl
from cloudguard.security_checks.public_block_check import check_public_access_block
from cloudguard.security_checks.check_bucket_logging import Get_Bucket_Logging


################################################################################
S3_SECURITY_CHECKS = [
    check_bucket_versioning,
    check_bucket_encryption,
    check_bucket_acl,
    check_public_access_block,
    Get_Bucket_Logging
]


def feeder(message:object) -> None:
    text = str(message)
    print(text)
    write_log(text)
    
def setup_logger()->None:
    config = load_config()
    running_tasks = []
    skipped_tasks = []


    for scan_type, enabled in config.items():
        if enabled:
            running_tasks.append(scan_type)
        else:
            skipped_tasks.append(scan_type)
    message = (
    "\n"
    +" " * 25 
    +"CLOUD GUARD\n"
    + SEPARATOR
    + "\n"
    + f"Running Tasks : {', '.join(running_tasks)}\n"
    + f"Skipped Tasks : {', '.join(skipped_tasks)}\n"
    + SEPARATOR
)   
    feeder(message)

def scan_s3_buckets() -> None:
    feeder("\n" + SEPARATOR)
    feeder(" S3 SECURITY ASSESSMENT")
    feeder(SEPARATOR)
    session = create_session()
    s3_client = session.client('s3')
    for bucket in list_buckets(s3_client):
        feeder(f"\n[RESOURCE] {bucket}")
        
        results = [
        check(bucket,s3_client)
        for check in S3_SECURITY_CHECKS
]

        for result in results:
            feeder(result)
        
            
    feeder("\n" + SEPARATOR)
    feeder(" SCAN COMPLETE")
    feeder(SEPARATOR)

        

        

def main():
    setup_logger()
    scan_s3_buckets()


if __name__ == "__main__":
    main()