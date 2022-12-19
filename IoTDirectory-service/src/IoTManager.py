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
        pass
    if request.method == 'POST':
        pass

    return render_template("IoTmanager.html")

@IoTmaganer.route('/virtualizer')
def virtualizer():
    query = Virtualizer.select(Virtualizer.ipVirtualizer, Virtualizer.portVirtualizer)
    virtualizerData = ""
    for virtualizer in query:
        virtualizerData += f"{virtualizer.ipVirtualizer}:{virtualizer.portVirtualizer}\n"
        
    return render_template("Virtualizer.html",virtualizerData=virtualizerData)

@IoTmaganer.route('/virtualizer/<string:host>')
def virtualizer_uuid(host):
    try:
        #host = request.form.get("virtualizerHost")
        
        exit = f"<h1>Virtualizador ({host})</h1> <div style=\"float:left;padding: 10px;\"><h3>Resources:</h3>"
        host = f"http://{host}"
        #172.23.169.18:8000
        r = requests.get(url = f"{host}/resources")
        print(r.text)
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
        return f"<h1>ERRO:</h1> <h2>Virtualizador ({host}) não existe</h2>"

@IoTmaganer.route('/gateway')
def gateway():
    query = Gateway.select(Gateway.ipGateway, Gateway.portGateway)
    gatewayData = ""
    for gateway in query:
        gatewayData += f"{gateway.ipGateway}:{gateway.portGateway}\n"
    #gatewayData.encode('string_escape')
    return render_template("Gateway.html",gatewayData=gatewayData)

@IoTmaganer.route('/gateway/<string:host>')
def gateway_uuid(host):
    pass
@IoTmaganer.route('/manager')
def manager():
    query = Manager.select(Manager.id, Manager.ipManager, Manager.portManager, Manager.registerTime)
    managerData = ""
    for manager in query:
        managerData += f"{manager.id}\t{manager.ipManager}:{manager.portManager}\t{manager.registerTime}\n"
    #managerData.encode('string_escape')
    return render_template("Manager.html",managerData=managerData)

if __name__ == "__main__":
    portF = 9000
    hostF = "0.0.0.0"

    managerdb = Manager.create(
                        ipManager = LOCAL_HOST,
                        portManager = portF,
                        registerTime = datetime.now()
    )
    IoTmaganer.run(host = hostF, port = portF, debug=True, use_reloader=False)
