
import random

def reference_fib(n: int) -> int:
    """
    Reference implementation to calculate the ground truth for the test cases.
    Uses an iterative approach to handle n up to 10,000 efficiently.
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def generate():
    """
    Generates a random test case for the fib(n) function.
    Ensures diversity by sampling from different ranges:
    - Edge cases (0, 1)
    - Small values (2-20)
    - Medium values (21-500)
    - Large values (501-10,000)
    """
    # Define categories to ensure diversity in the test suite
    categories = [
        ("edge", [0, 1]),
        ("small", (2, 20)),
        ("medium", (21, 500)),
        ("large", (501, 10000))
    ]
    
    # Randomly pick a category
    category_type, range_val = random.choice(categories)
    
    if isinstance(range_val, list):
        # Pick from a specific list of edge cases
        n = random.choice(range_val)
    else:
        # Pick a random integer within the range
        n = random.randint(range_val[0], range_val[1])
    
    return {
        "input": [n],
        "output": reference_fib(n)
    }

# Example of usage:
# for _ in range(5):
#     print(generate())
