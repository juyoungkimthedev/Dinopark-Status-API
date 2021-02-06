"""
Tests the API.
"""

# pylint: disable=invalid-name
# pylint: disable=unused-argument

# System imports
import os
import json
import unittest

# Third-party import
import adal
from mockito import mock


class TestAppErrorHandler(unittest.TestCase):
    """
    Tests for the API application's endpoints.
    """

    @classmethod
    def get_token_dict(cls, tenant_id, app_id, client_key):
        """
        Helper to generate a token dictionary (from which one can extract a token)

        :param tenant_id: The tenant ID (always the same for a Tenant, such as Capitec for example).
        :param app_id: The ID of the specific APP (different for different environments such as DEV, INT etc).
        :param client_key: The client's secret.
        :return: Token dictionary which includes the token.
        """
        # Retrieve valid AD token context
        context = adal.AuthenticationContext(
            'https://login.microsoftonline.com/' + tenant_id,
            validate_authority=tenant_id != 'adfs',
            api_version=None)

        # Acquire token with correct client credentials
        token_dict = context.acquire_token_with_client_credentials(
            resource=app_id,
            client_id=app_id,
            client_secret=client_key)

        return token_dict

    def setUp(self):
        """
        Setup a test app.
        """
        # Setup test client
        mock_dal = mock(CosmosSqlConnector, strict=False)
        app = TreatmentsModelApi.create_app(data_access_layer=mock_dal, config_object=Config)
        self.app = app.test_client()

        # Retrieve OAuth token
        token_dict = self.get_token_dict(tenant_id=TEST_TENANT_ID, app_id=TEST_APPLICATION_ID, client_key=TEST_CLIENT_KEY)
        token = token_dict['accessToken']

        # Header
        self.header = {'Authorization': 'Bearer {}'.format(token)}

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
