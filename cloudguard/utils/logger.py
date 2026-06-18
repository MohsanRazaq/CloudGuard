from datetime import datetime
from constants import LOGGER_PATH
import os
def write_log(message:str)->None:
    TIMESTAMP=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg=(f"[{TIMESTAMP}] {message}")
    os.makedirs(LOGGER_PATH,exist_ok=True)
    print(msg)
    with open(f'{LOGGER_PATH}/cloudguard.log','a') as f:
        f.write(msg+"\n\n")
    
