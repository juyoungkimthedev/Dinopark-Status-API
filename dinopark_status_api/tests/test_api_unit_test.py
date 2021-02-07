"""
Tests API main functionality.
"""

# System imports
import unittest
import mock
import time
from datetime import datetime
from unittest.mock import Mock, patch

# Third-party import
import pymongo
from requests.exceptions import HTTPError

# Local imports
from dinopark_status_api.constants import API_VERSION
from dinopark_status_api.apis import DinoparkStatusApi


class TestDinoparkStatusApi(unittest.TestCase):
    """
    Tests main functions of the API.
    """
    # MongoDB setup
    # We're testing using docker-compose remote interpreter so we can use same mongodb instance
    _MONGO_DAL = pymongo.MongoClient("mongodb://mongodb:27017/")

    @classmethod
    def setUpClass(cls):
        """
        A class method to setup a test app and mongodb.
        """
        # Setup test client
        mongo_dal = cls._MONGO_DAL
        app = DinoparkStatusApi.create_app(mongo_dal)
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """
        A class method called after tests in an individual class have run. This is to drop or delete collection entries after running test.
        """
        # Retrieve db and collection
        test_db = cls._MONGO_DAL["dinopark_status_db"]
        test_collection = test_db["dinopark_status_collection"]
        # Remove documents from the collection
        test_collection.delete_many({})

    def test_health_endpoint(self):
        """
        Test the health endpoint works.
        """
        with self.app as client:
            response = client.get('dinopark_status/' + API_VERSION + '/')
            response_json = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_json, {"status": {"code": 200, "info": "Welcome to Dino Park Status API!", "status": "SUCCESS"}})

    def test_safety_status(self):
        """
        Test the safety status endpoint works.
        """
        with self.app as client:
            pass

    @patch("dinopark_status_api.resources.requests.get")
    def test_maintenance_status(self, mock_get):
        """
        Test the maintenance status endpoint works.
        """
        # Test NUDLS source data
        source_data = [{'kind': 'dino_fed',
                        'dinosaur_id': 1039,
                        'park_id': 1,
                        'time': '2021-02-06T17:08:01.496Z'},
                       {'kind': 'dino_location_updated',
                        'location': 'V16',
                        'dinosaur_id': 1032,
                        'park_id': 1,
                        'time': '2021-02-05T17:08:01.497Z'},
                       {'kind': 'dino_removed',
                        'dinosaur_id': 1047,
                        'park_id': 1,
                        'time': '2021-02-05T17:08:01.497Z'},
                       {'kind': 'maintenance_performed',
                        'location': 'O4',
                        'park_id': 1,
                        'time': '2021-02-03T17:08:01.497Z'}]

        # Setup test dates. This is required since today's event_date changes everyday and test might fail.
        test_today_date = datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
        test_source_date = datetime.strptime("2021-02-03", "%Y-%m-%d")
        test_date_diff = (test_today_date - test_source_date).days

        expected_response = {
            "zone": "O4",
            "maintenance_required": 0,
            "info": f"Maintenance is not required. Currently {test_date_diff} days after last maintenance performed."
        }

        with self.app as client:
            args = "?zone=" + "O4"
            # Mock response.json() return values
            mock_get.return_value = Mock(status_code=200, json=lambda: source_data)
            response = client.get('dinopark_status/' + API_VERSION + '/maintenance_status' + args)
            response_json = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_json, expected_response)

    @mock.patch("dinopark_status_api.resources.requests.get")
    def test_no_nudls_response(self, mock_get):
        """
        Test API can handle exceptions raised when NUDLS is down.
        """
        # Test query args
        args = "?zone=" + "A1"
        # Mock response and exception
        mock_get.side_effect = HTTPError
        response = self.app.get('dinopark_status/' + API_VERSION + '/maintenance_status' + args)
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
