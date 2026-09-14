
def compress_string(s):
    """
    Compresses a string by replacing consecutive repeating characters 
    with the character followed by the count of repetitions.
    Returns the compressed string only if it is strictly shorter than the original.
    """
    if not s:
        return ""

    compressed = []
    count = 1
    
    # Iterate through the string starting from the second character
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            # Append the previous character and its count
            compressed.append(s[i - 1])
            compressed.append(str(count))
            count = 1
            
    # Append the last character and its count
    compressed.append(s[-1])
    compressed.append(str(count))
    
    # Join the list into a final string
    result = "".join(compressed)
    
    # Return the compressed version only if it's strictly shorter
    return result if len(result) < len(s) else s

def solve(s):
    """
    Entry function to solve the Smart String Compressor problem.
    """
    return compress_string(s)

# Example usage:
# print(solve("aaabbcccc")) # Output: "a3b2c4"
# print(solve("abcd"))      # Output: "abcd"
# print(solve("aabb"))      # Output: "aabb"
# print(solve(""))          # Output: ""
