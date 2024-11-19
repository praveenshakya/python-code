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
