import logging

import pytest
from fastapi.testclient import TestClient

from parma_mining.clearbit import __version__
from parma_mining.clearbit.api.dependencies.auth import authenticate
from parma_mining.clearbit.api.main import app
from parma_mining.mining_common.const import HTTP_200
from tests.dependencies.mock_auth import mock_authenticate


@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authenticate: mock_authenticate,
        }
    )
    return TestClient(app)


logger = logging.getLogger(__name__)


@pytest.mark.parametrize("arg", [True, False])
def test_dummy(arg: bool):
    assert arg or not arg
    assert len(__version__) > 0


def test_root(client):
    response = client.get("/")
    assert response.status_code == HTTP_200
    assert response.json() == {"welcome": "at parma-mining-clearbit"}


def test_dummy_auth(client):
    response = client.get("/dummy-auth")
    assert response.status_code == HTTP_200
    assert response.json() == {"welcome": "at parma-mining-clearbit"}
