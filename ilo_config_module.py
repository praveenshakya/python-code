#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Your Name
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ilo_raid_config
short_description: Configure RAID on HPE iLO 5 using Redfish API
description:
  - This module configures a RAID array on an HPE server using iLO 5's Redfish API.
  - Supports RAID 0, RAID 1, and RAID 5.
  - Automatically detects available drives and applies the specified RAID configuration.
version_added: "1.0.0"
author:
  - Your Name (@yourgithub)
options:
  ilo_ip:
    description: The IP address or hostname of the iLO 5 interface.
    required: true
    type: str
  username:
    description: The iLO username with sufficient privileges to configure RAID.
    required: true
    type: str
    no_log: true
  password:
    description: The password for the iLO user.
    required: true
    type: str
    no_log: true
  raid_level:
    description: The RAID level to configure (Raid0, Raid1, or Raid5).
    required: false
    type: str
    choices: ["Raid0", "Raid1", "Raid5"]
    default: "Raid5"
requirements:
  - "python >= 3.6"
  - "requests"
"""

EXAMPLES = r"""
- name: Configure RAID 5 on HPE iLO
  ilo_raid_config:
    ilo_ip: "https://192.168.1.100"
    username: "admin"
    password: "password"
    raid_level: "Raid5"
"""

RETURN = r"""
changed:
  description: Indicates if the RAID configuration changed.
  returned: always
  type: bool
status_code:
  description: HTTP response code from iLO.
  returned: always
  type: int
msg:
  description: Status message of the RAID configuration process.
  returned: always
  type: str
error:
  description: Detailed error message if the operation failed.
  returned: when failure occurs
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
import requests
import json
from requests.auth import HTTPBasicAuth

def send_request(url, headers, auth, method="GET", payload=None):
    """Generic function to send HTTP requests with error handling."""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, auth=auth, verify=False, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, auth=auth, json=payload, verify=False, timeout=10)
        else:
            return {"error": f"Unsupported HTTP method: {method}", "status_code": 400}

        if response.status_code == 200:
            return {"status_code": 200, "data": response.json()}
        elif response.status_code == 201:
            return {"status_code": 201, "msg": "Resource created successfully."}
        elif response.status_code == 202:
            return {"status_code": 202, "msg": "Request accepted and processing."}
        elif response.status_code == 401:
            return {"error": "Authentication failed. Check username and password.", "status_code": 401}
        elif response.status_code == 404:
            return {"error": "Requested resource not found on iLO server.", "status_code": 404}
        elif response.status_code >= 500:
            return {"error": f"iLO server error: {response.status_code}", "status_code": response.status_code}
        else:
            return {"error": f"Unexpected response {response.status_code}: {response.text}", "status_code": response.status_code}

    except requests.exceptions.ConnectionError:
        return {"error": "Unable to connect to iLO. Check network connectivity.", "status_code": 503}
    except requests.exceptions.Timeout:
        return {"error": "Request to iLO timed out. Check iLO responsiveness.", "status_code": 504}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {str(e)}", "status_code": 500}

def get_available_drives(ilo_ip, username, password, headers):
    """Retrieve all available drives from iLO storage controller."""
    drives_path = f"{ilo_ip}/redfish/v1/Systems/1/Storage/1/Drives"
    result = send_request(drives_path, headers, HTTPBasicAuth(username, password))

    if "error" in result:
        return result  # Return error dictionary

    drives = result.get("data", {}).get("Members", [])
    return [drive["@odata.id"] for drive in drives] if drives else {"error": "No drives found on iLO.", "status_code": 404}

def create_raid_configuration(ilo_ip, username, password, headers, raid_level):
    """Configure a RAID array with available drives."""
    drives_result = get_available_drives(ilo_ip, username, password, headers)

    if "error" in drives_result:
        return {"changed": False, "msg": "RAID configuration failed.", "error": drives_result["error"], "status_code": drives_result["status_code"]}

    if not drives_result or len(drives_result) < 3:
        return {"changed": False, "msg": "Not enough drives available for RAID 5!", "status_code": 400}

    raid_payload = {
        "LogicalDrives": [
            {
                "Raid": raid_level,
                "CapacityGiB": 1000,
                "DataDrives": drives_result[:3]  # Select first 3 drives for RAID 5
            }
        ]
    }

    storage_action_path = f"{ilo_ip}/redfish/v1/Systems/1/Storage/1/Actions/Storage.ConfigureLogicalDrives"
    result = send_request(storage_action_path, headers, HTTPBasicAuth(username, password), method="POST", payload=raid_payload)

    if "error" in result:
        return {"changed": False, "msg": "RAID configuration failed.", "error": result["error"], "status_code": result["status_code"]}

    return {"changed": True, "msg": "RAID configuration initiated successfully!", "status_code": result["status_code"]}

def main():
    module_args = dict(
        ilo_ip=dict(type="str", required=True),
        username=dict(type="str", required=True, no_log=True),
        password=dict(type="str", required=True, no_log=True),
        raid_level=dict(type="str", default="Raid5", choices=["Raid0", "Raid1", "Raid5"])
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    ilo_ip = module.params["ilo_ip"]
    username = module.params["username"]
    password = module.params["password"]
    raid_level = module.params["raid_level"]

    headers = {"Content-Type": "application/json", "OData-Version": "4.0"}

    if module.check_mode:
        module.exit_json(changed=False, msg="Check mode: No changes will be made.", status_code=200)

    result = create_raid_configuration(ilo_ip, username, password, headers, raid_level)

    if "error" in result:
        module.fail_json(msg=result["msg"], error=result["error"], status_code=result["status_code"])
    
    module.exit_json(**result)

if __name__ == "__main__":
    main()