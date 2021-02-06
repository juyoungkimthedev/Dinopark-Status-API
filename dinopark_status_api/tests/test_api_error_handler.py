"""
Tests the API.
"""

# System imports
import os
import json
import unittest

# Third-party import
from mockito import mock
from pymongo import MongoClient

# Local imports
from dinopark_status_api.apis import DinoparkStatusApi


class TestAppErrorHandler(unittest.TestCase):
    """
    Tests for the API application's endpoints.
    """
    def setUp(self):
        """
        Setup a test app.
        """
        # Setup test client
        mock_dal = mock(MongoClient, strict=False)
        app = DinoparkStatusApi.create_app(mock_dal)
        self.app = app.test_client()

        # Setup test data path
        self.directory_path = os.path.dirname(__file__)
        with open(os.path.join(self.directory_path, 'data/treatments_model_input_data.json')) as json_source:
            self.vmax_test_source = json.load(json_source)

    def test_unauthorized_error(self):
        """
        Test that the correct error is generated if the token is incorrect i.e. "Invalid Token".
        """
        with self.app as client:
            response = client.post('treatments_model/' + API_VERSION + '/best_treatments/', json=self.vmax_test_source, headers={
                'Authorization': 'Bearer {}'.format('junk')
            })
            self.assertEqual(response.status_code, 401)

    def test_unsupported_route_error(self):
        """
        Test that the correct error is generated if an unsupported route is invoked i.e. "Resource Not Available".
        """
        with self.app as client:
            response = client.get('treatments_model/' + API_VERSION + '/test_route', headers=self.header)
            self.assertEqual(response.status_code, 404)

    def test_unsupported_operation_error(self):
        """
        Test that the correct error is generated if an unsupported operation is tried on a route. i.e. "The method is not allowed for the requested URL".
        The home endpoint does not support post request hence, the test should return 405 not allowed method.
        """
        with self.app as client:
            response = client.post('treatments_model/' + API_VERSION + '/', headers=self.header)
            self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
