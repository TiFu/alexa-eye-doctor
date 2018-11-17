import boto3
import json
import os

lambda_client = boto3.client('lambda', region_name="eu-west-1")
s3_client = boto3.client('s3')

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
