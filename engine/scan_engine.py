from cloudguard.utils.config_loader import load_config
from cloudguard.utils.logger import feeder

from cloudguard.findings import COLORS
from cloudguard.constants import SEPARATOR

from engine.registry import SCANNERS


class ScanEngine:

    def __init__(self, session):
        self.session = session
        self.config = load_config()

    def setup_logger(self):

        running_tasks = [
            task for task, enabled in self.config.items()
            if enabled
        ]

        skipped_tasks = [
            task for task, enabled in self.config.items()
            if not enabled
        ]

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

    def run(self):

        self.setup_logger()

        findings = []
        engine_metadata = {
            "bucket_count": 0
        }


        for service,scanner in SCANNERS.items():
            if not self.config.get(service,True):
                continue
            service_finding,metadata=scanner(
                self.session
            )
            findings.extend(service_finding)
            
            engine_metadata["bucket_count"]+=metadata.get("bucket_count",0)
        
        


        return findings, engine_metadata