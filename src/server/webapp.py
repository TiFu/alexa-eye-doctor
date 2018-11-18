from flask import Blueprint, request
from aws import getPatientList ,getPatientInfo, getConsultationRequests, updatePatientEyeColor, getImageList, getImageLink, getDiagnosis, findPatient, uploadImage
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
    result = {
        "id": patientInfo["patientId"],
        "familyName": patientInfo["familyName"],
        "givenName": patientInfo["givenName"],
        "images": list(map(lambda x: getImageLink(x["s3Key"], x["s3Bucket"]), images)),
        "diagnosis": list(map(fixDecimal, diagnosis))
    }
    for key, val in patientInfo.items():
        result[key] = val
        
    return json.dumps(result)

@webapp_endpoints.route("/consultations", methods=["GET"])
def fetchConsultations():
    return json.dumps(getConsultationRequests())


import uuid
import base64
from binascii import a2b_base64
from urllib.parse import urlparse

@webapp_endpoints.route("/uploadImage", methods=["POST"])
def uploadImageRequest():
    print("Requested upload image")
    print(request.form["image"])
    file = request.form["image"]
    print(file)
    f = os.path.join(IMAGE_PATH, lastPatientId + ".jpg")

    up = urlparse(file)
    head, data = up.path.split(',', 1)
    bits = head.split(';')
    mime_type = bits[0] if bits[0] else 'text/plain'
    charset, b64 = 'ASCII', False
    for bit in bits:
        if bit.startswith('charset='):
            charset = bit[8:]
        elif bit == 'base64':
            b64 = True
    plaindata = base64.b64decode(data)
    with open(f, "wb") as outputFile:
        outputFile.write(plaindata)


    print("Saving image file")
    try:
        eyeData = faceProcessor.get_eye_data(f)
        print("got eye data: " + str(eyeData))
    except Exception as e:
        return str(2)
    if eyeData == faceProcessor.ERROR_BAD_EYE:
        return str(1)
    else:
        uploadImage(lastPatientId, eyeData[0], IMAGE_PATH + "/leftEye_" + str(uuid.uuid4()) + ".jpg")
        uploadImage(lastPatientId, eyeData[1], IMAGE_PATH + "/rightEye_" + str(uuid.uuid4()) + ".jpg")
        uploadImage(lastPatientId, f, "face.jpg")
        updatePatientEyeColor(lastPatientId, eyeData[2])
        return str(0)
    
    