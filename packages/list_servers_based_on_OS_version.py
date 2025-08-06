import os
import glob
import json
import sys

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <rhel_version> <env: r/s/t/p>")
        sys.exit(1)

    rhel_version = sys.argv[1]
    env = sys.argv[2]

    env_map = {
        'r': 'rese',
        's': 'syst',
        't': 'test',
        'p': 'prod'
    }

    if env not in env_map:
        print("Invalid environment input. Use one of r,s,t,p.")
        sys.exit(1)

    server_environment = env_map[env]

    json_files_dir = "/var/opt/reports"
    json_report_pattern = f"svli{env}c*.rpt"
    json_reports = glob.glob(os.path.join(json_files_dir, json_report_pattern))

    counter = 0
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

                ansible_facts = data.get('ansible_facts', {})
                os_version = ansible_facts.get('ansible_distribution_version', '')

                if os_version == rhel_version:
                    counter += 1
                    servers_list.append(server_name)

    print(f"Found {counter} servers running RHEL version {rhel_version} in environment '{server_environment}':")

    if servers_list:
        output_report = f"/var/tmp/rhel_{rhel_version}_{server_environment}.txt"
        with open(output_report, "a") as of:
            for server in servers_list:
                of.write(f"{server}\n")
        print(f"Report written to: {output_report}")

if __name__ == "__main__":
    main()
