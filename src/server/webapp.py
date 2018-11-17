from flask import Blueprint
from aws import getPatientInfo, getImageList, getImageLink, getConsultationRequests, getDiagnosis, findPatient
import json
from state import lastPatientId

webapp_endpoints = Blueprint('webapp', __name__)

@webapp_endpoints.route("/info", methods=["GET"])
def getInfoPatient():
    return getInfo(lastPatientId)

def fixDecimal(x):
    x["timestamp"] = int(x["timestamp"])
    return x

@webapp_endpoints.route("/info/name/<patientName>", methods=["GET"])
def getInfoName(patientName):
    split = patientName.split(" ")
    patient = findPatient(split[0], split[1])
    return getInfo(patient["patientId"])

@webapp_endpoints.route("/info/<patientId>", methods=["GET"])
def getInfo(patientId):
    patientInfo = getPatientInfo(patientId)
    images = getImageList(patientId)
    diagnosis = getDiagnosis(patientId)
    return json.dumps({
        "id": patientInfo["patientId"],
        "familyName": patientInfo["familyName"],
        "givenName": patientInfo["givenName"],
        "images": list(map(lambda x: getImageLink(x["s3Key"], x["s3Bucket"]), images)),
        "diagnosis": list(map(fixDecimal, diagnosis))
    })


@webapp_endpoints.route("/consultations", methods=["GET"])
def get_ConsultationRequests():
    requests = getConsultationRequests()
    
    return json.dumps(
            list(map(lambda x: getPatientInfo(x["patientId"]), requests))
    )
    