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

    def test_maintenance_status(self):
        """
        Test the health endpoint works.
        """
        with self.app as client:
            pass

    def test_safety_status(self):
        """
        Test the health endpoint works.
        """
        with self.app as client:
            pass

    def test_no_nudls_response(self):
        """
        Test API can handle no response from NUDLS monitoring system. I.e. service unavailable, should return 503 status code.
        """
        with self.app as client:
            pass
