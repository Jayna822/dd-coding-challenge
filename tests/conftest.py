import pytest
from flask import Flask


@pytest.fixture(scope='module')
def test_client():
    flask_app = Flask(__name__)
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()