import os
import json
import glob
from datetime import datetime
from enum import Enum

class ServerEnv(Enum):
    rese = 'rese'
    test = 'test'
    syst = 'syst'
    prod = 'prod'

def main():
    counter = 0
    json_files_dir = '/var/opt/reports/puppet_db'
    environment = input("Enter environment (r, s, t, p): ").lower()
    
    # Map input char to environment string
    env_map = {
        'r': 'rese',
        's': 'syst',
        't': 'test',
        'p': 'prod'
    }
    
    if environment not in env_map:
        print("Invalid environment input. Use one of r,s,t,p.")
        return
    
    server_environment = env_map[environment]
    
    json_reports = glob.glob(os.path.join(json_files_dir, f'svlipcl{environment}*.rpt'))
    
    rhel_version = input("Enter OS version: ").strip()
    login_id = os.getlogin()
    date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    output_report = f'/tmp/{server_environment}_{rhel_version}_{login_id}_{date_time}.txt'
    
    servers_list = []
    
    for report in json_reports:
        if os.path.getsize(report) > 0:
            server_name = os.path.basename(report).split('.')[0]
            with open(report) as json_report:
                try:
                    data = json.load(json_report)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON file: {report}")
                    continue
                
                # Assuming OS info is nested like this (adjust if needed)
                os_version = data.get('platform', {}).get('release', {}).get('full', '')
                
                if os_version == rhel_version:
                    #print(f"{server_name} running on {rhel_version}")
                    counter += 1
                    servers_list.append(server_name)
    
    if servers_list:
        with open(output_report, "a") as of:
            for server in servers_list:
                of.write(f"{server}\n")
    
    if counter > 0:
        print(f"Total {counter} servers running on {rhel_version}")
        print(f"Report is saved at {output_report}")
    else:
        print("No servers found")

if __name__ == "__main__":
    main()
