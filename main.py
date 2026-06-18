from cloudguard.constants import PROJECT_NAME,SERVICES,LOGGER_PATH
from cloudguard.utils.logger import write_log
from cloudguard.utils.config_loader import load_config

def start_scan():
    
    print("=================================")
    print("CloudGuard Started")
    print("=================================")
    print(PROJECT_NAME)
    for service in SERVICES:
        print(f'Future Scanner: {service}')
        

def setup_logger():
    config=load_config()
    running_tasks=[]
    skiiped_tasks=[]
    for scan_type,is_enabled in config.items():
        if is_enabled:
            print(f'Running Tasks: {scan_type}')
            running_tasks.append(scan_type)
        else:
            print(f'Skipped  Tasks: {scan_type}')
            skiiped_tasks.append(scan_type)
            
    message=f'CloudGuard Started\nRunning:{running_tasks}\nskipped:{skiiped_tasks}'
    
    write_log(message)




if __name__=="__main__":
    setup_logger()    
    start_scan()

