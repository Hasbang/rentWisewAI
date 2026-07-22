import json
import os


def load_properties():
    """
     Reads the properties.json file and returns a list of property dictionaries.
    
    Returns:
        list: A list of property records, or an empty list if the file is missing.
    """

    # Build the path relative to this file's location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'properties.json')

    try:
        with open(file_path, 'r') as f:
            properties = json.load(f)
            return properties
        

    except FileNotFoundError:
        print(f"ERROR: Could not find properties file at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from {file_path}")
        return []