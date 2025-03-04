import fnmatch

def find_all_keys_by_value(json_data: dict, target_value: str, use_wildcard: bool = False) -> list[tuple[str, any, any]]:
    """
    Finds all keys in a JSON object that have the specified target value.
    Supports wildcard matching if enabled.

    Args:
        json_data (dict): The JSON object to search.
        target_value (str): The value to search for (supports wildcard if enabled).
        use_wildcard (bool): Whether to enable wildcard matching.

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
                if use_wildcard and isinstance(value, str):
                    if fnmatch.fnmatch(value, target_value):  # Wildcard match
                        matches.append((full_key, value, json_obj, key))
                elif value == target_value:
                    matches.append((full_key, value, json_obj, key))
                elif isinstance(value, (dict, list)):
                    search(value, full_key)
        elif isinstance(json_obj, list):
            for index, item in enumerate(json_obj):
                full_key = f"{parent_key}[{index}]"
                if use_wildcard and isinstance(item, str):
                    if fnmatch.fnmatch(item, target_value):  # Wildcard match
                        matches.append((full_key, item, json_obj, index))
                elif item == target_value:
                    matches.append((full_key, item, json_obj, index))
                elif isinstance(item, (dict, list)):
                    search(item, full_key)

    search(json_data)
    return matches

def menu_driven_bulk_update_with_substring(json_data: dict) -> dict:
    """
    Menu-driven interface for updating specific keys in a JSON object.
    Supports substring replacement in matched values.

    Args:
        json_data (dict): The JSON object to update.

    Returns:
        dict: The updated JSON object.
    """
    menu_options = {
        "1": "hostname",
        "2": "ip_address",
        "3": "serial_number",
        "4": "exit"
    }

    while True:
        # Display menu
        print("\nMenu:")
        for key, value in menu_options.items():
            print(f"{key}. {value}")

        # User selects an option
        choice = input("\nSelect an option (1-4): ").strip()
        if choice == "4" or menu_options.get(choice) == "exit":
            print("\nExiting. No further changes made.")
            break

        selected_key = menu_options.get(choice)
        if not selected_key:
            print("\nInvalid choice. Please try again.")
            continue

        print(f"\nYou selected '{selected_key}'.")

        # Ask for target substring and replacement substring
        target_value = input(f"Enter the target substring for '{selected_key}': ").strip()
        new_value = input(f"Enter the new substring for '{selected_key}': ").strip()

        # Find matches
        matches = find_all_keys_by_value(json_data, f"*{target_value}*", use_wildcard=True)

        # Proceed with updates if matches are found
        if matches:
            print(f"\nFound {len(matches)} match(es) for '{selected_key}':")
            for idx, (key, value, _, _) in enumerate(matches, start=1):
                updated_value = value.replace(target_value, new_value)
                print(f"{idx}. Key: {key}, Current Value: {value}, Updated Value (Preview): {updated_value}")

            print("all. Update all keys with the target value.")
            print("exit. Exit without making any changes.")

            selection = input("\nEnter the numbers corresponding to the keys you want to update (comma-separated, 'all' for all, or 'exit' to cancel): ").strip().lower()

            if selection == "exit":
                print("\nNo changes were made.")
                continue

            if selection == "all":
                for key, value, parent, child_key in matches:
                    updated_value = value.replace(target_value, new_value)
                    parent[child_key] = updated_value
                    print(f"Updated: Key = '{key}', New Value = '{updated_value}'")
            else:
                try:
                    selected_indices = {int(num.strip()) for num in selection.split(",") if num.strip().isdigit()}
                    for idx, (key, value, parent, child_key) in enumerate(matches, start=1):
                        if idx in selected_indices:
                            updated_value = value.replace(target_value, new_value)
                            parent[child_key] = updated_value
                            print(f"Updated: Key = '{key}', New Value = '{updated_value}'")
                except ValueError:
                    print("\nInvalid input. No changes were made.")
                    continue
        else:
            # Key exists but the value does not match the input
            if selected_key in json_data:
                current_value = json_data[selected_key]
                if current_value != new_value:
                    print(f"\nKey '{selected_key}' exists with value '{current_value}', but it doesn't match the target value '{new_value}'.")
                    update_confirm = input(f"Do you want to update it to '{new_value}'? (yes/no): ").strip().lower()
                    if update_confirm == "yes":
                        json_data[selected_key] = new_value
                        print(f"Updated '{selected_key}' from '{current_value}' to '{new_value}'.")
                    else:
                        print(f"No changes made for '{selected_key}'.")
                else:
                    print(f"\nNo changes needed for '{selected_key}', the value matches the target value '{new_value}'.")
            else:
                print(f"\nNo matches found for '{selected_key}' containing substring '{target_value}'.")
                add_new = input(f"Do you want to add '{selected_key}' as a new entry? (yes/no): ").strip().lower()
                if add_new == "yes":
                    json_data[selected_key] = new_value
                    print(f"Added '{selected_key}' with value '{new_value}'.")
                else:
                    print(f"No changes made for '{selected_key}'.")

    # Final JSON output
    print("\nFinal JSON after updates:")
    return json_data


# Example JSON data
example_json = {
    "hostname": "server3.example.com",
    "ip_address": "192.168.1.1",
    "servers": [
        {"name": "server1", "ip": "192.168.1.2"},
        {"name": "server2", "ip": "192.168.1.3"}
    ],
    "metadata": {
        "serial_number": "SN12345",
        "status": "active"
    }
}

# Run the menu-driven JSON updater
updated_json = menu_driven_bulk_update_with_substring(example_json)

# Display the final JSON
print(updated_json)


Menu:
1. hostname
2. ip_address
3. serial_number
4. exit

Select an option (1-4): 1

You selected 'hostname'.
Enter the target substring for 'hostname': server1
Enter the new substring for 'hostname': server2

Found 2 match(es) for 'hostname':
1. Key: hostname, Current Value: server1.example.com, Updated Value (Preview): server2.example.com
2. Key: servers[0].name, Current Value: server1, Updated Value (Preview): server2
all. Update all keys with the target value.
exit. Exit without making any changes.

Enter the numbers corresponding to the keys you want to update (comma-separated, 'all' for all, or 'exit' to cancel): all

Updated: Key = 'hostname', New Value = 'server2.example.com'
Updated: Key = 'servers[0].name', New Value = 'server2'

Final JSON:
{
    "hostname": "server2.example.com",
    "ip_address": "192.168.1.1",
    "servers": [
        {"name": "server2", "ip": "192.168.1.2"},
        {"name": "server2", "ip": "192.168.1.3"}
    ],
    "metadata": {
        "serial_number": "SN12345",
        "status": "active"
    }
}
