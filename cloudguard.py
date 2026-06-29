from cloudguard.utils.config_loader import load_config
from cloudguard.utils.logger import write_log
from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.security_checks.s3_checks import (
    check_bucket_versioning
)
from cloudguard.constants import SEPARATOR
from cloudguard.security_checks.encryption_check import check_bucket_encryption

################################################################################
S3_CHECKS = [
    check_bucket_versioning,
    check_bucket_encryption,
]


def feeder(message) -> None:
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

def scan_s3_buckets()->None:
    feeder("\n" + SEPARATOR)
    feeder("S3 Discovery")
    feeder(SEPARATOR)
    

    for bucket in list_buckets():
        discovery_message=f"[DISCOVERED] {bucket}"
        feeder(discovery_message)

        for check in S3_CHECKS:
            result = check(bucket)

            if result:
                feeder(result)
        

        

def main():
    setup_logger()
    scan_s3_buckets()


if __name__ == "__main__":
    main()