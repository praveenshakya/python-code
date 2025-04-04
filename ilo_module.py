from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = """
---
module: ilo_create_logical_drive
short_description: Create logical drive in iLO using Redfish API
options:
  ilo_ip:
    description: iLO IP Address
    required: true
    type: str
  ilo_username:
    description: iLO Username
    required: true
    type: str
  ilo_password:
    description: iLO Password
    required: true
    type: str
  raid_level:
    description: RAID level (e.g., Raid1, Raid5)
    required: true
    type: str
  data_drives:
    description: List of drive numbers to use for the logical drive
    required: true
    type: list
  bootable:
    description: Whether the drive should be bootable
    required: false
    type: bool
    default: false
"""


def get_first_array_controller(ilo_ip, ilo_username, ilo_password, headers):
    controllers_url = f"https://{ilo_ip}/redfish/v1/Systems/1/SmartStorage/ArrayControllers/"
    response = requests.get(controllers_url, headers=headers, auth=(ilo_username, ilo_password), verify=False)
    if response.status_code == 200:
        controllers = response.json().get('Members', [])
        if controllers:
            return controllers[0]['@odata.id'].split('/')[-1]  # Return first controller ID
    return "0"  # Default to 0 if no controller found


def create_logical_drive(module):
    ilo_ip = module.params['ilo_ip']
    ilo_username = module.params['ilo_username']
    ilo_password = module.params['ilo_password']
    raid_level = module.params['raid_level']
    data_drives = module.params['data_drives']
    bootable = module.params['bootable']

    headers = {"Content-Type": "application/json"}
    controller_id = get_first_array_controller(ilo_ip, ilo_username, ilo_password, headers)

    base_drive_path = f"/redfish/v1/Systems/1/SmartStorage/ArrayControllers/{controller_id}/DiskDrives/"
    drive_paths = [base_drive_path + str(drive) for drive in data_drives]

    url = f"https://{ilo_ip}/redfish/v1/Systems/1/SmartStorage/ArrayControllers/{controller_id}/LogicalDrives/"
    payload = {
        "LogicalDrives": [
            {
                "Raid": raid_level,
                "DataDrives": drive_paths,
                "CapacityMiB": 100000,
                "Accelerator": "None",
                "Bootable": bootable
            }
        ],
        "DataGuard": "Disabled"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, auth=(ilo_username, ilo_password), verify=False)
        if response.status_code in [200, 201, 202]:
            module.exit_json(changed=True, msg="Logical drive created successfully.")
        else:
            module.fail_json(msg=f"Failed to create logical drive: {response.text}")
    except Exception as e:
        module.fail_json(msg=f"Error: {str(e)}")


def main():
    module_args = {
        "ilo_ip": {"type": "str", "required": True},
        "ilo_username": {"type": "str", "required": True},
        "ilo_password": {"type": "str", "required": True, "no_log": True},
        "raid_level": {"type": "str", "required": True},
        "data_drives": {"type": "list", "required": True},
        "bootable": {"type": "bool", "required": False, "default": False},
    }
    module = AnsibleModule(argument_spec=module_args)
    create_logical_drive(module)

if __name__ == "__main__":
    main()
