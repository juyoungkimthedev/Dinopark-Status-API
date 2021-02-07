"""
API resource mapped to REST routes.

"""

# System imports
import logging
import requests
import time
from datetime import datetime
from werkzeug.exceptions import BadRequest

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

    The NUDLS endpoint returns maintenance performed date. This endpoint will calculate the difference between
    today's date (when the API was called) and the retrieved maintenance date to decide whether maintenance is required or not.

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

        # Retrieve content of the logs
        content = resp.json()

        # Retrieve maintenance performed date by filtering logs
        maintenance_log = [entry for entry in content if entry["kind"] == "maintenance_performed"]

        # Check if zone exists in the logs
        locations = [entry["location"] for entry in maintenance_log]
        if zone not in locations:
            raise BadRequest(f"Zone: {zone} is not available from NUDLS logs currently.")

        # Filter document by given zone location
        filter_by_zone = [entry for entry in maintenance_log if entry["location"] == zone][0]

        # Retrieve today's date and maintenance date
        today = time.strftime("%Y-%m-%d")
        maintenance_date = filter_by_zone["time"]
        maintenance_date = datetime.strptime(maintenance_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")

        # Convert to datetime object
        date_obj_1 = datetime.strptime(today, "%Y-%m-%d")
        date_obj_2 = datetime.strptime(maintenance_date, "%Y-%m-%d")

        # Calculate the difference in days
        date_diff = (date_obj_1 - date_obj_2).days

        # Decide whether maintenance is required or not
        if date_diff < 30:
            maintenance_status = f"Maintenance is not required. Currently {date_diff} days after last maintenance performed."
            maintenance_required = 0
        elif date_diff == 30:
            maintenance_status = f"Maintenance is not required, but maintenance will be required from tomorrow."
            maintenance_required = 0
        else:
            maintenance_status = f"Maintenance is required. Currently {date_diff} days after last maintenance performed."
            maintenance_required = 1

        # Final response body of the API - zone will be a partition key inside document DB
        result = {
            "zone": zone,
            "maintenance_required": maintenance_required,
            "info": maintenance_status
        }

        # Insert status result into MongoDB and return insert count
        insert_docs = self._collection.insert_many([result])
        insert_count = len(insert_docs.inserted_ids)
        self._logger.error(f"Number of documents inserted: {insert_count}")

        self._logger.error(f"Processed maintenance status request for zone: {zone}")

        # Delete _id key from the final response after insertion into MongoDB
        result.pop("_id")

        return make_response(jsonify(result))


class StatusSafety(Resource):
    """
    End-point for providing the zone safety status in Dino Park for a given zone identifier.

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
        :return: A JSON response containing zone safety status for a given zone identifier.
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

        # Retrieve content of the logs
        content = resp.json()

        # Retrieve maintenance performed date by filtering logs
        maintenance_log = [entry for entry in content if entry["kind"] == "maintenance_performed"]

        # Check if zone exists in the logs
        locations = [entry["location"] for entry in maintenance_log]
        if zone not in locations:
            raise BadRequest(f"Zone: {zone} is not available from NUDLS logs currently.")

        # Final response body of the API - zone will be a partition key inside document DB
        result = {
            "zone": zone,
            "maintenance_required": maintenance_required,
            "info": maintenance_status
        }

        # Insert status result into MongoDB and return insert count
        insert_docs = self._collection.insert_many([result])
        insert_count = len(insert_docs.inserted_ids)
        self._logger.error(f"Number of documents inserted: {insert_count}")

        self._logger.error(f"Processed safety status request for zone: {zone}")

        # Delete _id key from the final response after insertion into MongoDB
        result.pop("_id")

        return make_response(jsonify(result))
