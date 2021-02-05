"""
A REST API for Dino Park zone status.

"""

# System imports
import logging

# Local imports
from dinopark_status_api.constants import API_VERSION, LOGGER


# Setup logging
logger = logging.getLogger(LOGGER)
logger.info(f"Starting DinoPark Status API {API_VERSION}")

# Setup App
