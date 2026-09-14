
import random
import string

def solve(s):
    """
    Helper function to calculate the expected output for the test cases.
    """
    if not s:
        return ""
    
    compressed = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            compressed.append(s[i-1] + str(count))
            count = 1
    
    # Append the last group
    compressed.append(s[-1] + str(count))
    
    compressed_str = "".join(compressed)
    
    # Return compressed only if it is strictly shorter than original
    return compressed_str if len(compressed_str) < len(s) else s

def generate():
    """
    Generates a random test case for the compress_string function.
    Ensures diversity by picking from different string patterns.
    """
    # Define different scenarios to ensure data diversity
    scenarios = [
        "empty",            # Empty string
        "no_repeats",       # No consecutive characters (compressed will be longer)
        "all_repeats",      # One character repeated many times (compressed will be shorter)
        "mixed_short",      # Short string with some repeats
        "mixed_long",       # Long string with various repeat lengths
        "boundary_equal",   # Compressed length equals original length (e.g., "aabb")
        "alphanumeric",     # Mix of letters and numbers
        "extreme_long"      # String near the constraint limit (10^5)
    ]
    
    scenario = random.choice(scenarios)
    chars = string.ascii_letters + string.digits
    
    if scenario == "empty":
        s = ""
    
    elif scenario == "no_repeats":
        length = random.randint(1, 100)
        # Sample unique characters to ensure no repeats
        s = "".join(random.sample(chars * 10, length)) 
        # To be safe, we ensure no two adjacent are same
        res = []
        for i in range(length):
            char = random.choice(chars)
            while res and res[-1] == char:
                char = random.choice(chars)
            res.append(char)
        s = "".join(res)
        
    elif scenario == "all_repeats":
        char = random.choice(chars)
        length = random.randint(2, 1000)
        s = char * length
        
    elif scenario == "mixed_short":
        length = random.randint(1, 20)
        s = "".join(random.choices(chars, k=length))
        
    elif scenario == "mixed_long":
        length = random.randint(100, 5000)
        # Create chunks of repeated characters
        s_list = []
        while len("".join(s_list)) < length:
            char = random.choice(chars)
            count = random.randint(1, 10)
            s_list.append(char * count)
        s = "".join(s_list)[:length]
        
    elif scenario == "boundary_equal":
        # "aabb" -> "a2b2" (Length 4 == 4)
        # We generate pairs of characters
        num_pairs = random.randint(1, 10)
        s = "".join(random.choice(chars) * 2 for _ in range(num_pairs))
        
    elif scenario == "alphanumeric":
        length = random.randint(10, 100)
        s = "".join(random.choices(chars, k=length))
        
    elif scenario == "extreme_long":
        length = random.randint(50000, 100000)
        # Mix of long runs and single chars to test O(n)
        s_list = []
        while len("".join(s_list)) < length:
            if random.random() > 0.5:
                s_list.append(random.choice(chars) * random.randint(10, 100))
            else:
                s_list.append(random.choice(chars))
        s = "".join(s_list)[:length]

    return {"input": [s], "output": solve(s)}
