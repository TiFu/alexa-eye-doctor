from flask_socketio import SocketIO


def init(app):
    sio = SocketIO(app)

    

    return sio