def update_all_keys_by_value(json_data: dict, target_value, new_value) -> dict:
    """
    Updates all occurrences of a specific value in a JSON object.

    Args:
        json_data (dict): The JSON object to update.
        target_value: The value to search for and replace.
        new_value: The new value to set.

    Returns:
        dict: The updated JSON object.
    """
    def search_and_update(json_obj):
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                if value == target_value:
                    json_obj[key] = new_value
                elif isinstance(value, (dict, list)):
                    search_and_update(value)
        elif isinstance(json_obj, list):
            for index, item in enumerate(json_obj):
                if item == target_value:
                    json_obj[index] = new_value
                elif isinstance(item, (dict, list)):
                    search_and_update(item)

    search_and_update(json_data)
    return json_data

# Update the JSON
updated_json = update_all_keys_by_value(json_data, "192.168.1.1", "10.0.0.1")
print("Updated JSON:", updated_json)
