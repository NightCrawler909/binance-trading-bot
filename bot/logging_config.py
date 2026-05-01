import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger with the given name.
    Logs to both console (WARNING+) and a rotating file handler (DEBUG+).
    """
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, return it immediately to avoid duplicate messages.
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.DEBUG)
    
    # Ensure logs directory exists structure-wise safely
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "trading_bot.log")
    
    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    
    # Console Handler for warning and critical messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    
    # File Handler (Rotating, Max 5MB, keeps up to 3 backups)
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Prevent logger from propagating to root naturally to avoid dupes across Typer
    logger.propagate = False
    
    return logger
