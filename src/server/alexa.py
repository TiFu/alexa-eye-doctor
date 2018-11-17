from flask_ask import Ask, question, statement, session
from aws import addConsultationRequest, addInformationRequest, findPatient, getPatientInfo, addDiagnosis
from state import setLastPatientId

def init(flaskApp, sio):
    ask = Ask(flaskApp, "/alexa")
    
    doctorState = {}

    userToPatientMap = {
         "amzn1.ask.account.AHCO7SYGZ5HUOBAKO5UASYRICROEXDZ7QJ6ZUY4FK2G43XLXO3EG3BMRG3VDXVWRPUXMX5N6EBTQKNOSBDHWMWU2CNQQA3REQLN4TAP3Q4UQNQDYBQTGAIKJUEVSSQAYYOVDKKTTXPOGHMZQBBJFLAC34N6M6EHSPTTE5PRM6J2NDE3XMVU6NZSAFU4DAA72PLTLBHDVMP5TD7A": "21c03410-ea14-11e8-badf-6542a9f38021",
         "amzn1.ask.account.AH62JX6DPMTJ7DZPIUTHK34ZL7S5CYA2FC7L3EIZSZ6EHK7NPYLZHHURK75MADNLAXCAJRQBGS5ZQRZEZ2JCNB2YRGCRKBQDDW2FUKLVWA3ATSV7WU27YOMPZZMIUQUVCLPDGJ4PDA4QHH4FIHDSRNPFCUOPB6AQ5J7275AQMCHKPNYSGOR7HSSKZVDR2C3HPSVKM2PLTOQ7F4A": "21c03410-ea14-11e8-badf-6542a9f38021"
    }

    userToDoctorMap = {
        
    }

    def getPatientIdFromUser(userId):
        if userId not in userToPatientMap:
                userToPatientMap[userId] = "21c03410-ea14-11e8-badf-6542a9f38021"
        return userToPatientMap[userId]

    @ask.intent("AMAZON.FallbackIntent")
    def handleFallbackIntent():
        return statement("Amazon sucks!")

    @ask.intent("TestIntent")
    def handleTestIntent():
        return statement("Test Intent successful!")

    @ask.intent("ViewPatientDataIntent") # Alexa, show me my diagnosis
    def handleViewPatientIntent():
        setLastPatientId(getPatientIdFromUser(session.user.userId))
        return statement("Okay, I'm opening your patient data.")

    @ask.intent("VideoCallIntent")
    def handleVideoCallIntent():
        return statement("Testing video call intent")

    @ask.intent("MessageIntent")
    def handleMessageIntent(message):
        addConsultationRequest(getPatientIdFromUser(session.user.userId), message)
        # TODO: send notification to doctor
        return statement("I have created a consultation request. A doctor will contact you shortly.")

    @ask.intent("ScheduleConsultationIntent")
    def handleCreateConsultationRequest(date):
        addConsultationRequest(getPatientIdFromUser(session.user.userId), "The patient has requested a consultation on " + str(date))
        # TODO: send notification to doctor
        return statement("I have created a consultation request on " + str(date) + ". A doctor will contact you shortly.")

    @ask.intent("RequestPictureIntent")
    def handleRequestInformationIntent():
        patientId = doctorState[session.user.userId]
        patient = getPatientInfo(patientId)
        addInformationRequest(patientId)
        # todo send notification to patient
        return statement("I have added an information request for " + str(patient["givenName"] + " " + str(patient["familyName"])))

    @ask.intent("GetInfoIntent")
    def handleOpenPatientIntent(name):
        splitName = name.split(" ")
        patient = findPatient(splitName[0], splitName[1])
        if patient is None:
                return statement("Sorry, I couldn't find " + str(name) + " in our database.")
        else:
                doctorState[session.user.userId] = patient["patientId"]
                return statement("Opening " + str(name) + "'s file.")

    @ask.intent("SendDiagnosisIntent")
    def handleAddDiagnosisIntent(message):
        patientId = doctorState[session.user.userId]
        patientInfo = getPatientInfo(patientId)
        addDiagnosis(patientId, message)
        return statement("Alright, I saved your diagnosis for " + patientInfo["givenName"] + " " + patientInfo["familyName"])

    @ask.intent("SendImageIntent")
    def handleSendImageIntent():
        return statement("The images were sent successfully!")
