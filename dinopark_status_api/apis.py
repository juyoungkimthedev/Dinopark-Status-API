"""
Main API package.
"""

# System imports
import logging

# Third-party imports
from flask import Flask, jsonify
from flask_restful import Api

# Local imports
from dinopark_status_api.constants import LOGGER, API_VERSION
from dinopark_status_api.resources import Health, Status


class DinoparkStatusApi(Api):
    """
    Dinopark Status API.
    """

    def handle_error(self, e):
        """
        Error handler for the API transforms a raised exception into a Flask response,
        with the appropriate HTTP status code and body..

        We are overriding handle_error inside Api package to customize.

        :param e: The exception to handle
        :return: JSON with the status and exception.
        """
        # retrieve attribute of exception class, defaults to 500.
        code = getattr(e, "code", 500)
        if hasattr(e, 'description') and e.description:
            message = e.description
        else:
            # if a description attribute is not available, consider it being a Python core exception class.
            message = f"Internal server error. Possible reason: {e.__class__.__name__}: {e}"

        error_message = f"{code} {message}"
        logging.getLogger(LOGGER).error(error_message)

        return self.make_response(jsonify({
            "status": {
                "code": code,
                "info": message,
                "status": "FAILURE"
            }
        }))

    @staticmethod
    def create_app():
        """
        Creates a new API instance.
        """
        logger = logging.getLogger(LOGGER)

        # Instantiate a new Flask app
        app = Flask(__name__)

        # Base path
        base_path = "/park_zone/" + API_VERSION

        @app.after_request
        def after_request(response):
            """
            Function to modify the response after the request has been processed.
            :param response:
            :return:
            """
            if 200 <= response.status_code < 300:
                log_statement = {
                    "status": {
                        "code": response.status_code,
                        "status": "SUCCESS"
                    }
                }

                logger.info(log_statement)
                return response

        # Instantiate main API class within Api. This is possible as information to create object of a class
        # is already known at the point when one of its methods is called in app.py
        api = DinoparkStatusApi(app, prefix=base_path)

        # Routes
        api.add_resource(Health, "/", endpoint="health")
        api.add_resource(Status, "/status/", "/status", endpoint="status", strict_slashes=False)

        return app