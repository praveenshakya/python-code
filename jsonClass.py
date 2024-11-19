def find_all_keys_by_value(json_data: dict, target_value) -> list[tuple[str, any]]:
    """
    Finds all keys in a JSON object that contain the specified value,
    including cases where the value appears multiple times.

    Args:
        json_data (dict): The JSON object to search.
        target_value: The value to search for.

    Returns:
        list[tuple[str, any]]: A list of tuples with the key path and value.
    """
    results = []

    def search(json_obj, parent_key=""):
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                full_key = f"{parent_key}.{key}" if parent_key else key

                if value == target_value:
                    results.append((full_key, value))
                elif isinstance(value, (dict, list)):
                    search(value, full_key)
        elif isinstance(json_obj, list):
            for index, item in enumerate(json_obj):
                full_key = f"{parent_key}[{index}]"
                if item == target_value:
                    results.append((full_key, item))
                elif isinstance(item, (dict, list)):
                    search(item, full_key)

    search(json_data)
    return results


# Example JSON data with duplicate IPs
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

# Search for all occurrences of an IP address
target_value = "192.168.1.1"
matches = find_all_keys_by_value(json_data, target_value)

# Display results
if matches:
    for key, value in matches:
        print(f"Found match: Key = '{key}', Value = '{value}'")
else:
    print("No matches found.")
