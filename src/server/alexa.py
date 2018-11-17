from flask_ask import Ask, question, statement

def init(flaskApp):
    ask = Ask(flaskApp, "/alexa")

    @ask.intent("SendImageIntent")
    def handleSendImageIntent():
        return statement("Hello my friend!")


    @ask.intent("ConsultationIntent")
    def handleConsultationIntent():
        return statement("Hello World")