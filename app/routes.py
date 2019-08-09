import logging

import flask
from flask import Response

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app.route("/merge/<profile>", methods=["GET"])
@app.route("/merge/<profile>/<profile2>", methods=["GET"])
def merge(profile, profile2=None):
    """
    Merge profiles from Github and Bitbucket together.
    In the case of differing profile names,
        the Github profile name must be first followed by the Bitbucket profile name
    """
    return 'Profile1: {}, Profile2: {}'.format(profile, profile2)
