import re
import random
from collections import defaultdict, Counter
from typing import Dict

class TextGenerator:
    def __init__(self, text: str):
        """
        Initialize the TextGenerator with the input text.
        
        Args:
            text (str): The input text to analyze
        """
        self.text = self._preprocess_text(text)
        self.words = self.text.split()
        self.char_ngrams = {2: None, 3: None, 4: None}
        self.word_bigrams = None
        
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess the text by converting to lowercase, removing accents,
        punctuation, and extra whitespace.
        
        Args:
            text (str): Input text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove accents and special characters
        text = (
            text.replace('á', 'a').replace('é', 'e')
                 .replace('í', 'i').replace('ó', 'o')
                 .replace('ú', 'u').replace('ü', 'u')
                 .replace('ñ', 'n')
        )
        
        # Remove punctuation and special characters, keep only letters and spaces
        text = re.sub(r'[^a-z\s]', '', text)
        
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def train_ngram_models(self):
        """Train n-gram models for n=2,3,4"""
        for n in self.char_ngrams.keys():
            self.char_ngrams[n] = self._build_ngram_model(n)
    
    def _build_ngram_model(self, n: int) -> Dict[str, Dict[str, float]]:
        """
        Build an n-gram model for the given n.
        
        Args:
            n (int): The size of the n-gram
            
        Returns:
            Dict[str, Dict[str, float]]: N-gram model with probabilities
        """
        ngrams = defaultdict(Counter)
        
        # For each position in the text (except the last n-1 characters)
        for i in range(len(self.text) - n + 1):
            # The current n-gram
            ngram = self.text[i:i+n-1]
            # The next character
            next_char = self.text[i+n-1]
            # Increment the count for this transition
            ngrams[ngram][next_char] += 1
        
        # Convert counts to probabilities
        ngram_model = {}
        for ngram, counter in ngrams.items():
            total = sum(counter.values())
            ngram_model[ngram] = {char: count/total for char, count in counter.items()}
            
        return ngram_model
    
    def train_word_bigram_model(self):
        """Train a word bigram model"""
        bigrams = defaultdict(Counter)
        
        for i in range(len(self.words) - 1):
            current_word = self.words[i]
            next_word = self.words[i+1]
            bigrams[current_word][next_word] += 1
        
        # Convert counts to probabilities
        self.word_bigrams = {}
        for word, counter in bigrams.items():
            total = sum(counter.values())
            self.word_bigrams[word] = {w: c/total for w, c in counter.items()}
    
    def generate_from_chars(self, start: str, length: int = 250) -> str:
        """
        Generate text using character-level n-grams
        
        Args:
            start (str): Starting string (must be 1-3 characters for n=2-4)
            length (int): Length of text to generate
            
        Returns:
            str: Generated text
        """
        # Determine the n-gram model to use based on start length
        n = len(start) + 1
        
        # If n is too large, use the largest available model and adjust start
        if n > 4:
            n = 4
            start = start[-(n-1):]  # Take last n-1 characters
        
        if n not in self.char_ngrams or not self.char_ngrams[n]:
            raise ValueError(f"No {n}-gram model trained. Call train_ngram_models() first.")
        
        current = start
        result = current
        
        for _ in range(length):
            if current not in self.char_ngrams[n]:
                # If we hit an unseen n-1 gram, pick a random one
                current = random.choice(list(self.char_ngrams[n].keys()))
            
            # Get probabilities for next character
            probs = self.char_ngrams[n][current]
            # Choose next character based on probabilities
            next_char = random.choices(
                list(probs.keys()),
                weights=list(probs.values())
            )[0]
            
            result += next_char
            # Update current n-1 gram (shift left and add new character)
            current = (current + next_char)[-(n-1):]
        
        return result
    
    def generate_from_words(self, start: str, length: int = 50) -> str:
        """
        Generate text using word-level bigrams
        
        Args:
            start (str): Starting word
            length (int): Number of words to generate
            
        Returns:
            str: Generated text
        """
        if not self.word_bigrams:
            raise ValueError("Word bigram model not trained. Call train_word_bigram_model() first.")
        
        current = start
        result = [current]
        
        for _ in range(length - 1):
            if current not in self.word_bigrams:
                # If we hit an unseen word, pick a random one
                current = random.choice(list(self.word_bigrams.keys()))
            
            # Get probabilities for next word
            probs = self.word_bigrams[current]
            # Choose next word based on probabilities
            next_word = random.choices(
                list(probs.keys()),
                weights=list(probs.values())
            )[0]
            
            result.append(next_word)
            current = next_word
        
        return ' '.join(result)

def main():
    # Read the book text
    with open('book.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Initialize and train the generator
    print("Training models...")
    generator = TextGenerator(text)
    generator.train_ngram_models()
    generator.train_word_bigram_model()
    
    print("\n=== Character-based Generation (2-grams) ===")
    print(generator.generate_from_chars("el", 250))
    
    print("\n=== Character-based Generation (3-grams) ===")
    print(generator.generate_from_chars("el_", 250))
    
    print("\n=== Character-based Generation (4-grams) ===")
    print(generator.generate_from_chars("el_p", 250))
    
    print("\n=== Word-based Generation ===")
    print(generator.generate_from_words("el_principito", 50))
    print("\n" + "="*50 + "\n")
    print(generator.generate_from_words("el_rey_hablo_con", 50))

if __name__ == "__main__":
    main()
