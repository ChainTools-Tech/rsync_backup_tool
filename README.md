# Rsync Backup Tool

The **Rsync Backup Tool** is a Python-based utility designed to automate `rsync` backups for multiple hosts. It allows you to define a configuration file (`config.yaml`) that specifies the hosts, folders to back up, and other settings. The tool will then synchronize the specified folders from the remote hosts to a local destination directory.

## Features

- **Multi-host support**: Backup folders from multiple remote hosts in a single run.
- **Common and host-specific folders**: Define folders that are common across all hosts and folders specific to individual hosts.
- **Logging**: Detailed logging for debugging and monitoring.
- **Flexible configuration**: Customize backup behavior via a YAML configuration file.
- **Timestamped backups**: Each backup run creates a timestamped directory to avoid overwriting previous backups.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/rsync_backup_tool.git
   cd rsync_backup_tool
   ```

### Install dependencies
The tool requires Python 3.7+ and the PyYAML package. Install the dependencies using:

```bash
pip install pyyaml
```

### Ensure rsync and ssh are installed
The tool relies on rsync and ssh for file synchronization. Make sure they are installed on your system:

```bash
sudo apt-get install rsync openssh-client
```

## Configuration
The tool uses a YAML configuration file (config.yaml) to define the backup settings. Below is an example configuration:

```yaml
destination: /path/to/backup/destination
log_directory: .logs
log_file: rsync_backup_tool.log
log_level: INFO

common_folders:
  - path: /var/log
    pull_entire_folder: true
  - path: /etc
    pull_entire_folder: false

hosts:
  host1:
    specific_folders:
      - path: /home/user1
        pull_entire_folder: true
  host2:
    specific_folders:
      - path: /opt/app
        pull_entire_folder: false
```        

### Configuration Keys

- `destination`: The base directory where backups will be stored.
- `log_directory`: Directory for storing log files (default: .logs).
- `log_file`: Name of the log file (default: rsync_backup_tool.log).
- `log_level`: Logging level (e.g., INFO, DEBUG).
- `common_folders`: Folders to back up from all hosts.
- `path`: The path to the folder on the remote host.
- `pull_entire_folder`: If true, the entire folder is synced. If false, only files in the folder are synced (excluding subdirectories).
- `hosts`: Host-specific folders to back up.
- `specific_folders`: Folders specific to this host (same structure as common_folders).

## Usage
Run the tool:

```bash
python -m rsync_backup_tool --config /path/to/config.yaml
```

## Check the logs
Logs are stored in the directory specified by log_directory in the configuration file. The main log file is named rsync_backup_tool.log, and rsync output is logged to rsync.log.

## View the backups
Backups are stored in timestamped directories under the destination path specified in the configuration file.

## Example
Given the configuration above, the tool will:
Sync `/var/log` and `/etc` from both host1 and host2.

Sync `/home/user1` from host1 and `/opt/app` from host2.

Store the backups in `/path/to/backup/destination/YYYYMMDDHHMM/`.

## Contributing
Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

