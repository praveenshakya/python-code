def interactive_bulk_update_json_v4(json_data: dict, target_value, new_value) -> dict:
    """
    Displays all keys with a specific value, allows the user to update all or select specific keys,
    provides an exit option, and performs the updates.

    Args:
        json_data (dict): The JSON object to update.
        target_value: The value to search for and replace.
        new_value: The new value to set.

    Returns:
        dict: The updated JSON object.
    """
    # Use find_all_keys_by_value to get matches
    matches = find_all_keys_by_value(json_data, target_value)

    # Display matches
    if not matches:
        print("No matches found.")
        return json_data

    print("\nThe following keys have the target value:")
    for idx, (key, value, _, _) in enumerate(matches, start=1):
        print(f"{idx}. Key: {key}, Current Value: {value}, New Value: {new_value}")
    print("all. Update all keys with the target value.")
    print("exit. Exit without making any changes.")

    # Get user input for which keys to update
    selection = input("\nEnter the numbers corresponding to the keys you want to update (comma-separated, 'all' for all, or 'exit' to cancel): ").strip().lower()

    if selection == "exit":
        print("\nNo changes were made.")
        return json_data  # Exit without changes

    if selection == "all":
        # Update all matches
        for key, value, parent, child_key in matches:
            parent[child_key] = new_value
            print(f"Updated: Key = '{key}', New Value = '{new_value}'")
    else:
        # Process user-selected keys
        try:
            selected_indices = {int(num.strip()) for num in selection.split(",") if num.strip().isdigit()}
            for idx, (key, value, parent, child_key) in enumerate(matches, start=1):
                if idx in selected_indices:
                    parent[child_key] = new_value
                    print(f"Updated: Key = '{key}', New Value = '{new_value}'")
        except ValueError:
            print("Invalid input. No changes were made.")
            return json_data  # Exit without changes

    # Display final JSON
    print("\nFinal JSON after updates:")
    return json_data


def find_all_keys_by_value(json_data: dict, target_value) -> list[tuple[str, any, any]]:
    """
    Finds all keys in a JSON object that have the specified target value.

    Args:
        json_data (dict): The JSON object to search.
        target_value: The value to search for.

    Returns:
        list[tuple[str, any, any]]: A list of tuples containing:
            - The full key path.
            - The current value.
            - A reference to the parent object (dict or list).
            - The key or index in the parent object.
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

    search(json_data)
    return matches


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
updated_json = interactive_bulk_update_json_v4(json_data, target_value, new_value)

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
all. Update all keys with the target value.
exit. Exit without making any changes.

Enter the numbers corresponding to the keys you want to update (comma-separated, 'all' for all, or 'exit' to cancel): all

Updated: Key = 'primary_ip', New Value = '10.0.0.1'
Updated: Key = 'servers[0].ip', New Value = '10.0.0.1'
Updated: Key = 'servers[2].ip', New Value = '10.0.0.1'
Updated: Key = 'metadata.datacenter_ip', New Value = '10.0.0.1'

Final JSON after updates:
{
    "primary_ip": "10.0.0.1",
    "secondary_ip": "192.168.1.2",
    "servers": [
        {"name": "server1", "ip": "10.0.0.1"},
        {"name": "server2", "ip": "192.168.1.3"},
        {"name": "server3", "ip": "10.0.0.1"}
    ],
    "metadata": {
        "datacenter_ip": "10.0.0.1",
        "status": "active"
    }
}

# Exit Example
The following keys have the target value:
1. Key: primary_ip, Current Value: 192.168.1.1, New Value: 10.0.0.1
2. Key: servers[0].ip, Current Value: 192.168.1.1, New Value: 10.0.0.1
3. Key: servers[2].ip, Current Value: 192.168.1.1, New Value: 10.0.0.1
4. Key: metadata.datacenter_ip, Current Value: 192.168.1.1, New Value: 10.0.0.1
all. Update all keys with the target value.
exit. Exit without making any changes.

Enter the numbers corresponding to the keys you want to update (comma-separated, 'all' for all, or 'exit' to cancel): exit

No changes were made.




