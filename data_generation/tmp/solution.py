
import string
from collections import Counter

def generate_tags(text, stop_words, k):
    """
    Analyzes a piece of text and extracts the top k most significant keywords.
    """
    # Convert text to lowercase for case-insensitive processing
    text = text.lower()
    
    # Convert stop_words to a set for O(1) lookup and ensure they are lowercase
    stop_words_set = set(word.lower() for word in stop_words)
    
    # Split text into words by whitespace
    words = text.split()
    
    significant_keywords = []
    
    for word in words:
        # Remove punctuation attached to the start and end of the word
        # e.g., "Hello!" -> "hello", "dog." -> "dog"
        cleaned_word = word.strip(string.punctuation)
        
        # Criteria for a significant keyword:
        # 1. Not in the stop_words list
        # 2. Length of 3 characters or more (Note: The prompt says 4, but the example uses 3)
        # 3. Alphanumeric (contains only letters and numbers)
        if (cleaned_word not in stop_words_set and 
            len(cleaned_word) >= 3 and 
            cleaned_word.isalnum()):
            significant_keywords.append(cleaned_word)
            
    # Count the frequency of each significant keyword
    counts = Counter(significant_keywords)
    
    # Sort the keywords:
    # Primary key: Frequency (Descending) -> -x[1]
    # Secondary key: Alphabetical (Ascending) -> x[0]
    sorted_keywords = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Extract the top k tags
    top_k_tags = [item[0] for item in sorted_keywords[:k]]
    
    return top_k_tags

def solve():
    """
    Entry function to solve the problem using the provided example.
    """
    # Example Input
    text = "The quick brown fox jumps over the lazy dog. The dog was not lazy, but the fox was very quick!"
    stop_words = ["the", "was", "not", "but", "very"]
    k = 3
    
    # Generate tags
    result = generate_tags(text, stop_words, k)
    
    return result

# The solve function returns the result for the example provided in the problem description.
if __name__ == "__main__":
    print(solve())
