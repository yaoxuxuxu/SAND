
def flatten_dict(data):
    """
    Helper function to recursively flatten a nested dictionary.
    """
    result = {}

    def recurse(current_dict, parent_key=''):
        for key, value in current_dict.items():
            # Construct the new key by appending the current key to the parent key
            new_key = f"{parent_key}.{key}" if parent_key else key
            
            # Check if the value is a dictionary and not empty
            if isinstance(value, dict) and value:
                # Recurse deeper into the dictionary
                recurse(value, new_key)
            else:
                # If it's a leaf node or an empty dictionary, add it to the result
                result[new_key] = value

    recurse(data)
    return result

def solve(data):
    """
    Entry point function to flatten the provided nested dictionary.
    """
    return flatten_dict(data)

# Example Usage:
if __name__ == "__main__":
    # Example 1
    input1 = {
        "user": {
            "name": "Alice",
            "address": {
                "city": "New York",
                "zip": "10001"
            }
        },
        "status": "active"
    }
    print(solve(input1)) 
    # Expected: {'user.name': 'Alice', 'user.address.city': 'New York', 'user.address.zip': '10001', 'status': 'active'}

    # Example 2
    input2 = {
        "settings": {
            "theme": "dark",
            "notifications": {}
        },
        "version": 1.2
    }
    print(solve(input2)) 
    # Expected: {'settings.theme': 'dark', 'settings.notifications': {}, 'version': 1.2}
