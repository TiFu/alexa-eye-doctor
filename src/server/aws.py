import boto3
import json
import os
import uuid
import time

lambda_client = boto3.client('lambda', region_name="eu-west-1")
s3_client = boto3.client('s3')
dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
consulationRequestTable = dynamodb.Table("ConsultationRequest")
infoRequestTable = dynamodb.Table("RequestInfo")
diagnosisTable = dynamodb.Table("Diagnosis")

def findPatient(givenName, fullName):
    patients = getPatientList()
    potentialPatients = list(filter(lambda x: x["givenName"] == givenName and x["familyName"] == fullName))
    if len(potentialPatients) == 0:
        return None
    else:
        return potentialPatients[0]

def getPatientList():
    result = lambda_client.invoke(FunctionName="dr-cloud-patient-service", Payload=json.dumps({ "action": "list"}))
    return json.loads(result["Payload"].read().decode())

def getPatientInfo(id):
    result = lambda_client.invoke(FunctionName="dr-cloud-patient-service", Payload=json.dumps({ "action": "get", "body": { "patientId": id}}))
    return json.loads(result["Payload"].read().decode())

def createPatient(givenName, familyName):
    result = lambda_client.invoke(FunctionName="dr-cloud-patient-service", Payload=json.dumps({ "action": "create", "body": { "givenName": givenName, "familyName": familyName}}))
    return json.loads(result["Payload"].read().decode())

def getImageList(patientId):
    result = lambda_client.invoke(FunctionName="dr-cloud-image-service", Payload=json.dumps({ "action": "list", "body": { "patientId": patientId}}))
    return json.loads(result["Payload"].read().decode())

def uploadImage(patientId, fileName, bucket="dr-cloud-128740296733-eu-west-1"):
    key = patientId.split("-")[0] + "/" + patientId + "/" + os.path.basename(fileName)
    result = s3_client.upload_file(fileName, bucket, key)


def addConsultationRequest(patientId, message = None):
    guid = uuid.uuid4()
    consulationRequestTable.put_item(Item={"consultationId": str(guid), "patientId": patientId, "message": message if not None else ""})

def deleteConsultationRequests(consultationId):
    consulationRequestTable.delete_item(Key={"consultationId": consultationId})

def getConsultationRequests():
    return consulationRequestTable.scan()["Items"]


def addInformationRequest(patientId):
    infoRequestTable.put_item(Item={"patientId": str(patientId)})

def deleteInformationRequest(patientId):
    infoRequestTable.delete_item(Key={"patientId": str(patientId)})

def getInformationRequest(patientId):
    return "Item" in infoRequestTable.get_item(Key={"patientId": str(patientId)})

def addDiagnosis(patientId, diagnosis):
    guid = uuid.uuid4()
    diagnosisTable.put_item(Item={"timestamp": time.time(), "diagnosisId": str(guid), "patientId": patientId, "diagnosis": diagnosis})

def getDiagnosis(patientId):
    return sorted(list(filter(lambda x: x["patientId"] == patientId, diagnosisTable.scan()["Items"])), key=lambda x: x["timestamp"])

# defining the bucket like this is horrible - but hey it's a hackatohn
# also not making the region a variable
def getImageLink(key, bucket="dr-cloud-128740296733-eu-west-1"):
    return "https://s3-eu-west-1.amazonaws.com/" + bucket + "/" + key
