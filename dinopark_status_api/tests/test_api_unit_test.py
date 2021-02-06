"""
Tests API main functionality.
"""

# System imports
import unittest

# Third-party import
import pymongo

# Local imports
from dinopark_status_api.constants import API_VERSION
from dinopark_status_api.apis import DinoparkStatusApi


class TestDinoparkStatusApi(unittest.TestCase):
    """
    Tests API's main functions.
    """
    @classmethod
    def setUpClass(cls):
        """
        Setup a test app.
        """
        # Setup test client and mongodb
        # We're testing using docker-compose remote interpreter so we can use same mongodb instance
        mongo_url = "mongodb://mongodb:27017/"
        mongo_dal = pymongo.MongoClient(mongo_url)
        app = DinoparkStatusApi.create_app(mongo_dal)
        cls.app = app.test_client()

    def test_health_endpoint(self):
        """
        Test the health endpoint works.
        """
        with self.app as client:
            response = client.get('dinopark_status/' + API_VERSION + '/')
            response_json = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_json, {"status": {"code": 200, "info": "Welcome to Dino Park Status API!", "status": "SUCCESS"}})
