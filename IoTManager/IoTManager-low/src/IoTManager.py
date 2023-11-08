from flask import *
import socket, requests, json
from datetime import datetime
from IoTDirectoryService import *
from IoTCreateVirtualizer import *
from playhouse.shortcuts import model_to_dict, dict_to_model
import sys, os, math

import psutil

portF = 9000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
my_eip = s.getsockname()[0]
nics = psutil.net_if_addrs()
my_enic = [i for i in nics for j in nics[i]
           if j.address == my_eip and j.family == socket.AF_INET][0]
print('\033[1m[MANAGER-LOW]:\033[0m\t\t\tEthernet NIC name is {0}\n\t\t\t\tIPv4 address is {1}.'.format(
    my_enic, my_eip))
LOCAL_HOST = format(my_eip)

FORMAT = 'utf-8'

IoTmaganer = Flask(__name__)
@IoTmaganer.route('/',methods =['GET', 'POST', 'DELETE'])
def IoTmanager():
    localName = treeAddress.get()
    fullLoc = f"{localName.parent}/{localName.name}"
    if request.method == 'GET':
        return render_template("IoTManager.html", loc=fullLoc)
    if request.method == 'POST':

    # Consultar Dados
        virtualizerHost = request.form.get("virtualizerHost")
        gatewayHost = request.form.get("gatewayHost")
        print(f"\033[1m[MANAGER-LOW]:\033[0m\tMethod = POST, virtualizerHost = {virtualizerHost}")
        print(f"\033[1m[MANAGER-LOW]:\033[0m\tMethod = POST, gatewayHost = {gatewayHost}")
        if(gatewayHost  != None):
            print(f"\033[1m[MANAGER-LOW]:\033[0m\tRedirect to /gateway/{gatewayHost}")
            return redirect(url_for('gateway_uuid',host=gatewayHost))
        if(virtualizerHost  != None):
            print(f"\033[1m[MANAGER-LOW]:\033[0m\tRedirect to /virtualizer/{virtualizerHost}")
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
            print(f"\033[1m[MANAGER-LOW]:\033[0m\tCadastrando {capabiliteNome}")
            msg = {
                "name":capabiliteNome,
                "description":capabiliteDescription,
                "capability_type":capabiliteCapabilityType,
                "association": capabiliteAssociation 
	        }
            try:
                requests.post (f'http://{capabiliteAddr}/capabilities', data = json.dumps(msg),headers=headers)
            except:
                print(f"\033[1m[MANAGER-LOW]:\033[0m\tNão foi possivel cadastrar {capabiliteNome}")
                erroMsg1 = f"\033[1m[MANAGER-LOW]:\033[0m\tNão foi possivel cadastrar {capabiliteNome}"
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

@IoTmaganer.route('/virtualizer',methods =['GET', 'POST'])
def virtualizer():
    if request.method == 'GET':
        headers = ("id","ipVirtualizer","portVirtualizer","registerTime")
        try:
            print("\033[1m[MANAGER-LOW]:\033[0m\tConsultando Resources em /virtualizer")
            resources = Virtualizer.select()
        except:
            print("\033[1m[MANAGER-LOW]:\033[0m\tERRO no processo de consulta do Resource em /virtualizer")
        else:
            return render_template("table.html", headings=headers, data=resources)

@IoTmaganer.route('/gateway',methods =['GET', 'POST'])
def gateway():
    if request.method == 'GET':
        headers = ("id","ipGateway","portGateway","registerTime")
        try:
            print("\033[1m[MANAGER-LOW]:\033[0m\tConsultando Resources em /gateway")
            resources = Gateway.select()
        except:   
            print("\033[1m[MANAGER-LOW]:\033[0m\tERRO no processo de consulta do Resource em /gateway")
        else:
            return render_template("table.html", headings=headers, data=resources)
    if request.method == 'POST':
        id = request.form.get('id')
        port = request.form.get('port')
        ip = request.form.get('ip')
        row = request.form.get('row')
        return redirect(f"http://{ip}:{port}")
    

@IoTmaganer.route('/manager',methods =['GET', 'POST'])
def manager():
    if request.method == 'GET':
        headers = ("id","ipManager","portManager","registerTime")
        try:
            print("\033[1m[MANAGER-LOW]:\033[0m\tConsultando Resources em /manager")
            resources = Manager.select()
        except:
            print("\033[1m[MANAGER-LOW]:\033[0m\tERRO no processo de consulta do Resource em /manager")
        else:
            return render_template("table.html", headings=headers, data=resources)
    if request.method == 'POST':
        id = request.form.get('id')
        port = request.form.get('port')
        ip = request.form.get('ip')
        row = request.form.get('row')
        return redirect(f"http://{ip}:{port}")
    
@IoTmaganer.route('/father',methods =['GET', 'POST'])  
def father():
    if request.method == 'GET':

        headers = ("id","IpManager","PortManager","Description","Register Time","Last Update","Unregister Time")
        try:
            print("[MANAGER_LOW]:\tConsultando Resources em /father")
            resources = ManagerFather.select()
        except:
            print("[MANAGER_LOW]:\tERRO no processo de consulta do Resource em /father")
        else:
            return render_template("table.html", headings=headers, data=resources)
    if request.method == 'POST':
        id = request.form.get('id')
        port = request.form.get('port')
        ip = request.form.get('ip')
        row = request.form.get('row')
        return redirect(f"http://{ip}:{port}")
    
@IoTmaganer.route('/allfather',methods =['GET','DELETE'])
def getFather():
    if request.method == 'GET':
        headers= {'Content-type': 'application/json',}
        data = []
        query = ManagerFather.select().paginate(1, ManagerFather.select().count())
        for i in query:
            data.append(model_to_dict(i))
        print(json.dumps(data, indent=4,sort_keys=True, default=str))

        return json.dumps(data, indent=4, sort_keys=True, default=str)
    if request.method == 'DELETE':
        query = ManagerFather.select().paginate(1, ManagerFather.select().count())
        for i in query:
            i.delete_instance()
        return jsonify({"@message":"ALL DELETED"})


    
@IoTmaganer.route('/virtualizer/<string:host>',methods =['GET','DELETE'])
def virtualizer_uuid(host):
    if request.method == 'GET':
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
    if request.method == 'DELETE':
        try:
            hostT = host.split(":")
            query = Virtualizer.select().where(Virtualizer.ipVirtualizer == hostT[0],Virtualizer.portVirtualizer ==hostT[1]).get()
            msg={
                "@message":"DELETED",
                "id":query.id,
                "ip":query.ipVirtualizer,
                "port":query.portVirtualizer,
                "registered":query.registerTime
            }
            query.delete_instance()
            return jsonify(msg)

        except:
            return jsonify({"@message":"ERROR"})
    

@IoTmaganer.route('/gateway/<string:host>', methods =['GET','DELETE'])
def gateway_uuid(host):
    if request.method == 'GET':
        try:
            exit = f"<h1>Gateway ({host})</h1> <div style=\"float:left;padding: 10px;\"><h3>Sensor:</h3>"
            host = f"http://{host}"
            r = requests.get(url = f"{host}/resources")
            exit +=r.text
            return exit
        except:
            return f"<h1>ERRO:</h1> <h2>Virtualizador ({host}) não existe ou esta offline</h2>"
    
    if request.method == 'DELETE':
        try:
            hostT = host.split(":")
            query = Gateway.select().where(Gateway.ipGateway == hostT[0],Gateway.portGateway ==hostT[1]).get()
            msg={
                "@message":"DELETED",
                "id":query.id,
                "ip":query.ipGateway,
                "port":query.portGateway,
                "registered":query.registerTime
            }
            query.delete_instance()
            return jsonify(msg)

        except:
            return jsonify({"@message":"ERROR"})
    

        
@IoTmaganer.route('/setupfather',methods =['GET', 'POST', 'DELETE'])
def setupfather():
    if request.method == 'POST':
        try:
            data = request.get_json()

            ipFather = data["ip"]
            portFather = data["port"]
            descFather = data["description"]
            p_loc = data["parentLoc"]
                        
            try:
                loc = treeAddress.get(treeAddress.id == 1)
                loc.parent = p_loc
                loc.save()
                print("[MANAGER_LOW]:\tUpdating Father")
                
                try:
                    query = ManagerFather.get(
                            (ManagerFather.id == 1)
                        )
                except ManagerFather.DoesNotExist:
                    query = ManagerFather.create(
                        ipManager = ipFather,
                        portManager = portFather,
                        description = descFather
                    )
                else:
                    if(query.ipManager == ipFather and query.portManager == str(portFather)):
                        query.description = descFather
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
                localName = treeAddress.get()
                print(f"mandando repouse = {localName.name}")
                return localName.name
            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()

                print("[MANAGER_LOW]:\tERRO ao atualizar Father", error)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)    
        except:
            print(f"[MANAGER_LOW]:\tERRO ao receber cadastro do Pai")

    return "@erro404"

@IoTmaganer.route('/erro')
def erro_m(erroMsg):
    erroMsg = "<h1>ERRO</h1>"
    return erroMsg

@IoTmaganer.route('/search',methods =['POST','GET'])
def search():
    if request.method == 'GET':
        virtualizers = []
        gateways = []
        query = Virtualizer.select().paginate(1, Virtualizer.select().count())
        for i in query:
            virtualizers.append(model_to_dict(i))
        query = Gateway.select().paginate(1, Gateway.select().count())
        for i in query:
            gateways.append(model_to_dict(i))

        localName = treeAddress.get()
        fullLoc = f"{localName.parent}/{localName.name}"
        response = {
            "Manager address": fullLoc,
            "addr": f"{LOCAL_HOST}:{portF}",
            "Virtualizers": virtualizers,
            "Gateways": gateways
        }
        if 'datetime' in response:
            response['datetime'] = response['datetime'].strftime('%Y-%m-%d %H:%M:%S')
        json_data = json.dumps(response, cls=DateTimeEncoder, indent=4, sort_keys=True)
        print(json_data)
        response = Response(json_data, content_type='application/json')
        return response

    if request.method == 'POST':
        localName = treeAddress.get()
        #curl http://172.24.219.147:8000/search -d "/a"
        fullLoc = f"{localName.parent}/{localName.name}"
        #fullLoc = "a/b/d"
        fullLoc = fullLoc.split("/")

        entrada = request.get_data().decode('utf-8')
        add = entrada.split("/")

        if(fullLoc == add):
            print(f"{fullLoc} == {add}")
            virtualizers = []
            gateways = []
            query = Virtualizer.select().paginate(1, Virtualizer.select().count())
            for i in query:
                virtualizers.append(model_to_dict(i))
            query = Gateway.select().paginate(1, Gateway.select().count())
            for i in query:
                gateways.append(model_to_dict(i))

            localName = treeAddress.get()
            fullLoc = f"{localName.parent}/{localName.name}"
            response = {
                "Manager address": fullLoc,
                "addr": f"{LOCAL_HOST}:{portF}",
                "Virtualizers": virtualizers,
                "Gateways": gateways
            }
            if 'datetime' in response:
                response['datetime'] = response['datetime'].strftime('%Y-%m-%d %H:%M:%S')
            json_data = json.dumps(response, cls=DateTimeEncoder, indent=4, sort_keys=True)
            print(json_data)
            response = Response(json_data, content_type='application/json')
            return response
        
        else:
            print(f"{fullLoc} != {add}")
            pai = ManagerFather.get(ManagerFather.id == 1)
            print(f'POST http://{pai.ipManager}:{pai.portManager}/search -d {entrada}')
            response = requests.post (f'http://{pai.ipManager}:{pai.portManager}/search', data = entrada)
            response = Response(response, content_type='application/json')
            return response

@IoTmaganer.route('/AutoSetVirtualizer',methods =['POST'])
def AutoSetVirtualizer():
    if request.method == 'POST':  
        #curl -X POST -H "Content-Type: application/json" -d @testautosetvit.json http://172.24.219.147:9000/AutoSetVirtualizer


        Json = request.get_json()
        Sensors = Json["sensors"]
        Capabilities = Sensors["capabilities"]
        print(Json)

        if Json["rules"]["type"] == "latency-precision":
            latencyPrecision(Json)
        

        #### TESTE REMOVER 
        listUrl = []
        for Cap in Json["sensors"]["capabilities"]:
            listUrl.append(Cap["addr"])

        #BetterUrl = latencyTest(listUrl)

        for Cap in Capabilities:
            msg = {
                "name":Cap["name"],
                "description":Cap["description"],
                "capability_type":Cap["capability_type"],
                "association": Cap["association"], 
            }
            #cadastrarCap(msg,BetterUrl)

        msg = {
            "regInfos": Json["sensors"]["resources"],
            "realSensors":[{"uuid":"709fd3e3-4112-46f4-b148-4778775998e7","capabilities":["temperature","pressure"]}]
        }
        #cadastrarRec(msg,BetterUrl)
        return "ok"

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)


if __name__ == "__main__":

    hostF = "0.0.0.0"
    print(f"\t\t\t\tThe port used is {portF}")
    temp = input("\n\033[1m[MANAGER-LOW]:\033[0m\t\t\tDo you like to change de port?\n\t\t\t\tPress ENTER to NO or enter with the PORT NUMBER to YES: ")

    if(temp != "" and temp.isdigit()):
        portF = int(temp)
        print(f"\t\t\t\tThe port used now is {portF}")
    else:
        print(f"\t\t\t\tThe port used is {portF}")
    
    managerdb = Manager.create(
                        ipManager = LOCAL_HOST,
                        portManager = portF,
                        registerTime = datetime.now()
    )
    treeLoc = input("\033[1m[MANAGER-LOW]:\033[0m\t\t\tNome para localização na árvore: ")

    try:
        query  = treeAddress.get(treeAddress.id == 1)
        treeAddress.create(
            name = query.name,
            parent = query.parent,
            registerTime = query.registerTime,
            unregisterTime = datetime.now()
        )
        query.name = treeLoc
        query.parent = ""
        query.registerTime = datetime.now()
        query.save()
    except treeAddress.DoesNotExist:
        query = treeAddress.create(name = treeLoc)

    x = sendIpToDs(portF)
    print(f"[MANAGER_LOW]:\t\t\tIniciando Flask . . .\n\n\033[1m---------------------------------------FLASK---------------------------------------\033[0m")
    IoTmaganer.run(host = LOCAL_HOST, port = portF, debug=True, use_reloader=False)
