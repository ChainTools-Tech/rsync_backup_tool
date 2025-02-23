import yaml
import subprocess
import os
import tempfile
from datetime import datetime

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def rsync_pull(host, folder_config, destination):
    # Create a temporary file to store the list of folders
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        for folder in folder_config:
            path = folder['path']
            pull_entire_folder = folder.get('pull_entire_folder', False)

            # Check if the folder exists on the remote server
            check_command = [
                'ssh', host,
                f'test -d {path} && echo exists || echo not_exists'
            ]
            result = subprocess.run(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Debug output
            print(f"Checking {host}:{path}...")
            print(f"Command: {' '.join(check_command)}")
            print(f"Output: {result.stdout.decode().strip()}")
            print(f"Error: {result.stderr.decode().strip()}")

            if result.returncode != 0 or result.stdout.decode().strip() != 'exists':
                print(f"Skipping {host}:{path} (does not exist or cannot access)")
                continue

            # Write the folder to the temporary file
            if pull_entire_folder:
                temp_file.write(f"{path}/\n")  # Include trailing slash for entire folder
            else:
                temp_file.write(f"{path}\n")  # No trailing slash for files only

            # Construct the destination path
            dest_path = f"{destination}/{host}{path}"

            # Create the destination directory if it doesn't exist
            os.makedirs(dest_path, exist_ok=True)

        # Get the path to the temporary file
        temp_file_path = temp_file.name

    # Construct the rsync command
    command = [
        'rsync', '-avz', '--progress', '-e', 'ssh',
        '--rsync-path', 'sudo rsync',
        '--partial', '--timeout=60',  # Handle interruptions gracefully
        '--files-from', temp_file_path,  # Use the temporary file as the list of folders
        f"{host}:./",  # Source is the root of the remote server
        f"{destination}/{host}/"  # Destination is the host-specific folder
    ]

    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, stderr=subprocess.PIPE)

    # Check for errors
    if result.returncode != 0:
        print(f"Error occurred while syncing {host}:")
        print(result.stderr.decode())

    # Clean up the temporary file
    os.remove(temp_file_path)

def main():
    config = load_config('config.yaml')
    base_destination = config['destination']

    # Generate timestamp in YYYYMMDDHHMM format
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    destination = f"{base_destination}/{timestamp}"

    # Create the base destination directory if it doesn't exist
    os.makedirs(destination, exist_ok=True)

    common_folders = config['common_folders']

    # Iterate through all hosts
    for host, details in config.get('hosts', {}).items():
        print(f"Processing host: {host}")
        specific_folders = details.get('specific_folders', [])

        # Combine common and host-specific folders
        all_folders = common_folders + specific_folders

        # Sync all folders in one go
        rsync_pull(host, all_folders, destination)

if __name__ == "__main__":
    main()