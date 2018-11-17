from flask_ask import Ask, question, statement
from aws import addConsultationRequest

def init(flaskApp, sio):
    ask = Ask(flaskApp, "/alexa")

    @ask.intent("CreateConsultationRequestIntent")
    def handleCreateConsultationRequest(patientId):
        addConsultationRequest(patientId)
        return statement("I have created a consultation request. A doctor will contact you shortly.")

    @ask.intent("SendImageIntent")
    def handleSendImageIntent():
        return statement("Hello my friend!")


    @ask.intent("ConsultationIntent")
    def handleConsultationIntent():
        return statement("Hello World")