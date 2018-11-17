from flask import Blueprint, request
from aws import getPatientList ,getPatientInfo, updatePatientEyeColor, getImageList, getImageLink, getConsultationRequests, getDiagnosis, findPatient, uploadImage
import json
from state import lastPatientId
from face_processor import FaceProcessor
import os
from alexa import getPatientData
faceProcessor = FaceProcessor()

IMAGE_PATH = "images/"

webapp_endpoints = Blueprint('webapp', __name__)
@webapp_endpoints.route("/webapp", methods=["GET"])
def testWebapp():
    return "Hello webapp"

@webapp_endpoints.route("/patients", methods=["GET"])
def getPatients():
    patientList = getPatientList()
    print(patientList)
    return json.dumps(list(map(lambda x: getPatientData(x["patientId"]), patientList)))

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

import uuid

@webapp_endpoints.route("/uploadImage", methods=["POST"])
def uploadImageRequest():
    file = request.files["image"]
    f = os.path.join(IMAGE_PATH, lastPatientId + ".jpg")
    file.save(f)
    print("Saving image file")
    try:
        eyeData = faceProcessor.get_eye_data(f)
        print("got eye data: " + str(eyeData))
    except Exception as e:
        return str(False)
    if eyeData == faceProcessor.ERROR_BAD_EYE:
        return str(False)
    else:
        uploadImage(lastPatientId, eyeData[0], IMAGE_PATH + "/leftEye_" + str(uuid.uuid4()) + ".jpg")
        uploadImage(lastPatientId, eyeData[1], IMAGE_PATH + "/rightEye_" + str(uuid.uuid4()) + ".jpg")
        uploadImage(lastPatientId, f, "face.jpg")
        print(eyeData[2])
        updatePatientEyeColor(lastPatientId, eyeData[2])
        return str(True)
    


@webapp_endpoints.route("/consultations", methods=["GET"])
def get_ConsultationRequests():
    requests = getConsultationRequests()
    
    return json.dumps(
            list(map(lambda x: getPatientInfo(x["patientId"]), requests))
    )
    