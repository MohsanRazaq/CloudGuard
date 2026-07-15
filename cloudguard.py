import argparse
import subprocess
import sys
from datetime import datetime

from cloudguard.utils.logger import feeder
from cloudguard.utils.config_loader import load_config
from cloudguard.findings import COLORS
from cloudguard.aws.session import create_session

from cloudguard.reporting.summary import print_summary
from cloudguard.reporting.html_exporter import export_to_html
from cloudguard.reporting.json_exporter import export_to_json

from engine.scan_engine import ScanEngine


def report(findings, bucket_count, start_time, end_time):
    print_summary(findings, bucket_count, start_time, end_time)


def main():
    parser = argparse.ArgumentParser(
        description="CloudGuard: Lightweight AWS Security Scanner"
    )

    parser.add_argument(
        "--scan",
        action="store_true",
        help="Execute security scans"
    )

    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Launch the interactive Streamlit dashboard"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Export findings to JSON"
    )

    parser.add_argument(
        "--html",
        action="store_true",
        help="Export findings to HTML"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Print terminal summary report"
    )

    args = parser.parse_args()

    start_time = datetime.now()

    findings = []
    bucket_count = 0

    config = load_config()
    running_tasks = [
        task for task, enabled in config.items() if enabled
    ]

    if args.scan:

        session = create_session()

        engine = ScanEngine(session)

        findings, metadata = engine.run()
        bucket_count=metadata["bucket_count"]

    else:
        feeder(
            f"\n{COLORS['YELLOW']}[WARN]{COLORS['RESET']} "
            "No scan requested. Use --scan to run assessment."
        )

    end_time = datetime.now()

    # -Report 

    if args.report:
        if findings:
            report(findings, bucket_count, start_time, end_time)
        else:
            print("No findings to report.")
    else:
        print("No summary report requested.")

    # - JSON -

    if args.json:
        if findings:
            export_to_json(findings, running_tasks)
        else:
            print("No findings to export to JSON.")
    else:
        print("No JSON output requested.")

    # - HTML 

    if args.html:
        if findings:
            feeder(
                f"\n{COLORS['GREEN']}[INFO]{COLORS['RESET']} Exporting HTML report..."
            )
            export_to_html(findings, running_tasks)
        else:
            print("No findings to export to HTML.")
    else:
        print("No HTML output requested.")

    # - Dashboard 

    if args.dashboard:
        feeder(
            f"\n{COLORS['GREEN']}[INFO]{COLORS['RESET']} Launching CloudGuard Dashboard..."
        )

        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    "dashboard/app.py",
                ]
            )
        except KeyboardInterrupt:
            feeder(
                f"\n{COLORS['YELLOW']}[INFO]{COLORS['RESET']} Dashboard stopped by user."
            )


if __name__ == "__main__":
    main()