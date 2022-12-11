from flask import Flask, request, jsonify
import socket
from datetime import datetime
from IoTDirectoryService import Virtualizer, Gateway, Manager

LOCAL_HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

IoTmaganer = Flask(__name__)
@IoTmaganer .route('/',methods =['GET', 'POST', 'DELETE'])
def manager():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        try:
            data = request.get_json()
        except:
            return "[DATABASE]:\tPOST: ERROR"
    if request.method == 'DELETE':
        pass
    return "TEST"
if __name__ == "__main__":
    portF = 8000
    hostF = "0.0.0.0"

    managerdb = Manager.create(
                        ipManager = LOCAL_HOST,
                        portManager = portF,
                        registerTime = datetime.now()
    )
    IoTmaganer.run(host = hostF, port = portF, debug=True, use_reloader=False)
