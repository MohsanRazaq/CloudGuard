from cloudguard.utils.config_loader import load_config
from cloudguard.utils.logger import write_log
from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.reporting.summary import print_summary
from cloudguard.security_checks.check_bucket_versioning import (
    check_bucket_versioning
)
from cloudguard.findings import COLORS
from cloudguard.aws.session import create_session
from cloudguard.constants import SEPARATOR
from cloudguard.security_checks.check_bucket_encryption import check_bucket_encryption
from cloudguard.security_checks.check_bucket_public_block import check_public_access_block
from cloudguard.security_checks.check_bucket_logging import check_bucket_logging
from cloudguard.security_checks.check_bucket_acl import check_bucket_acl


################################################################################
S3_SECURITY_CHECKS = [
    check_bucket_versioning,
    check_bucket_encryption,
    check_public_access_block,
    check_bucket_logging,
    check_bucket_acl
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

def scan_s3_buckets() :
    all_findings = []
    feeder("\n" + SEPARATOR)
    feeder(f"{COLORS['BOLD']} S3 SECURITY ASSESSMENT")
    feeder(SEPARATOR)
    session = create_session()
    s3_client = session.client('s3')
    buckets=list_buckets(s3_client)
    bucket_count=len(buckets)
    for bucket in buckets:
        feeder(f"\n{COLORS['BLUE']}[RESOURCE]{COLORS['RESET']} {bucket} \n")
        
        results = [
        check(bucket,s3_client)
        for check in S3_SECURITY_CHECKS
]

        for result in results:
            feeder(result)
        all_findings.extend(results)
        
            
    return  all_findings , bucket_count
        

def main():
    setup_logger()
    findings,bucket_count=scan_s3_buckets()
    
    print_summary(findings,bucket_count)

if __name__ == "__main__":
    main()