def interactive_update_json(json_data: dict, target_value, new_value) -> dict:
    """
    Finds all occurrences of a specific value in a JSON object, 
    displays them, and asks the user if they want to update each one.

    Args:
        json_data (dict): The JSON object to update.
        target_value: The value to search for and replace.
        new_value: The new value to set.

    Returns:
        dict: The updated JSON object.
    """
    def search_and_update(json_obj, parent_key=""):
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                full_key = f"{parent_key}.{key}" if parent_key else key

                if value == target_value:
                    print(f"\nFound match: Key = '{full_key}', Value = '{value}'")
                    response = input(f"Do you want to update this value to '{new_value}'? (Yes/No): ").strip().lower()
                    if response in ["yes", "y"]:
                        json_obj[key] = new_value
                        print(f"Updated: Key = '{full_key}', New Value = '{new_value}'")
                    else:
                        print(f"Skipped: Key = '{full_key}'")
                elif isinstance(value, (dict, list)):
                    search_and_update(value, full_key)
        elif isinstance(json_obj, list):
            for index, item in enumerate(json_obj):
                full_key = f"{parent_key}[{index}]"
                if item == target_value:
                    print(f"\nFound match: Key = '{full_key}', Value = '{item}'")
                    response = input(f"Do you want to update this value to '{new_value}'? (Yes/No): ").strip().lower()
                    if response in ["yes", "y"]:
                        json_obj[index] = new_value
                        print(f"Updated: Key = '{full_key}', New Value = '{new_value}'")
                    else:
                        print(f"Skipped: Key = '{full_key}'")
                elif isinstance(item, (dict, list)):
                    search_and_update(item, full_key)

    search_and_update(json_data)
    return json_data

# Example JSON data with duplicate values
json_data = {
    "primary_ip": "192.168.1.1",
    "secondary_ip": "192.168.1.2",
    "servers": [
        {"name": "server1", "ip": "192.168.1.1"},
        {"name": "server2", "ip": "192.168.1.3"},
        {"name": "server3", "ip": "192.168.1.1"}
    ],
    "metadata": {
        "datacenter_ip": "192.168.1.1",
        "status": "active"
    }
}

# Interactive update
target_value = "192.168.1.1"
new_value = "10.0.0.1"
updated_json = interactive_update_json(json_data, target_value, new_value)

# Display final JSON
print("\nFinal JSON after updates:")
print(updated_json)


{
    "primary_ip": "192.168.1.1",
    "secondary_ip": "192.168.1.2",
    "servers": [
        {"name": "server1", "ip": "192.168.1.1"},
        {"name": "server2", "ip": "192.168.1.3"},
        {"name": "server3", "ip": "192.168.1.1"}
    ],
    "metadata": {
        "datacenter_ip": "192.168.1.1",
        "status": "active"
    }
}


Found match: Key = 'primary_ip', Value = '192.168.1.1'
Do you want to update this value to '10.0.0.1'? (Yes/No): Yes
Updated: Key = 'primary_ip', New Value = '10.0.0.1'

Found match: Key = 'servers[0].ip', Value = '192.168.1.1'
Do you want to update this value to '10.0.0.1'? (Yes/No): No
Skipped: Key = 'servers[0].ip'

Found match: Key = 'servers[2].ip', Value = '192.168.1.1'
Do you want to update this value to '10.0.0.1'? (Yes/No): Yes
Updated: Key = 'servers[2].ip', New Value = '10.0.0.1'

Found match: Key = 'metadata.datacenter_ip', Value = '192.168.1.1'
Do you want to update this value to '10.0.0.1'? (Yes/No): Yes
Updated: Key = 'metadata.datacenter_ip', New Value = '10.0.0.1'

{
    "primary_ip": "10.0.0.1",
    "secondary_ip": "192.168.1.2",
    "servers": [
        {"name": "server1", "ip": "192.168.1.1"},
        {"name": "server2", "ip": "192.168.1.3"},
        {"name": "server3", "ip": "10.0.0.1"}
    ],
    "metadata": {
        "datacenter_ip": "10.0.0.1",
        "status": "active"
    }
}
