from flask_ask import Ask, question, statement

def init(flaskApp):
    ask = Ask(flaskApp, "/alexa")

    @ask.intent("SendImageIntent")
    def testIntent():
        return statement("Hello my friend!")
