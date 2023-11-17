import logging

# Create a logger object for your application
logger = logging.getLogger("render-api")

# Set the global logging level (can be adjusted as needed)
logging.basicConfig(level=logging.DEBUG)

# Configure a file handler to log DEBUG-level logs to a debug.log file
debug_file_handler = logging.FileHandler("debug.log")
debug_file_handler.setLevel(logging.DEBUG)

# Create a formatter to customize the log message format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
debug_file_handler.setFormatter(formatter)

# Add the file handler to the logger for DEBUG-level messages
logger.addHandler(debug_file_handler)

# Configure a file handler to log INFO-level logs to an info.log file
info_file_handler = logging.FileHandler("info.log")
info_file_handler.setLevel(logging.INFO)

# Add the formatter to the file handler
info_file_handler.setFormatter(formatter)

# Add the file handler to the logger for INFO-level messages
logger.addHandler(info_file_handler)

# Configure a file handler to log WARNING-level logs to a warning.log file
warning_file_handler = logging.FileHandler("warning.log")
warning_file_handler.setLevel(logging.WARNING)

# Add the formatter to the file handler
warning_file_handler.setFormatter(formatter)

# Add the file handler to the logger for WARNING-level messages
logger.addHandler(warning_file_handler)

# Configure a file handler to log ERROR-level logs to an error.log file
error_file_handler = logging.FileHandler("error.log")
error_file_handler.setLevel(logging.ERROR)

# Add the formatter to the file handler
error_file_handler.setFormatter(formatter)

# Add the file handler to the logger for ERROR-level messages
logger.addHandler(error_file_handler)

# Configure a file handler to log CRITICAL-level logs to a critical.log file
critical_file_handler = logging.FileHandler("critical.log")
critical_file_handler.setLevel(logging.CRITICAL)

# Add the formatter to the file handler
critical_file_handler.setFormatter(formatter)

# Add the file handler to the logger for CRITICAL-level messages
logger.addHandler(critical_file_handler)
