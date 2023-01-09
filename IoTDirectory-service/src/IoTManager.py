from flask import *
import socket, requests, json
from datetime import datetime
from IoTDirectoryService import Virtualizer, Gateway, Manager

LOCAL_HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

IoTmaganer = Flask(__name__)
@IoTmaganer.route('/',methods =['GET', 'POST', 'DELETE'])
def IoTmanager():
    if request.method == 'GET':
        return render_template("IoTmanager.html")
    if request.method == 'POST':
        virtualizerHost = request.form.get("virtualizerHost")
        gatewayHost = request.form.get("gatewayHost")
        print(f"[MANAGER]:\tMethod = POST, virtualizerHost = {virtualizerHost}")
        print(f"[MANAGER]:\tMethod = POST, gatewayHost = {gatewayHost}")
        if(gatewayHost  != None):
            print(f"[MANAGER]:\tRedirect to /gateway/{gatewayHost}")
            return redirect(url_for('gateway_uuid',host=gatewayHost))
        if(virtualizerHost  != None):
            print(f"[MANAGER]:\tRedirect to /virtualizer/{virtualizerHost}")
            return redirect(url_for('virtualizer_uuid',host=virtualizerHost))
    return render_template("IoTmanager.html")

@IoTmaganer.route('/virtualizer')
def virtualizer():
    headers = ("id","ipVirtualizer","portVirtualizer","registerTime")
    try:
        print("[MANAGER]:\tConsultando Resources em /virtualizer")
        resources = Virtualizer.select()
    except:
        print("[MANAGER]:\tERRO no processo de consulta do Resource em /virtualizer")
    else:
        return render_template("table.html", headings=headers, data=resources)

@IoTmaganer.route('/gateway')
def gateway():
    headers = ("id","ipGateway","portGateway","registerTime")
    try:
        print("[MANAGER]:\tConsultando Resources em /gateway")
        resources = Gateway.select()
    except:
        print("[MANAGER]:\tERRO no processo de consulta do Resource em /gateway")
    else:
        return render_template("table.html", headings=headers, data=resources)


@IoTmaganer.route('/manager')
def manager():
    headers = ("id","ipManager","portManager","registerTime")
    try:
        print("[MANAGER]:\tConsultando Resources em /manager")
        resources = Manager.select()
    except:
        print("[MANAGER]:\tERRO no processo de consulta do Resource em /manager")
    else:
        return render_template("table.html", headings=headers, data=resources)


@IoTmaganer.route('/virtualizer/<string:host>')
def virtualizer_uuid(host):
    try:
        exit = f"<h1>Virtualizador ({host})</h1> <div style=\"float:left;padding: 10px;\"><h3>Resources:</h3>"
        host = f"http://{host}"
        r = requests.get(url = f"{host}/resources")
        exit +=r.text
        exit += "</div><div style=\"float:left;padding: 10px;\"><h3>Capabilites:</h3>"
        r = requests.get(url = f"{host}/capabilities")
        exit +=r.text
        exit += "</div><div style=\"float:left;padding: 10px;\"><h3>Realsensors:</h3>"
        r = requests.get(url = f"{host}/realsensors")
        exit +=r.text
        exit += "</div><div style=\"float:left;padding: 10px;\"><h3>Data:</h3>"
        r = requests.get(url = f"{host}/data")
        exit +=r.text
        return exit
    except:
        return f"<h1>ERRO:</h1> <h2>Virtualizador ({host}) não existe ou esta offline</h2>"

@IoTmaganer.route('/gateway/<string:host>')
def gateway_uuid(host):
    try:
        exit = f"<h1>Gateway ({host})</h1> <div style=\"float:left;padding: 10px;\"><h3>Sensor:</h3>"
        host = f"http://{host}"
        r = requests.get(url = f"{host}/resources")
        exit +=r.text
        return exit
    except:
        return f"<h1>ERRO:</h1> <h2>Virtualizador ({host}) não existe ou esta offline</h2>"


if __name__ == "__main__":
    portF = 9000
    hostF = "0.0.0.0"

    managerdb = Manager.create(
                        ipManager = LOCAL_HOST,
                        portManager = portF,
                        registerTime = datetime.now()
    )
    IoTmaganer.run(host = hostF, port = portF, debug=True, use_reloader=False)
