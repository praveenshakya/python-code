def interactive_bulk_update_json(json_data: dict, target_value, new_value) -> dict:
    """
    Displays all keys with a specific value, allows the user to select which keys 
    to update using comma-separated input, and performs the updates.

    Args:
        json_data (dict): The JSON object to update.
        target_value: The value to search for and replace.
        new_value: The new value to set.

    Returns:
        dict: The updated JSON object.
    """
    matches = []

    def search(json_obj, parent_key=""):
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                full_key = f"{parent_key}.{key}" if parent_key else key

                if value == target_value:
                    matches.append((full_key, value, json_obj, key))
                elif isinstance(value, (dict, list)):
                    search(value, full_key)
        elif isinstance(json_obj, list):
            for index, item in enumerate(json_obj):
                full_key = f"{parent_key}[{index}]"
                if item == target_value:
                    matches.append((full_key, item, json_obj, index))
                elif isinstance(item, (dict, list)):
                    search(item, full_key)

    # Find all matches
    search(json_data)

    # Display matches
    if not matches:
        print("No matches found.")
        return json_data

    print("\nThe following keys have the target value:")
    for idx, (key, value, _, _) in enumerate(matches, start=1):
        print(f"{idx}. Key: {key}, Current Value: {value}, New Value: {new_value}")

    # Get user input for which keys to update
    selection = input("\nEnter the numbers corresponding to the keys you want to update (comma-separated): ").strip()

    # Process user input
    if selection:
        selected_indices = {int(num.strip()) for num in selection.split(",") if num.strip().isdigit()}

        # Update selected keys
        for idx, (key, value, parent, child_key) in enumerate(matches, start=1):
            if idx in selected_indices:
                parent[child_key] = new_value
                print(f"Updated: Key = '{key}', New Value = '{new_value}'")

    # Display final JSON
    print("\nFinal JSON after updates:")
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
updated_json = interactive_bulk_update_json(json_data, target_value, new_value)

# Display final JSON
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

The following keys have the target value:
1. Key: primary_ip, Current Value: 192.168.1.1, New Value: 10.0.0.1
2. Key: servers[0].ip, Current Value: 192.168.1.1, New Value: 10.0.0.1
3. Key: servers[2].ip, Current Value: 192.168.1.1, New Value: 10.0.0.1
4. Key: metadata.datacenter_ip, Current Value: 192.168.1.1, New Value: 10.0.0.1

Enter the numbers corresponding to the keys you want to update (comma-separated): 1, 4

Updated: Key = 'primary_ip', New Value = '10.0.0.1'
Updated: Key = 'metadata.datacenter_ip', New Value = '10.0.0.1'

Final JSON after updates:
{
    "primary_ip": "10.0.0.1",
    "secondary_ip": "192.168.1.2",
    "servers": [
        {"name": "server1", "ip": "192.168.1.1"},
        {"name": "server2", "ip": "192.168.1.3"},
        {"name": "server3", "ip": "192.168.1.1"}
    ],
    "metadata": {
        "datacenter_ip": "10.0.0.1",
        "status": "active"
    }
}


