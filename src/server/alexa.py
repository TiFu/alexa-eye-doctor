from flask_ask import Ask, question, statement, session
from aws import addConsultationRequest, addInformationRequest, updatePatientEyeColor, findPatient, getPatientInfo, addDiagnosis, getDiagnosis, getImageLink, getImageList
from state import setLastPatientId
from datetime import datetime

def fixDecimal(x):
    x["timestamp"] = int(x["timestamp"])
    return x

def getPatientData(patientId):
        patientInfo = getPatientInfo(patientId)
        images = getImageList(patientId)
        diagnosis = getDiagnosis(patientId)
        outputData = {
                "id": patientInfo["patientId"],
                "images": list(map(lambda x: getImageLink(x["s3Key"], x["s3Bucket"]), images)),
                "diagnosis": list(map(fixDecimal, diagnosis))
        }
        for key, val in patientInfo.items():
            outputData[key] = val
        return outputData

def init(flaskApp, sio):
    ask = Ask(flaskApp, "/alexa")
    
    doctorState = {}

    userToPatientMap = {
         "amzn1.ask.account.AHCO7SYGZ5HUOBAKO5UASYRICROEXDZ7QJ6ZUY4FK2G43XLXO3EG3BMRG3VDXVWRPUXMX5N6EBTQKNOSBDHWMWU2CNQQA3REQLN4TAP3Q4UQNQDYBQTGAIKJUEVSSQAYYOVDKKTTXPOGHMZQBBJFLAC34N6M6EHSPTTE5PRM6J2NDE3XMVU6NZSAFU4DAA72PLTLBHDVMP5TD7A": "21c03410-ea14-11e8-badf-6542a9f38021",
         "amzn1.ask.account.AH62JX6DPMTJ7DZPIUTHK34ZL7S5CYA2FC7L3EIZSZ6EHK7NPYLZHHURK75MADNLAXCAJRQBGS5ZQRZEZ2JCNB2YRGCRKBQDDW2FUKLVWA3ATSV7WU27YOMPZZMIUQUVCLPDGJ4PDA4QHH4FIHDSRNPFCUOPB6AQ5J7275AQMCHKPNYSGOR7HSSKZVDR2C3HPSVKM2PLTOQ7F4A": "21c03410-ea14-11e8-badf-6542a9f38021"
    }

    userToDoctorMap = {
        
    }

    def updatePatientData(patientId, ns):
        sio.emit("patient_data", getPatientData(patientId), namespace=ns)


    def getPatientIdFromUser(userId):
        if userId not in userToPatientMap:
                userToPatientMap[userId] = "21c03410-ea14-11e8-badf-6542a9f38021"
        return userToPatientMap[userId]

    @ask.intent("AMAZON.FallbackIntent")
    def handleFallbackIntent():
        return statement("Fallback Intent!")

    @ask.intent("TestIntent")
    def handleTestIntent():
        return statement("Test Intent successful!")

    @ask.intent("ViewPatientDataIntent") # Alexa, show me my diagnosis
    def handleViewPatientIntent():
        patientId = getPatientIdFromUser(session.user.userId)
        setLastPatientId(patientId)
        updatePatientData(patientId, "/patient")
        sio.emit("show_patient_overview", patientId, namespace="/doctor")
        return statement("Okay, I'm opening your patient data.")

    @ask.intent("VideoCallIntent")
    def handleVideoCallIntent():
        return statement("Testing video call intent")

    @ask.intent("MessageIntent")
    def handleMessageIntent(message):
        addConsultationRequest(getPatientIdFromUser(session.user.userId), message)
        # TODO: send notification to doctor
        sio.emit("new_consultation_request", None, namespace="/doctor")
        return statement("I have created a consultation request. A doctor will contact you shortly.")

    @ask.intent("ConsultationIntent")
    def handleConsultationIntent():
        return handleMessageIntent(" ")

    @ask.intent("ScheduleConsultationIntent")
    def handleCreateConsultationRequest(date):
        addConsultationRequest(getPatientIdFromUser(session.user.userId), "The patient has requested a consultation on " + str(date))
        # TODO: send notification to doctor
        sio.emit("new_consultation_request", None, namespace="/doctor")
        return statement("I have created a consultation request on " + str(date) + ". A doctor will contact you shortly.")

    @ask.intent("ShowDiagnosisIntent")
    def handleShowDiagnosisIntent():
        patientId = getPatientIdFromUser(session.user.userId)
        diagnosis = getDiagnosis(patientId)
        diagnose = diagnosis[len(diagnosis) - 1]
        return statement("The latest diagnosis from your doctor was created on " + datetime.utcfromtimestamp(diagnose["timestamp"]).strftime('%Y-%m-%d %H:%M:%S') + ". The doctor said: " + str(diagnose["diagnosis"]))

    @ask.intent("ShowConsultationListIntent")
    def handleShowConsultationListIntent():
        sio.emit("show_consultation_list", namespace="/doctor")
        return statement("Okay. I am opening the consultation list")

    @ask.intent("ShowPatientListIntent")
    def handleShowPatientListIntent():
        sio.emit("show_patient_list", namepsace="/doctor")
        return statement("Okay. I am opening the patient list")

    @ask.intent("RequestPictureIntent")
    def handleRequestInformationIntent():
        patientId = doctorState[session.user.userId]
        addInformationRequest(patientId)
        # todo send notification to patient
        updatePatientData(patientId, "/patient")
        sio.emit("new_picture_request", None, namespace="/patient")
        return statement("I have added an information request for " + str(patient["givenName"] + " " + str(patient["familyName"])))

    @ask.intent("GetInfoIntent")
    def handleOpenPatientIntent(name):
        splitName = name.split(" ")
        patient = findPatient(splitName[0], splitName[1])
        if patient is None:
                return statement("Sorry, I couldn't find " + str(name) + " in our database.")
        else:
                doctorState[session.user.userId] = patient["patientId"]
                updatePatientData(patient["patientId"], "/doctor")
                return statement("Opening " + str(name) + "'s file.")

    @ask.intent("SendDiagnosisIntent")
    def handleAddDiagnosisIntent(message):
        patientId = doctorState[session.user.userId]
        patientInfo = getPatientInfo(patientId)
        addDiagnosis(patientId, message)
        updatePatientData(patientId, "/patient")
        sio.emit("new_diagnosis", None, namespace="/patient")
        return statement("Alright, I saved your diagnosis for " + patientInfo["givenName"] + " " + patientInfo["familyName"])

    @ask.intent("SendImageIntent")
    def handleSendImageIntent():
        sio.emit("take_picture", None, namespace="/patient")
        return statement("Please take a picture of your face!")
