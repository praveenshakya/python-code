def json_update_menu(json_data: dict) -> dict:
    """
    Menu-driven function to update specific keys in a JSON object.
    Allows the user to select a key (hostname, ip_address, serial_number),
    checks if the key exists, and either updates or adds it.

    Args:
        json_data (dict): The JSON object to update.

    Returns:
        dict: The updated JSON object.
    """
    # Define menu options
    options = {
        "1": "hostname",
        "2": "ip_address",
        "3": "serial_number",
        "4": "exit"
    }

    while True:
        # Display menu to the user
        print("\nMenu:")
        for key, value in options.items():
            print(f"{key}. {value}")

        # Get user choice
        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "4" or options.get(choice) == "exit":
            print("\nExiting the updater. No further changes made.")
            break

        # Check for valid selection
        selected_key = options.get(choice)
        if not selected_key:
            print("\nInvalid choice. Please select a valid option.")
            continue

        # Find existing key and value
        print(f"\nYou selected '{selected_key}'.")

        # Search for the selected key in the JSON
        existing_value = json_data.get(selected_key)
        if existing_value is not None:
            print(f"Existing {selected_key}: {existing_value}")
            new_value = input(f"Enter the new value for '{selected_key}': ").strip()
            json_data[selected_key] = new_value
            print(f"Updated '{selected_key}' to '{new_value}'.")
        else:
            print(f"'{selected_key}' does not exist in the JSON.")
            add_new = input(f"Do you want to add a new '{selected_key}'? (yes/no): ").strip().lower()
            if add_new == "yes":
                new_value = input(f"Enter the value for new '{selected_key}': ").strip()
                json_data[selected_key] = new_value
                print(f"Added '{selected_key}' with value '{new_value}'.")
            else:
                print(f"No changes made for '{selected_key}'.")

    # Display final JSON
    print("\nFinal JSON:")
    return json_data


# Example JSON data
json_data = {
    "hostname": "server1",
    "ip_address": "192.168.1.1",
    "os": "Linux"
}

# Run the menu-driven updater
updated_json = json_update_menu(json_data)

# Display final JSON
print(updated_json)
