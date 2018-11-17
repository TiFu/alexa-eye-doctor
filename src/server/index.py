from flask import Flask
from config import config
import alexa
from webapp import webapp_endpoints

from flask_socketio import SocketIO


app = Flask(__name__)
app.register_blueprint(webapp_endpoints, url_prefix='/api')
alexa.init(app)

#sio = SocketIO(app)

if __name__ == "__main__":
    if config["ssl"]:
        app.run(ssl_context='adhoc', host=config["host"], port=config["port"]) 
    else:
        app.run(host=config["host"], port=config["port"])