from flask import *
import socket, requests, json
from datetime import datetime
from DBManagerHigh import ManagerHigh 

LOCAL_HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

IoTmaganer = Flask(__name__)

@IoTmaganer.route('/',methods =['GET', 'POST', 'DELETE'])
def IoTmanager():
    return "TEsT"

if __name__ == "__main__":
    portF = 9090
    hostF = "0.0.0.0"

    managerDescription = input("[MANAGER-HIGH]\tDescriçao do Manager High: ")

    managerdb = ManagerHigh.create(
                        ipManager = LOCAL_HOST,
                        portManager = portF,
                        description = managerDescription,
                        registerTime = datetime.now()
    )
    IoTmaganer.run(host = hostF, port = portF, debug=True, use_reloader=False)
