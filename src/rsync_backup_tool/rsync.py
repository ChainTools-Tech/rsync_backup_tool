import subprocess
import os
import logging
from typing import Dict, Any, List

from rsync_backup_tool.utils import generate_timestamp


logger = logging.getLogger(__name__)


class RsyncBackupTool:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def run(self):
        base_destination = self.config["destination"]
        timestamp = generate_timestamp()
        destination = f"{base_destination}/{timestamp}"

        # Create the base destination directory if it doesn't exist
        os.makedirs(destination, exist_ok=True)

        common_folders = self.config["common_folders"]

        # Iterate through all hosts
        for host, details in self.config.get("hosts", {}).items():
            logger.info(f"Processing host: {host}")
            specific_folders = details.get("specific_folders", [])

            # Combine common and host-specific folders
            all_folders = common_folders + specific_folders

            # Sync each folder individually
            for folder in all_folders:
                self.rsync_pull(host, folder, destination)

    def rsync_pull(self, host: str, folder: Dict[str, Any], destination: str):
        path = folder["path"]
        pull_entire_folder = folder.get("pull_entire_folder", False)
        logger.debug(f"Pulling files/folders.", extra={"path": path, "pull_entire_folder": pull_entire_folder})

        # Check if the folder exists on the remote server
        check_command = [
            "ssh", host,
            f"test -d {path} && echo exists || echo not_exists"
        ]
        result = subprocess.run(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0 or result.stdout.decode().strip() != "exists":
            logger.warning(f"Skipping {host}:{path} (does not exist or cannot access)")
            return

        # Construct the source path
        if pull_entire_folder:
            source = f"{host}:{path}/"  # Include trailing slash for entire folder
        else:
            source = f"{host}:{path}/*"  # No trailing slash for files only

        # Construct the destination path
        dest_path = f"{destination}/{host}{path}"
        logger.debug(f"Copying {host}:{path} to {dest_path}")

        # Create the destination directory if it doesn't exist
        os.makedirs(dest_path, exist_ok=True)

        # Construct the rsync command
        command = [
            "rsync", "-avz", "--progress", "-e", "ssh",
            "--rsync-path", "sudo rsync",
            "--partial", "--timeout=60",  # Handle interruptions gracefully
            source, dest_path
        ]

        logger.info(f"Synchronizing {host}:{path}")
        logger.debug(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, stderr=subprocess.PIPE)

        # Check for errors
        if result.returncode != 0:
            logger.error(f"Error occurred while syncing {host}:{path}:")
            logger.error(result.stderr.decode())