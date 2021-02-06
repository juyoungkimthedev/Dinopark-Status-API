"""
Tests common API functions.
"""

# System imports
import unittest

# Third-party import
import pymongo

# Local imports
from dinopark_status_api.constants import API_VERSION
from dinopark_status_api.apis import DinoparkStatusApi


class TestAppErrorHandler(unittest.TestCase):
    """
    Tests for the API application's endpoints.
    """
    @classmethod
    def setUpClass(cls):
        """
        Setup a test app.
        """
        # Setup test client and mongodb
        # Here since we're testing for common API functions, it will not write anything to mongodb
        mongo_url = "mongodb://mongodb:27017/"
        mongo_dal = pymongo.MongoClient(mongo_url)
        app = DinoparkStatusApi.create_app(mongo_dal)
        cls.app = app.test_client()

    def test_unsupported_route_error(self):
        """
        Test that the correct error is generated if an unsupported route is invoked i.e. "Resource Not Available".
        """
        with self.app as client:
            response = client.get('dinopark_status/' + API_VERSION + '/test_route')
            self.assertEqual(response.status_code, 404)

    def test_unsupported_operation_error(self):
        """
        Test that the correct error is generated if an unsupported operation is tried on a route. i.e. "The method is not allowed for the requested URL".
        The home endpoint does not support post request hence, the test should return 405 not allowed method.
        """
        with self.app as client:
            response = client.post('dinopark_status/' + API_VERSION + '/')
            self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
