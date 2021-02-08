"""
API resource mapped to REST routes.

"""

# System imports
import logging
import requests
import time
from datetime import datetime, timedelta
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

        # Retrieve dinosaur information and create look up dictionary for information
        dino_log = [i for i in content if i["kind"] == "dino_added"]

        # Species look up e.g. {"1032": "Tyrannosaurus rex"}
        dino_species = [{str(i["id"]): i["species"]} for i in dino_log]
        _dino_species = {}
        for i in dino_species:
            for k, v in i.items():
                _dino_species[k] = v

        # Type look up e.g. {"1032": "carnivore"}
        dino_type = [{str(i["id"]): i["herbivore"]} for i in dino_log]
        _dino_type = {}
        for i in dino_type:
            for k, v in i.items():
                if v is False:
                    _dino_type[k] = "carnivore"
                else:
                    _dino_type[k] = "herbivore"

        # Digestion time (in days) look up e.g. {"1032": 2}
        dino_dt = [{str(i["id"]): i["digestion_period_in_hours"]} for i in dino_log]
        _dino_dt = {}
        for i in dino_dt:
            for k, v in i.items():
                _dino_dt[k] = int(v / 24)  # convert to days

        # Removal of dinosaur with date e.g. {"1047": "2021-02-05T22:59:31.696Z"}
        dino_rm_log = [i for i in content if i["kind"] == "dino_removed"]
        dino_rm = [{str(i["dinosaur_id"]): i["time"]} for i in dino_rm_log]
        _dino_rm = {}
        for i in dino_rm:
            for k, v in i.items():
                _dino_rm[k] = v

        # Feeding date of dinosaur e.g. {"1032": "2021-02-03T22:59:31.696Z"}
        dino_fed_log = [i for i in content if i["kind"] == "dino_fed"]
        dino_fed = [{str(i["dinosaur_id"]): i["time"]} for i in dino_fed_log]
        _dino_fed = {}
        for i in dino_fed:
            for k, v in i.items():
                _dino_fed[k] = v

        # Retrieve location update information
        dino_loc_update = [i for i in content if i["kind"] == "dino_location_updated"]
        # Check if zone exists in the logs
        locations = [entry["location"] for entry in dino_loc_update]
        if zone not in locations:
            raise BadRequest(f"Zone: {zone} is not available from NUDLS logs currently.")

        # Filter entry by provided zone
        filtered_item = [i for i in dino_loc_update if i["location"] == zone][0]

        # Retrieve dinosaur id of the given dinosaur location updated zone
        dino = str(filtered_item["dinosaur_id"])
        result = self._safety_status_algorithm(filtered_item, zone, dino, _dino_species, _dino_type, _dino_dt, _dino_rm, _dino_fed)

        # Insert status result into MongoDB and return insert count
        insert_docs = self._collection.insert_many([result])
        insert_count = len(insert_docs.inserted_ids)
        self._logger.error(f"Number of documents inserted: {insert_count}")

        self._logger.error(f"Processed safety status request for zone: {zone}")

        # Delete _id key from the final response after insertion into MongoDB
        result.pop("_id")

        return make_response(jsonify(result))

    def _safety_status_algorithm(self, zone_item, zone, dino_id, dino_species, dino_type, dino_digestion_time, dino_remove, dino_fed):
        """
        A Helper method to process logs using safety status algorithm.

        :param zone_item: Dictionary of information of dino location update for a given zone.
        :param zone: Given zone identifier.
        :param dino_id: Dinosaur's unique ID.
        :param dino_species: Species look up dictionary.
        :param dino_type: Type look up dictionary.
        :param dino_digestion_time: Digestion time look up dictionary.
        :param dino_remove: Removal look up dictionary.
        :param dino_fed: Fed time look up dictionary.
        :return: Dictionary of safety status result.
        """

        # Check if dino is herbivore or carnivore
        if dino_type[dino_id] == "herbivore":
            result = {
                "zone": zone,
                "safety_status": 1,
                "info": f"It is safe to enter. Currently {dino_species[dino_id]} ({dino_type[dino_id]}) is in the zone."
            }
            return result

        # Now dino is carnivore. Check if dinosaur was removed.
        if dino_id in dino_remove.keys():
            removal_date = datetime.strptime(dino_remove[dino_id], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            update_date = datetime.strptime(zone_item["time"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            if removal_date > update_date:
                self._logger.info(f"{dino_id} was removed after its location was updated")
                result = {
                    "zone": zone,
                    "safety_status": 1,
                    "info": f"It is safe to enter. {dino_species[dino_id]} - ({dino_type[dino_id]}) was removed."
                }
                return result
        else:
            self._logger.info(f"{dino_id} was not removed.")

        # Check if dinosaur was fed
        if dino_id not in dino_fed.keys():
            result = {
                "zone": zone,
                "safety_status": 0,
                "info": f"{dino_id} - ({dino_type[dino_id]}) was not fed. It is not safe to enter."
            }
            return result

        # If dino was fed, check if fed time + digestion time is bigger than today or not
        else:
            # Convert fed time to datetime object
            fed_date = datetime.strptime(dino_fed[dino_id], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            fed_date = datetime.strptime(fed_date, "%Y-%m-%d")
            today = datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
            # Sum of fed date and digestion time
            sum_fed_digest_date = fed_date + timedelta(days=dino_digestion_time[dino_id])

            if sum_fed_digest_date < today:
                result = {
                    "zone": zone,
                    "safety_status": 0,
                    "info": f"It is not safe to enter. Currently {dino_species[dino_id]} has finished digesting."
                }
                return result
            elif sum_fed_digest_date >= today:
                result = {
                    "zone": zone,
                    "safety_status": 1,
                    "info": f"It is safe to enter. Currently {dino_species[dino_id]} is still digesting."
                }
                return result
