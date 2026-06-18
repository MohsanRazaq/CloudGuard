from constants import PROJECT_NAME,SERVICES,LOGGER_PATH
from cloudguard.utils.logger import write_log
def start_scan():
    
    print("=================================")
    print("CloudGuard Started")
    print("=================================")
    print(PROJECT_NAME)
    for service in SERVICES:
        print(f'Future Scanner: {service}')
        

def setup_logger():
    message='CloudGuard Started'
    
    write_log(message)




if __name__=="__main__":
    setup_logger()    
    start_scan()

