import glob
import os
import json
import sys
from enum import Enum

class ServerEnvironment(Enum):
    r = 'rese'
    t = 'test'
    s = 'syst'
    p = 'prod'

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <package> <version> <env: r,s,t,p>")
        sys.exit(1)

    rpm = sys.argv[1]
    rpm_version = sys.argv[2]
    env = sys.argv[3]

    if env not in ServerEnvironment.__members__:
        print(f"Invalid environment '{env}'. Use one of: r, s, t, p")
        sys.exit(1)

    server_env = ServerEnvironment[env].value

    json_files_dir = "/var/opt/reports/puppet_db"
    json_pattern = f"svli{env}c*.rpt"
    json_reports = glob.glob(os.path.join(json_files_dir, json_pattern))

    if not json_reports:
        print(f"No report files found matching pattern '{json_pattern}' in {json_files_dir}")
        sys.exit(1)

    output_file = f"/tmp/{rpm}_{server_env}.txt"
    installed_servers = []

    print(f"Searching {len(json_reports)} report(s) for package '{rpm}' version '{rpm_version}' in environment '{server_env}'...")

    for report in json_reports:
        if os.path.getsize(report) == 0:
            print(f"Skipping empty file: {report}")
            continue

        server_name = os.path.basename(report).split('.')[0]

        try:
            with open(report) as jf:
                server_data = json.load(jf)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON file: {report}")
            continue

        # In your JSON, packages are top-level keys
        packages = server_data

        # Debug print: uncomment to see all packages found in report
        # print(f"{server_name} packages: {list(packages.keys())}")

        if rpm in packages:
            version_found = packages[rpm][0].get('version', '')
            if version_found == rpm_version:
                print(f"Found {rpm} version {rpm_version} on {server_name}")
                installed_servers.append(server_name)
            else:
                # For debugging version mismatch
                # print(f"{server_name}: {rpm} version mismatch (found {version_found})")
                pass
        else:
            # For debugging package missing
            # print(f"{server_name}: {rpm} not installed")
            pass

    if installed_servers:
        with open(output_file, 'w') as of:
            for server in installed_servers:
                of.write(f"{server}\n")
        print(f"\nFile saved with list of servers: {output_file}")
    else:
        print(f"\nNo servers found with package '{rpm}' version '{rpm_version}' in environment '{server_env}'.")

if __name__ == "__main__":
    main()
