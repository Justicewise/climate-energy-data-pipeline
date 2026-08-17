import logging
import os

def setup_logger(name, log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if this is called multiple times
    if not logger.handlers:
        # Console output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File output
        file_handler = logging.FileHandler(f"{log_dir}/pipeline.log")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger