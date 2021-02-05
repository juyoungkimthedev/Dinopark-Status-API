"""
API resource mapped to REST routes.

"""

# System imports
import logging

# Third-party imports
import pandas
from flask import request, make_response, jsonify
from flask_restful import Resource
from werkzeug.exceptions import NotFound

# Local imports
from dinopark_status_api.constants import LOGGER


class Health(Resource):
    """
    The health check endpoint.
    """
    def get(self):
        """
        :return: The response containing status of API.
        """
        return make_response(jsonify({
            "status": {
                "code": 200,
                "info": "Welcome to Dino Park Status API!",
                "status": "SUCCESS",
            }
        }))


class Status(Resource):
    """
    End-point for providing the zone status in Dino Park for a given zone identifier.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.logger = logging.getLogger(LOGGER)

    def get(self):
        """
        :return: A JSON response containing zone status for a given zone identifier.
        """
        zone = "A1"
        result = {
            "maintenance": "required",
            "safety": "safe"
        }
        self.logger.info(f"Processed request for zone: {zone}")

        return make_response(jsonify(result))
