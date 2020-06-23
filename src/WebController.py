from flask import Flask, request, render_template
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
