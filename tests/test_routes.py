import pytest

from app.tests.conftest import test_client


def test_heathcheck(test_client):
    response = test_client.get('/health-check')
    print('break')