import logging


def configure_file_handler(log_file, level):
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    return handler


# Logger for the app
logger = logging.getLogger("render-api")
logger.setLevel(logging.DEBUG)

# Add handlers with specific log level
logger.addHandler(configure_file_handler("debug.log", logging.DEBUG))
logger.addHandler(configure_file_handler("info.log", logging.INFO))
logger.addHandler(configure_file_handler("warning.log", logging.WARNING))
logger.addHandler(configure_file_handler("error.log", logging.ERROR))
logger.addHandler(configure_file_handler("critical.log", logging.CRITICAL))

# Optional handler for console logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)
