from flask_socketio import SocketIO


def init(app):
    sio = SocketIO(app)

    advertisementIdToPatientMap = {}

    @sio.on('connect', namespace="/patient")
    def connected():
        print("New connection on patient")


    @sio.on('connect', namespace="/doctor")
    def connected():
        print("New connection on doctor")

    return sio