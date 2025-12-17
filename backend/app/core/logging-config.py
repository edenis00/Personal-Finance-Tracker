# backend/app/core/logging-config.py
import logging
import sys
from pathlib import Path


def setup_logging():
    """
    Docstring for setup_logging
    """

    # create log directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # logging config
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Set specific log levels for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    return logging.getLogger(__name__)
