"""Internet connectivity check."""

import socket

from udm.logger import logger


def check_internet(host: str = "8.8.8.8", port: int = 53, timeout: int = 5) -> bool:
    """Return True if there is an active internet connection."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            pass
        logger.info("Internet connection verified.")
        return True
    except OSError:
        logger.warning("No internet connection detected.")
        return False
