from flask import Blueprint

webapp_endpoints = Blueprint('webapp', __name__)

@webapp_endpoints.route('/webapp')
def show():
    return "Hello Webapp"

@webapp_endpoints.route("/info/<name>", methods=["GET"])
def getInfo(name):
    pass

