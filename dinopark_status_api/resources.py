"""
API resource mapped to REST routes.

"""

# System imports
import logging
import requests
from werkzeug.exceptions import ServiceUnavailable

# Third-party imports
from flask import make_response, jsonify
from flask_restful import Resource, reqparse

# Local imports
from dinopark_status_api.constants import LOGGER, NUDLS_URL


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

    def __init__(self, **kwargs):
        """
        Constructor.
        :param kwargs: key word args sent from the main API package.

        """
        # collection object passed from the main API package.
        self._collection = kwargs["collection"]
        self._logger = logging.getLogger(LOGGER)
        self._parser = reqparse.RequestParser()
        self._parser.add_argument("zone", type=str, help="Provide a zone number", location="args", required=True)

    # TODO: Remove all the logging.error() change to logging.info()
    def get(self):
        """
        :return: A JSON response containing zone status for a given zone identifier.
        """
        # Parse arguments
        args = self._parser.parse_args()
        query = dict(args)
        zone = query["zone"]

        # Retrieve records from NUDLS monitoring system
        # resp = requests.get(NUDLS_URL)
        # if resp.status_code != 200:
        #     # If NUDLS system is down, we want to return 503 error status
        #     raise ServiceUnavailable("NUDLS service is currently unavailable. Try again later.")
        # Retrieve JSON entries
        # resp_body = resp.json()

        try:
            resp = requests.get(NUDLS_URL)
            resp_body = resp.json()
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            self._logger.error(err)
            raise

        # Insert retrieved records into MongoDB and return insert count
        insert_docs = self._collection.insert_many(resp_body)
        insert_count = len(insert_docs.inserted_ids)
        self._logger.error(f"Number of documents inserted: {insert_count}")

        # Final response body of the API
        result = {
            "zone": zone,
            "maintenance": "required",
            "safety": "safe"
        }
        self._logger.error(f"Processed request for zone: {zone}")

        return make_response(jsonify(result))
