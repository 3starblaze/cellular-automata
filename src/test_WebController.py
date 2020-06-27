import pytest

from Rule import Rule
from Controller import Controller
from WebController import app as WebController


@pytest.fixture
def client():
    WebController.config["TESTING"] = True
    return WebController.test_client()


@pytest.fixture
def controller_init(client):
    global current_controller

    indices = [[0, 1], [1, 0]]
    ruleset_string = (
        "if cell:"
        "    return 3 <= sum(retrieved_cells) <= 4"
        "else:"
        "    return sum(retrieved_cells) == 3"
    )
    width = 467

    current_controller = Controller(
        indices, Rule.string_to_ruleset(ruleset_string), width=width
    )
    return client.post(
        "/controller",
        json={
            "kwargs": {"indices": indices, "ruleset": ruleset_string, "width": width,}
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
    assert (
        client.get("/controller/width").get_json()["prop"] == current_controller.width
    )
    assert (
        client.get("/controller/data").get_json()["prop"]
        == current_controller.data.tolist()
    )


def test_nested_prop_access(client, controller_init):
    res = client.get("/controller/drawer/line_width").get_json()
    assert res["prop"] == current_controller.drawer.line_width
    res = client.get("/controller/state/rule/indices").get_json()
    assert res["prop"] == current_controller.state.rule.indices.tolist()


def test_prop_update(client, controller_init):
    assert client.post("/controller/update", json={"height": 420}).get_json()["success"]
    assert client.get("/controller/height").get_json()["prop"] == 420
