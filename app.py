"""
A REST API for Dino Park zone status.

"""

# System imports
import logging

# Local imports
from dinopark_status_api.constants import API_VERSION, LOGGER
from dinopark_status_api.apis import DinoParkStatusApi

# Setup logging
logger = logging.getLogger(LOGGER)
logger.info(f"Starting DinoPark Status API {API_VERSION}")

# Setup App
app = DinoParkStatusApi.create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
