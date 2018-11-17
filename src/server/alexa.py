from flask_ask import Ask, question, statement, session
from aws import addConsultationRequest, addInformationRequest, findPatient, getPatientInfo, addDiagnosis
from state import setLastPatientId

def init(flaskApp, sio):
    ask = Ask(flaskApp, "/alexa")
    
    doctorState = {}

    userToPatientMap = {
         "amzn1.ask.account.AHCO7SYGZ5HUOBAKO5UASYRICROEXDZ7QJ6ZUY4FK2G43XLXO3EG3BMRG3VDXVWRPUXMX5N6EBTQKNOSBDHWMWU2CNQQA3REQLN4TAP3Q4UQNQDYBQTGAIKJUEVSSQAYYOVDKKTTXPOGHMZQBBJFLAC34N6M6EHSPTTE5PRM6J2NDE3XMVU6NZSAFU4DAA72PLTLBHDVMP5TD7A": "21c03410-ea14-11e8-badf-6542a9f38021"
    }

    userToDoctorMap = {
        
    }

    @ask.intent("ViewPatientDataIntent") # Alexa, show me my diagnosis
    def handleViewPatientIntent():
        setLastPatientId(userToPatientMap[session.user.userId])
        return statement("Okay, I'm opening your patient data.")

    @ask.intent("VideoCallIntent")
    def handleVideoCallIntent():
        return statement("Testing video call intent")

    @ask.intent("MessageIntent")
    def handleMessageIntent(message):
        addConsultationRequest(userToPatientMap[session.user.userId], message)
        # TODO: send notification to doctor
        return statement("I have created a consultation request. A doctor will contact you shortly.")

    @ask.intent("ConsultationIntent")
    def handleCreateConsultationRequest():
        addConsultationRequest(userToPatientMap[session.user.userId])
        # TODO: send notification to doctor
        return statement("I have created a consultation request. A doctor will contact you shortly.")

    @ask.intent("RequestInformationIntent")
    def handleRequestInformationIntent():
        patientId = doctorState[session.user.userId]
        patient = getPatientInfo(patientId)
        addInformationRequest(patientId)
        # todo send notification to patient
        return statement("I have added an information request for " + str(patient["givenName"] + " " + str(patient["familyName"])))

    @ask.intent("OpenPatientIntent")
    def handleOpenPatientIntent(patientName):
        splitName = patientName.split(" ")
        patient = findPatient(splitName[0], splitName[1])
        if patient is None:
                return statement("Sorry, I couldn't find " + str(patientName) + " in our database.")
        else:
                doctorState[session.user.userId] = patient["patientId"]
                return statement("Opening " + str(patientName) + "'s file.")

    @ask.intent("AddDiagnosisIntent")
    def handleAddDiagnosisIntent(diagnosis):
        patientId = doctorState[session.user.userId]
        patientInfo = getPatientInfo(patientId)
        addDiagnosis(patientId, diagnosis)
        return statement("Alright, I saved your diagnosis in " + patientInfo["givenName"] + " " + patientInfo["familyName"])

    @ask.intent("SendImageIntent")
    def handleSendImageIntent():
        return statement("The images were sent successfully!")
