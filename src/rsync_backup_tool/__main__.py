from rsync_backup_tool.cli import command_line_parser
from rsync_backup_tool.config import load_config
from rsync_backup_tool.logger import initialize_loggers
from rsync_backup_tool.rsync import RsyncBackupTool


def main():
    # Parse command-line arguments
    cmdargs = command_line_parser()

    # Load the configuration
    config = load_config(cmdargs.config)

    # Set up logging
    initialize_loggers(config)

    # Run the backup tool
    backup_tool = RsyncBackupTool(config)
    backup_tool.run()


if __name__ == "__main__":
    main()