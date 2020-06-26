import pytest

from WebController import app as WebController


@pytest.fixture
def client():
    WebController.config["TESTING"] = True
    return WebController.test_client()


@pytest.fixture
def controller_init(client):
    return client.post(
        "/controller",
        json={
            "kwargs": {
                "indices": [[0, 1], [1, 0]],
                "ruleset": "if cell:\n    return 3 <= sum(retrieved_cells) <= 4\nelse:\n    return sum(retrieved_cells) == 3",
                "width": 467,
            }
        },
    )


def test_index_page(client):
    assert client.get("/").status_code == 404


def test_controller_page(client):
    assert client.get("/controller").data == b"There is no controller at the moment!"


def test_controller_creation(client, controller_init):
    data = controller_init.get_json()
    assert data["success"]
    assert client.get("/controller").data != b"There is no controller at the moment!"


def test_prop_access(client, controller_init):
    assert client.get("/controller/width").get_json()["prop"] == 467
    assert client.get("/controller/data").get_json()["prop"] == [[0] * 10] * 10


def test_prop_update(client, controller_init):
    assert (
        client.post("/controller/update", json={"height": 420}).get_json()["success"]
        == True
    )
    assert client.get("/controller/height").get_json()["prop"] == 420
