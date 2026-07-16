from datetime import datetime
import os
from cloudguard.findings import COLORS

from cloudguard.constants import LOGGER_PATH

def write_log(message: str) -> None:
    #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs(LOGGER_PATH, exist_ok=True)

    with open(f"{LOGGER_PATH}/cloudguard.log", "a") as f:
        f.write(f" {message}\n")
        
        
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