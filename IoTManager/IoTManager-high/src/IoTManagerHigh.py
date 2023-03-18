from flask import *
import socket, requests, json
from datetime import datetime
from DBManagerHigh import ManagerHighFather, ManagerHighSons

LOCAL_HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

IoTmaganer = Flask(__name__)

@IoTmaganer.route('/',methods =['GET', 'POST', 'DELETE'])
def IoTmanager():
    if request.method == 'GET':
        return render_template("IoTManagerHigh.html")
    if request.method == 'POST':
        return render_template("IoTManagerHigh.html")
    return "TEsT"

@IoTmaganer.route('/sons')
def sons():
    headers = ("id","ipManager","portManager","description","registerTime")
    try:
        print("[MANAGER_HIGH]:\tConsultando Resources em /sons")
        resources = ManagerHighSons.select()
    except:
        print("[MANAGER_HIGH]:\tERRO no processo de consulta do Resource em /sons")
    else:
        return render_template("table.html", headings=headers, data=resources)

@IoTmaganer.route('/father')  
def father():
    headers = ("id","ipManager","portManager","registerTime")
    try:
        print("[MANAGER_HIGH]:\tConsultando Resources em /father")
        resources = ManagerHighFather.select()
    except:
        print("[MANAGER_HIGH]:\tERRO no processo de consulta do Resource em /father")
    else:
        return render_template("table.html", headings=headers, data=resources)

if __name__ == "__main__":
    portF = 9090
    hostF = "0.0.0.0"
    managerDescription = input("[MANAGER-HIGH]\tDescriçao do Manager High: ")


    ####TEST##### remover
    managerdb = ManagerHighSons.create(
                        ipManager = LOCAL_HOST,
                        portManager = portF,
                        description = managerDescription,
                        registerTime = datetime.now()
    )
    ####TEST end

    IoTmaganer.run(host = hostF, port = portF, debug=True, use_reloader=False)
