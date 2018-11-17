from flask_ask import Ask, question, statement
from aws import addConsultationRequest, addInformationRequest, findPatient

def init(flaskApp, sio):
    ask = Ask(flaskApp, "/alexa")

    @ask.intent("ConsultationRequestIntent")
    def handleCreateConsultationRequest(patientId):
        addConsultationRequest(patientId)
        # TODO: send notification to doctor
        return statement("I have created a consultation request. A doctor will contact you shortly.")

    @ask.intent("RequestInformationIntent")
    def handleRequestInformationIntent(patientName):
        splitName = patientName.split(" ")
        patient = findPatient(splitName[0], splitName[1])
        if patient is None:
                return statement("Sorry, I couldn't find " + str(patientName) + " in our database.")
        addInformationRequest(patientId)
        # todo send notification to patient
        return statement("I have added an information request for " + str(patientName))

    @ask.intent("SendImageIntent")
    def handleSendImageIntent():
        return statement("Hello my friend!")


    @ask.intent("ConsultationIntent")
    def handleConsultationIntent():
        return statement("Hello World")