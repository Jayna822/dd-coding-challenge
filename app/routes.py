import logging

import flask
from flask import Response

from app.api_logic import get_github_info, get_bitbucket_info

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


@app.route("/merge/<user>", methods=["GET"])
@app.route("/merge/<user>/<user2>", methods=["GET"])
def merge(user, user2=None):
    """
    Merge profiles from Github and Bitbucket together.
    In the case of differing profile names,
        the Github profile name must be first followed by the Bitbucket profile name
    """
    # github_org = user
    # bb_team = user2 or user

    github_info = get_github_info(user)
    bitbucket_info = get_bitbucket_info(user2 or user)

    return 'Profile1: {}, Profile2: {}'.format(user, user2)
#
# if __name__ == "__main__":
#     app.run(debug=True)

