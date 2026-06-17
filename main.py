from constants import PROJECT_NAME,SERVICES



def start_scan():
    
    print("=================================")
    print("CloudGuard Started")
    print("=================================")
    print(PROJECT_NAME)
    for service in SERVICES:
        print(f'Future Scanner: {service}')

start_scan()