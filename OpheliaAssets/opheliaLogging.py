import logging

# Create a logger
logger = logging.getLogger("Ophelia")
logger.setLevel(logging.DEBUG)  # Logs everything from DEBUG and above

# Debug log (stores ALL messages)
debug_handler = logging.FileHandler("debug.log", mode="a")
debug_handler.setLevel(logging.DEBUG)  # Logs everything

# Security log (only stores warnings and above)
security_handler = logging.FileHandler("security.log", mode="a")
security_handler.setLevel(logging.WARNING)  # Logs WARNING, ERROR, CRITICAL

# Console log (optional, prints logs to terminal)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Only shows INFO and above in the console

# Define a consistent format for logs
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
debug_handler.setFormatter(formatter)
security_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(debug_handler)
logger.addHandler(security_handler)
logger.addHandler(console_handler)  # Prints logs to the console
