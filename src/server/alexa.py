from flask_ask import Ask, question, statement

def init(flaskApp):
    ask = Ask(flaskApp, "/")

    @ask.intent("TestIntent")
    def testIntent():
        return statement("Hello my friend!")
