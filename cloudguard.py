import json,argparse
from datetime import datetime
from cloudguard.utils.config_loader import load_config
from cloudguard.utils.logger import write_log
from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.aws.iam_scanner import scan_iam
from cloudguard.reporting.summary import print_summary
from cloudguard.security_checks.s3.check_bucket_versioning import (
    check_bucket_versioning
)
from cloudguard.findings import COLORS
from cloudguard.aws.session import create_session
from cloudguard.constants import SEPARATOR
from cloudguard.security_checks.s3.check_bucket_encryption import check_bucket_encryption
from cloudguard.security_checks.s3.check_bucket_public_block import check_public_access_block
from cloudguard.security_checks.s3.check_bucket_logging import check_bucket_logging
from cloudguard.security_checks.s3.check_bucket_acl import check_bucket_acl
from cloudguard.security_checks.s3.check_bucket_policy import check_bucket_policy



S3_SECURITY_CHECKS = [
    check_bucket_versioning,
    check_bucket_encryption,
    check_public_access_block,
    check_bucket_logging,
    check_bucket_acl,
    check_bucket_policy
]



def feeder(message: object, plain_text_log: str = "") -> None:
    """print colorized output to console but writes clean text to log files."""
    text_to_print = str(message)
    print(text_to_print)
    
    if plain_text_log:
        write_log(plain_text_log)
    else:
        clean_text = text_to_print
        for code in COLORS.values():
            clean_text = clean_text.replace(code, "")
        write_log(clean_text)
#############################################################################################
session = create_session()
s3_client = session.client('s3')
iam_client = session.client("iam")
    
################################################################################################
def setup_logger() -> None:
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
        + " " * 25 
        + f"{COLORS['GREEN']}CLOUD GUARD{COLORS['RESET']}\n"
        + SEPARATOR
        + "\n"
        + f"Running Tasks : {', '.join(running_tasks)}\n"
        + f"Skipped Tasks : {', '.join(skipped_tasks)}\n"
        + SEPARATOR
    )   
    feeder(message)
################################################################################################

def scan_s3_buckets() :
    all_findings = []
    feeder("\n" + SEPARATOR)
    feeder(f"{COLORS['BOLD']} S3 SECURITY ASSESSMENT")
    feeder(SEPARATOR)
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

################################################################################################

def export_to_json(all_findings,running_tasks):
    
    findings_list=[finding.to_dict() for finding in all_findings]    
    json_payload={
        "scan_metadata": {
            "engine": "CloudGuard",
            "version": "v0.1.0",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tasks_run": running_tasks
        },
        "findings": findings_list} 
    report_filename="cloudguard_report.json"
    with open (report_filename,'w') as json_file:
        json.dump(json_payload,json_file,indent=4)
    feeder(f"\n{COLORS['GREEN']}JSON report exported successfully to {report_filename}!{COLORS['RESET']}")
    
################################################################################################
def report(findings,buck_c,sT,eT):
    print_summary(findings, buck_c, sT, eT)

#################################################################################################
def main():
    parser = argparse.ArgumentParser(
        description='CloudGuard: Lightweight AWS Security Scanner'
    )
    parser.add_argument(
        "--scan",
        action='store_true',
        help="Execute S3 and IAM security scans"
    )
    parser.add_argument(
        "--json",
        action='store_true',
        help="Write scan results to a JSON report file"
    )
    parser.add_argument(
        "--report",
        action='store_true',
        help="Print a summary report to the terminal"
    )
    
    args = parser.parse_args()
    
    start_time = datetime.now()
    findings = []
    bucket_count = 0
    config = load_config()
    running_tasks = [task for task, enabled in config.items() if enabled]

    if args.scan:
        setup_logger()
        
        if config.get("s3", True): 
            s3_findings, bucket_count = scan_s3_buckets()
            findings.extend(s3_findings)
            
        if config.get("iam", True):
            iam_findings = scan_iam(iam_client, feeder)
            findings.extend(iam_findings)
    else:
        feeder(f"\n{COLORS['YELLOW']}[WARN]{COLORS['RESET']} No scan requested. Use --scan to run assessment.")

    end_time = datetime.now()
    
    if args.report:
        if findings:
            report(findings, bucket_count, start_time, end_time)
        else:
            print("No findings to report. Did you run the scan with --scan?")
    else:
        print("No summary report requested (missing --report).")
        
    if args.json:
        if findings:
            export_to_json(findings, running_tasks)
        else:
            print("No findings to export to JSON.")
    else:
        print("Execution completed. No JSON output file requested.")
        
if __name__=="__main__":
    main()