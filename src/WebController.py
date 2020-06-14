from flask import Flask, request
from Controller import Controller

app = Flask(__name__)

current_controller = {}


@app.route("/controller", methods=["POST"])
def controller_route_handler():
    global current_controller
    if request.method == "POST":
        data = request.get_json(force=True)
        try:
            current_controller = Controller(*data["args"], **data["kwargs"])
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
