from flask_ask import Ask, question, statement
from aws import getPatientList

def init(flaskApp, sio):
    ask = Ask(flaskApp, "/alexa")

    @ask.intent("SendImageIntent")
    def handleSendImageIntent():
        return statement("Hello my friend!")


    @ask.intent("ConsultationIntent")
    def handleConsultationIntent():
        return statement("Hello World")