from flask import *
import socket, requests, json
from datetime import datetime
from IoTDirectoryService import Virtualizer, Gateway, Manager, ManagerFather


LOCAL_HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

IoTmaganer = Flask(__name__)
@IoTmaganer.route('/',methods =['GET', 'POST', 'DELETE'])
def IoTmanager():
    if request.method == 'GET':
        return render_template("IoTmanager.html")
    if request.method == 'POST':

    # Consultar Dados
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

    # Registrar no virtualizer 
        #capabilites
        capabiliteAddr              = request.form.get("capabilite_addr")
        capabiliteNome              = request.form.get("capabilite_nome")
        capabiliteDescription       = request.form.get("capabilite_description")
        capabiliteCapabilityType    = request.form.get("capabilite_capability_type")
        capabiliteAssociation       = request.form.get("capabilite_association")
        headers= {'Content-type': 'application/json',}

        if(True):
            print(f"[MANAGER]:\tCadastrando {capabiliteNome}")
            msg = {
                "name":capabiliteNome,
                "description":capabiliteDescription,
                "capability_type":capabiliteCapabilityType,
                "association": capabiliteAssociation 
	        }
            try:
                requests.post (f'http://{capabiliteAddr}/capabilities', data = json.dumps(msg),headers=headers)
            except:
                print(f"[MANAGER]:\tNão foi possivel cadastrar {capabiliteNome}")
                erroMsg1 = f"[MANAGER]:\tNão foi possivel cadastrar {capabiliteNome}"
                      #redirect(url_for('gateway_uuid',host=gatewayHost))
                return redirect(url_for('erro_m',erroMsg=erroMsg1))

        #recurso
        recursoUUID     = request.form.get("recurso_uuid")
        sensorCap1      = request.form.get("sensor_cap1")
        sensorCap2      = request.form.get("sensor_cap2")
        sensorStatus    = request.form.get("sensor_status")
        sensorLat       = request.form.get("sensor_lat")
        sensorLon       = request.form.get("sensor_lon")


        
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
    
@IoTmaganer.route('/father')  
def father():
    headers = ("id","IpManager","PortManager","Description","Register Time","Last Update","Unregister Time")
    try:
        print("[MANAGER_HIGH]:\tConsultando Resources em /father")
        resources = ManagerFather.select()
    except:
        print("[MANAGER_HIGH]:\tERRO no processo de consulta do Resource em /father")
    else:
        return render_template("table.html", headings=headers, data=resources)
    
    
@IoTmaganer.route('/setupfather',methods =['GET', 'POST', 'DELETE'])
def setupfather():
    if request.method == 'POST':

        try:
            data = request.get_json()

            ipFather = data["ip"]
            portFather = data["port"]
            descFather = data["description"]
            
            try:
                print("[MANAGER_HIGH]:\tUpdating Father")
                query = ManagerFather.get()
                if(query.ipManager == ipFather and query.portManager == portFather):
                    query.lastUpdateTime = datetime.now()
                    query.description = descFather
                else:
                    managerdb = ManagerFather.create(
                        ipManager = query.ipManager,
                        portManager = query.portManager,
                        description = query.description,
                        registerTime = query.registerTime,
                        lastUpdateTime = query.lastUpdateTime,
                        unregisterTime = datetime.now()
                    )
                    query.ipManager = ipFather
                    query.portManager = portFather
                    query.description = descFather
                    query.lastUpdateTime = None
                    query.registerTime = datetime.now()
                    query.save()
            except:
                print("[MANAGER_HIGH]:\tERRO ao atualizar Father")

        except:
            print(f"[MANAGER_HIGH]:\tERRO ao receber cadastro do Pai")

    return redirect(url_for('father'))

@IoTmaganer.route('/erro')
def erro_m(erroMsg):
    erroMsg = "<h1>ERRO</h1>"
    return erroMsg

if __name__ == "__main__":
    portF = 9000
    hostF = "0.0.0.0"

    managerdb = Manager.create(
                        ipManager = LOCAL_HOST,
                        portManager = portF,
                        registerTime = datetime.now()
    )
    IoTmaganer.run(host = hostF, port = portF, debug=True, use_reloader=False)
