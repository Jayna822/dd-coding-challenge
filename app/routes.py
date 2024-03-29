
from flask import Response, jsonify

from app import app_blueprint
from app.api_logic import get_github_info, get_bitbucket_info, merge_dicts


@app_blueprint.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    # app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app_blueprint.route("/merge/<profile>", methods=["GET"])
@app_blueprint.route("/merge/<profile>/<profile2>", methods=["GET"])
def merge(profile, profile2=None):
    """
    Merge profiles from Github and Bitbucket together.
    In the case of differing profile names,
        the Github profile name must be first followed by the Bitbucket profile name
    """

    github_info = get_github_info(profile)
    bitbucket_info = get_bitbucket_info(profile2 or profile)

    data = {
        'github_org': profile,
        'bitbucket_team': profile2 or profile,
        'github_results': github_info,
        'bitbucket_results': bitbucket_info
    }

    # Check to make sure there wasn't an error in getting API results
    if not(github_info.get('error') or bitbucket_info.get('error')):
        merge_result = merge_dicts(github_info, bitbucket_info)
        data['merge'] = merge_result

    return jsonify(data)
