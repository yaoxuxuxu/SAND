
import random
import string

def generate():
    """
    Generates a random test case for the flatten_dict function.
    Returns a dictionary containing the input parameters and the expected output.
    """

    def get_random_string(length=5):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def create_random_dict(depth, max_width=3):
        """
        Recursively creates a random nested dictionary.
        """
        # Base case: if depth is 0, return a leaf value
        if depth == 0:
            return random.choice([
                get_random_string(), 
                random.randint(0, 1000), 
                round(random.uniform(0, 1000), 2)
            ])

        # Randomly decide how many keys this level has
        num_keys = random.randint(1, max_width)
        res = {}
        for _ in range(num_keys):
            key = get_random_string()
            
            # Decide the type of value for this key
            # 0: Leaf value, 1: Nested dict, 2: Empty dict
            choice = random.choices([0, 1, 2], weights=[0.5, 0.3, 0.2])[0]
            
            if choice == 0:
                res[key] = random.choice([get_random_string(), random.randint(0, 1000), round(random.uniform(0, 1000), 2)])
            elif choice == 1:
                res[key] = create_random_dict(depth - 1, max_width)
            else:
                res[key] = {}
        return res

    def reference_flatten(d, parent_key=''):
        """
        Reference implementation to generate the expected output.
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict) and v: # If it's a non-empty dictionary
                items.extend(reference_flatten(v, new_key).items())
            else:
                # If it's a leaf or an empty dictionary
                items.append((new_key, v))
        return dict(items)

    # Configuration for randomness
    MAX_DEPTH = random.randint(1, 5)
    MAX_WIDTH = random.randint(2, 4)
    
    # Generate random input dictionary
    test_input_dict = create_random_dict(MAX_DEPTH, MAX_WIDTH)
    
    # Generate expected output using reference implementation
    expected_output = reference_flatten(test_input_dict)

    return {
        "input": [test_input_dict], 
        "output": expected_output
    }

# Example of usage:
# print(generate())
