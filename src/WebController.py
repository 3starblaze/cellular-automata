from flask import Flask, request, render_template
import numpy as np
from Controller import Controller
from Rule import Rule

app = Flask(__name__)

current_controller = {}


@app.route("/controller", methods=["GET", "POST"])
def controller_route_handler():
    global current_controller
    if request.method == "GET":
        if current_controller:
            return render_template("controller.j2", controller=current_controller,)
        else:
            return "There is no controller at the moment!"

    if request.method == "POST":
        data = request.get_json(force=True)
        try:
            kwargs = data.get("kwargs") or {}
            ruleset_string = kwargs.get("ruleset")
            kwargs["ruleset"] = Rule.string_to_ruleset(ruleset_string)
            current_controller = Controller(**kwargs)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}


@app.route("/controller/<path:prop>", methods=["GET"])
def controller_prop_route_handler(prop):
    try:
        prop_chain = prop.split("/")
        value = current_controller
        for p in prop_chain:
            value = getattr(value, p)
        if isinstance(value, np.ndarray):
            value = value.tolist()
        return {"success": True, "prop": value}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.route("/controller/update", methods=["POST"])
def controller_access():
    global current_controller
    data = request.get_json(force=True)
    try:
        for k, v in data.items():
            setattr(current_controller, k, v)
    except Exception as e:
        return {"success": False, "error": str(e)}

    return {"success": True}
