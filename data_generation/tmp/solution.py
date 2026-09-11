
def fib(n: int) -> int:
    """
    Calculates the n-th Fibonacci number using an iterative approach.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    # Handle edge cases for n = 0 and n = 1
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Initialize the first two numbers of the sequence
    # a represents F(i-2), b represents F(i-1)
    a, b = 0, 1
    
    # Iterate from 2 up to n to calculate the sequence
    for _ in range(2, n + 1):
        # Update a and b:
        # The new b is the sum of the previous two (F(n) = F(n-1) + F(n-2))
        # The new a becomes the previous b
        a, b = b, a + b
        
    return b

def solve(n: int) -> int:
    """
    Entry point function to return the result of the Fibonacci calculation.
    """
    result = fib(n)
    return result

# Example usage:
# print(solve(0))   # Output: 0
# print(solve(1))   # Output: 1
# print(solve(6))   # Output: 8
# print(solve(10))  # Output: 55
