from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = """
---
module: ilo_create_logical_drive
short_description: Create logical drive in iLO using Redfish API (iLO 5)
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
  logical_drive_name:
    description: Name of the logical drive
    required: true
    type: str
  data_drive_count:
    description: Number of data drives
    required: true
    type: int
  media_type:
    description: Media type (e.g., HDD or SSD)
    required: true
    type: str
  interface_type:
    description: Interface type (e.g., SAS or SATA)
    required: true
    type: str
  minimum_size_gib:
    description: Minimum size in GiB for the drives
    required: true
    type: int
"""


def create_logical_drive(module):
    ilo_ip = module.params['ilo_ip']
    ilo_username = module.params['ilo_username']
    ilo_password = module.params['ilo_password']
    raid_level = module.params['raid_level']
    logical_drive_name = module.params['logical_drive_name']
    data_drive_count = module.params['data_drive_count']
    media_type = module.params['media_type']
    interface_type = module.params['interface_type']
    minimum_size_gib = module.params['minimum_size_gib']

    headers = {"Content-Type": "application/json"}
    url = f"https://{ilo_ip}/redfish/v1/Systems/1/smartstorageconfig/settings/"

    payload = {
        "DataGuard": "Disabled",
        "LogicalDrives": [
            {
                "LogicalDriveName": logical_drive_name,
                "Raid": raid_level,
                "DataDrives": {
                    "DataDriveCount": data_drive_count,
                    "DataDriveMediaType": media_type,
                    "DataDriveInterfaceType": interface_type,
                    "DataDriveMinimumSizeGiB": minimum_size_gib
                }
            }
        ]
    }

    try:
        response = requests.put(url, json=payload, headers=headers, auth=(ilo_username, ilo_password), verify=False)
        if response.status_code in [200, 201, 202]:
            module.exit_json(changed=True, msg="Logical drive created successfully.")
        else:
            module.fail_json(msg=f"Failed to create logical drive: {response.status_code} - {response.text}")
    except Exception as e:
        module.fail_json(msg=f"Error: {str(e)}")


def main():
    module_args = {
        "ilo_ip": {"type": "str", "required": True},
        "ilo_username": {"type": "str", "required": True},
        "ilo_password": {"type": "str", "required": True, "no_log": True},
        "raid_level": {"type": "str", "required": True},
        "logical_drive_name": {"type": "str", "required": True},
        "data_drive_count": {"type": "int", "required": True},
        "media_type": {"type": "str", "required": True},
        "interface_type": {"type": "str", "required": True},
        "minimum_size_gib": {"type": "int", "required": True},
    }
    module = AnsibleModule(argument_spec=module_args)
    create_logical_drive(module)

if __name__ == "__main__":
    main()
