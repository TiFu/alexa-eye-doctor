from flask import Flask, send_from_directory
from config import config
import sio_impl
import alexa
from webapp import webapp_endpoints
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="public")
app.register_blueprint(webapp_endpoints, url_prefix='/api')
sio = sio_impl.init(app)
CORS(app)
alexa.init(app, sio)

@app.route('/public/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return send_from_directory("./public/", path)

if __name__ == "__main__":
    if config["ssl"]:
        sio.run(app, ssl_context='adhoc', host=config["host"], port=config["port"]) 
    else:
        sio.run(app, host=config["host"], port=config["port"])
