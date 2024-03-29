import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import request

class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    def rotation_filename(self, default_name):
        directory, basename = os.path.split(default_name)
        name, ext = os.path.splitext(basename)
        date_part = basename.split(".")[-1]
        new_filename = f"{name}.{date_part}{ext}"
        return os.path.join(directory, new_filename)


def configure_logging():
    logs_folder = 'logs'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    
    # Set up error logging with customized file naming
    error_log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_log_handler = MyTimedRotatingFileHandler(os.path.join(logs_folder, 'error.log'), when='midnight', interval=1, backupCount=10)
    error_log_handler.setFormatter(error_log_formatter)
    error_logger = logging.getLogger('werkzeug')
    error_logger.addHandler(error_log_handler)
    error_logger.setLevel(logging.ERROR)
    
    # Set up access logging with customized file naming
    access_log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    access_log_handler = MyTimedRotatingFileHandler(os.path.join(logs_folder, 'access.log'), when='midnight', interval=1, backupCount=30)
    access_log_handler.setFormatter(access_log_formatter)
    access_logger = logging.getLogger('access_log')
    access_logger.addHandler(access_log_handler)
    access_logger.setLevel(logging.INFO)

def log_request():
    """Log request details."""
    client_ip = request.remote_addr
    request_line = f"{request.method} {request.full_path}"
    logger = logging.getLogger('access_log')
    logger.info(f"Request from {client_ip}: {request_line}")
