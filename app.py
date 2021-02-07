"""
A REST API for Dino Park zone status.

"""

# System imports
import logging

# Third-party imports
import pymongo

# Local imports
from dinopark_status_api.constants import API_VERSION, LOGGER
from dinopark_status_api.apis import DinoparkStatusApi
from dinopark_status_api.json_encoder import MongoJsonEncoder

# Setup logging
logger = logging.getLogger(LOGGER)
logger.info(f"Starting DinoPark Status API {API_VERSION}")

# Setup MongoDB as a persistent layer
# The main app service is in a different container than mongodb container
# from docker point of view it's under different ip, just use service name specified in docker-compose as the hostname
# i.e. mongodb://<MONGO_DB_IP_ADDRESS>/<PORT>/
MONGO_URL = "mongodb://mongodb:27017/"
mongo_dal = pymongo.MongoClient(MONGO_URL)

# Setup App
app = DinoparkStatusApi.create_app(data_access_layer=mongo_dal)
app.json_encoder = MongoJsonEncoder

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)  # TODO: remember to set debug=False before completing!
