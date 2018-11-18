from flask import Flask
from config import config
import sio_impl
import alexa
from webapp import webapp_endpoints
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(webapp_endpoints, url_prefix='/api')
sio = sio_impl.init(app)
CORS(app)
alexa.init(app, sio)

@app.route('/public/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file("./public/" + path)

if __name__ == "__main__":
    if config["ssl"]:
        sio.run(app, ssl_context='adhoc', host=config["host"], port=config["port"]) 
    else:
        sio.run(app, host=config["host"], port=config["port"])