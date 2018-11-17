from flask import Blueprint
from aws import getPatientInfo, getImageList, getImageLink
import json

webapp_endpoints = Blueprint('webapp', __name__)

@webapp_endpoints.route('/webapp')
def show():
    return "Hello Webapp"

@webapp_endpoints.route("/info/<patientId>", methods=["GET"])
def getInfo(patientId):
    patientInfo = getPatientInfo(patientId)
    images = getImageList(patientId)

    print(patientInfo)
    print(images)
    return json.dumps({
        "id": patientInfo["patientId"],
        "familyName": patientInfo["familyName"],
        "givenName": patientInfo["givenName"],
        "images": list(map(lambda x: getImageLink(x["s3Key"], x["s3Bucket"]), images))
    })