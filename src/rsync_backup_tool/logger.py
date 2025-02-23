import logging
import os
from typing import Dict, Any

from rsync_backup_tool.utils import ensure_directory


def initialize_loggers(config: Dict[str, Any]):
    # Ensure log directory exists
    log_directory = ensure_directory(config.get("log_directory", "logs"))

    # Configure the main logger
    main_log_file = os.path.join(log_directory, "rsync_backup_tool.log")
    main_logger = logging.getLogger("rsync_backup_tool")
    main_logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(main_log_file, mode="w")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    )
    main_logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    )
    main_logger.addHandler(console_handler)