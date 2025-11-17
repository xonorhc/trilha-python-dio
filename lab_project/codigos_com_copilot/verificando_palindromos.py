# Ask the user for a word
word = input("Enter a word: ")

# Convert to lowercase to make the comparison case-insensitive
word_lower = word.lower()

# Reverse the word
reversed_word = word_lower[::-1]

# Check if the word is a palindrome
if word_lower == reversed_word:
    print("The word is a palindrome.")
else:
    print("The word is not a palindrome.")
