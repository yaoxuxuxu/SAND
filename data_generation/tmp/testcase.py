
import random
import string
import re
from collections import Counter

def solve(text, stop_words, k):
    """
    Reference implementation of generate_tags to produce the expected output.
    """
    # Case-insensitive: convert to lowercase
    text = text.lower()
    # Convert stop_words to lowercase set for O(1) lookup
    stop_set = {word.lower() for word in stop_words}
    
    # Split by whitespace
    raw_words = text.split()
    cleaned_words = []
    
    for word in raw_words:
        # Remove punctuation attached to words (keep only alphanumeric)
        # The prompt says "Punctuation attached to words should be removed"
        # We filter the string to keep only alphanumeric characters
        cleaned = "".join(char for char in word if char.isalnum())
        
        # Criteria: 
        # 1. Not in stop_words
        # 2. Length >= 4
        # 3. Alphanumeric (already ensured by the join above, but check if empty)
        if cleaned and cleaned not in stop_set and len(cleaned) >= 4:
            cleaned_words.append(cleaned)
            
    # Count frequencies
    counts = Counter(cleaned_words)
    
    # Sorting: Frequency DESC, then Alphabetical ASC
    # We use a tuple (-count, word) for sorting
    sorted_tags = sorted(counts.keys(), key=lambda w: (-counts[w], w))
    
    return sorted_tags[:k]

def generate():
    """
    Generates a random test case for the generate_tags function.
    """
    # Word pools for diversity
    common_words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]
    tech_words = ["python", "algorithm", "database", "interface", "compiler", "network", "security"]
    short_words = ["the", "a", "an", "is", "it", "of", "to", "in", "and", "or"]
    punctuation_marks = [".", ",", "!", "?", ";", ":", "(", ")", '"']

    # 1. Randomly decide the "theme" of the text
    pool = random.choice([common_words, tech_words, common_words + tech_words])
    
    # 2. Generate a random set of words to create frequency
    # We pick a few words to repeat multiple times
    num_unique_significant = random.randint(3, 10)
    significant_pool = random.sample(pool, min(num_unique_significant, len(pool)))
    
    text_tokens = []
    for word in significant_pool:
        # Repeat each significant word 1 to 5 times
        for _ in range(random.randint(1, 5)):
            text_tokens.append(word)
            
    # Add some noise (short words and stop words)
    for _ in range(random.randint(5, 15)):
        text_tokens.append(random.choice(short_words))
        
    random.shuffle(text_tokens)
    
    # 3. Add random punctuation and casing
    processed_text_list = []
    for token in text_tokens:
        # Randomly change case
        if random.random() > 0.5:
            token = token.upper()
        elif random.random() > 0.5:
            token = token.capitalize()
            
        # Randomly attach punctuation
        if random.random() > 0.6:
            token += random.choice(punctuation_marks)
        processed_text_list.append(token)
        
    text = " ".join(processed_text_list)
    
    # 4. Generate stop_words
    # Mix of short words and some randomly picked significant words
    stop_words = random.sample(short_words, random.randint(2, len(short_words)))
    if random.random() > 0.7 and significant_pool:
        stop_words.append(random.choice(significant_pool))
        
    # 5. Generate k
    # k can be smaller than, equal to, or larger than the number of valid tags
    k = random.randint(1, 15)
    
    # Calculate expected output using the reference solve function
    output = solve(text, stop_words, k)
    
    return {
        "input": [text, stop_words, k],
        "output": output
    }

# Example of running the generator
if __name__ == "__main__":
    for i in range(3):
        print(f"Test Case {i+1}:")
        print(generate())
        print("-" * 20)
