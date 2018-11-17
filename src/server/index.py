from flask import Flask
from config import config
import alexa
from webapp import webapp_endpoints

app = Flask(__name__)
app.register_blueprint(webapp_endpoints, url_prefix='/api')
sio = socketio.init(app)
alexa.init(app, sio)

if __name__ == "__main__":
    if config["ssl"]:
        sio.run(app, ssl_context='adhoc', host=config["host"], port=config["port"]) 
    else:
        sio.run(app, host=config["host"], port=config["port"])