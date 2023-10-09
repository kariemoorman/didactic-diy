import random
import string


def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_digits=True, use_special_chars=True):
    # Define character sets based on user preferences
    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation
    characters += ' '  # add space
    # Check if at least one character set is selected
    if not characters:
        raise ValueError("At least one character set must be selected")
    # Generate the password
    password = ''.join(random.choice(characters) for _ in range(length))
    print("Generated Password:", password)
    return password

# Example usage:
#generate_password(length=22, use_uppercase=True, use_lowercase=True, use_digits=True, use_special_chars=True)

