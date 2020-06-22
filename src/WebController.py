from flask import Flask, request
from Controller import Controller
from Rule import Rule

app = Flask(__name__)

current_controller = {}


@app.route("/controller", methods=["POST"])
def controller_route_handler():
    global current_controller
    if request.method == "POST":
        data = request.get_json(force=True)
        try:
            kwargs = data.get("kwargs") or {}
            ruleset_string = kwargs.get('ruleset')
            kwargs["ruleset"] = Rule.string_to_ruleset(ruleset_string)
            current_controller = Controller(**kwargs)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
