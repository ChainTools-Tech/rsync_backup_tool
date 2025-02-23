import argparse
import logging


def command_line_parser():
    parser = argparse.ArgumentParser(
        prog="rsync_backup_tool",
        description="Automate rsync backups for multiple hosts.",
        epilog="...and Relayer is happy!",
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        type=str,
        required=True,
        dest="config",
        help="Path to the configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="1.0"
    )
    return parser.parse_args()