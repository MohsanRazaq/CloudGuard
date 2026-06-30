from datetime import datetime
import os
from cloudguard.constants import LOGGER_PATH

def write_log(message: str) -> None:
    #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs(LOGGER_PATH, exist_ok=True)

    with open(f"{LOGGER_PATH}/cloudguard.log", "a") as f:
        f.write(f" {message}\n")
        