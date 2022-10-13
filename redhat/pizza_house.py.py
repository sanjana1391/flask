from flask import Flask, jsonify, render_template, request

from crud import MongoCRUD
from error import UnsupportedRequestError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f8d8d62d5a9790dad915372e73bb202da93ae93b'
app.config["APPLICATION_ROOT"] = "/api/"

VALID_FORMAT = ("order")


@app.route('/healthcheck')
def healthcheck():
    return 'OK'

@app.route("/")
def hello_world():
    return "<p> WELCOME TO PIZZA HOUSE</p>"

@app.route('/crud/<orders_name>/', methods=["GET", "POST"])
@app.route('/crud/<orders_name>/<order_id>', methods=["GET", "DELETE", "PUT"])
def api_crud(orders_name=None, order_id=None):
    try:
        if orders_name not in VALID_FORMAT:
            raise UnsupportedRequestError(
                "Only formats {} are allowed".format(", ".join(VALID_FORMAT)))
        request_method = request.method

        if request_method == "GET":
            data_obj = MongoCRUD(orders_name, id=order_id)
            return jsonify(data_obj.read())

        if request_method == "DELETE":
            data_obj = MongoCRUD(orders_name, id=order_id)
            return jsonify(data_obj.delete())

        if request_method == "PUT":
            data = request.json
            data_obj = MongoCRUD(orders_name, id=order_id, data=data)
            return jsonify(data_obj.update())

        if request_method == "POST":
            data = request.json
            data_obj = MongoCRUD(orders_name, id=order_id, data=data)
            return jsonify(data_obj.create())

    except UnsupportedRequestError as error:
        return {"result": {"error": error.message}}, 422

    except Exception as exc:
        return {"result": {"error": str(exc)}}, 500
