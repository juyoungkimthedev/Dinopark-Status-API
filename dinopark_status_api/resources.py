"""
API resource mapped to REST routes.

"""

# System imports
import logging
import requests

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


class StatusMaintenance(Resource):
    """
    End-point for providing the zone maintenance status in Dino Park for a given zone identifier.
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

    def get(self):
        """
        :return: A JSON response containing zone maintenance status for a given zone identifier.
        """
        # Parse query arguments
        args = self._parser.parse_args()
        query = dict(args)
        zone = query["zone"]

        # Retrieve logs from NUDLS monitoring system
        try:
            resp = requests.get(NUDLS_URL)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            self._logger.error(err)
            raise

        # Retrieve content from the logs
        resp_body = resp.json()

        # Check if maintenance is required. If the given zone is not in the logs, an error is returned.


        # Insert status result into MongoDB and return insert count
        insert_docs = self._collection.insert_many(resp_body)
        insert_count = len(insert_docs.inserted_ids)
        self._logger.error(f"Number of documents inserted: {insert_count}")

        # Final response body of the API - zone will be a partition key inside document DB
        result = {
            "zone": zone,
            "maintenance": "required",
        }

        self._logger.error(f"Processed maintenance status request for zone: {zone}")

        return make_response(jsonify(result))
