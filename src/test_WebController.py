import pytest

from WebController import app as WebController


@pytest.fixture
def client():
    WebController.config["TESTING"] = True
    return WebController.test_client()


def test_index_page(client):
    assert client.get("/").status_code == 404


def test_controller_page(client):
    assert client.get("/controller").data == b"There is no controller at the moment!"
