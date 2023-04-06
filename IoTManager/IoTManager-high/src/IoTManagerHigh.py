from flask import *
import socket, requests, json
from datetime import datetime
from DBManagerHigh import ManagerHighFather, ManagerHighSons, treeEndress

import psutil

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
my_eip = s.getsockname()[0]
nics = psutil.net_if_addrs()
my_enic = [i for i in nics for j in nics[i]
           if j.address == my_eip and j.family == socket.AF_INET][0]
print('[MANAGER-HIGH]:\t\t\tEthernet NIC name is {0}\n\t\t\t\tIPv4 address is {1}.'.format(
    my_enic, my_eip))
LOCAL_HOST = format(my_eip)


FORMAT = 'utf-8'

IoTmaganer = Flask(__name__)

@IoTmaganer.route('/',methods =['GET', 'POST', 'DELETE'])
def IoTmanager():
    localName = treeEndress.get()
    fullLoc = f"{localName.parent}/{localName.name}"
    if request.method == 'GET':
        return render_template("IoTManagerHigh.html",loc=fullLoc)
    if request.method == 'POST':
        headers= {'Content-type': 'application/json',}

        ipSon = request.form.get("m_son_ip")
        portSon = request.form.get("m_son_port")
        descSon = request.form.get("m_son_desc")

        ipFather = request.form.get("m_father_ip")
        portFather = request.form.get("m_father_port")
        descFather = request.form.get("m_father_desc") 

        print(f"[MANAGER_HIGH]:\tCadastrando {ipSon}:{portSon} ...")
        if(ipSon!= None and portSon!=None):
            managerdb = ManagerHighSons.create(
                        ipManager = ipSon,
                        portManager = portSon,
                        description = descSon,
                        registerTime = datetime.now()
            )
            
            print(f"[MANAGER_HIGH]:\tConectando com {ipSon}:{portSon} ... ")
            msg = {
                    "ip":LOCAL_HOST,
                    "port": portF,
                    "description":managerDescription,
                    "parentLoc": fullLoc
                } 
            try:
                requests.post (f'http://{ipSon}:{portSon}/setupfather', data = json.dumps(msg),headers=headers)
                print(f"[MANAGER_HIGH]:\tPOST \"http://{ipSon}:{portSon}/setupfather\" realizado")
            except:
                print(f"[MANAGER_HIGH]:\tERRO ao cadastrando Filho em: \"http://{ipSon}:{portSon}/setupfather\"")

        

    return render_template("IoTManagerHigh.html", loc=fullLoc)
    

@IoTmaganer.route('/sons',methods =['GET', 'POST'])
def sons():
    if request.method == 'GET':
        headers = ("ID","IP","Port","Description","RegisterTime")
        try:
            print("[MANAGER_HIGH]:\tConsultando Resources em /sons")
            resources = ManagerHighSons.select()
        except:
            print("[MANAGER_HIGH]:\tERRO no processo de consulta do Resource em /sons")
        else:
            return render_template("table_enviar.html", headings=headers, data=resources)
        
    if request.method == 'POST':
        id = request.form.get('id')
        port = request.form.get('port')
        ip = request.form.get('ip')
        row = request.form.get('row')
        print(id)
        print(ip)
        print(port)
        #print(row)
        return redirect(f"http://{ip}:{port}")

@IoTmaganer.route('/father',methods =['GET', 'POST'])  
def father():
    
    if request.method == 'GET':
        headers = ("ID","IP","Port","Description","Register Time","Last Update","Unregister Time")
        try:
            print("[MANAGER_HIGH]:\tConsultando Resources em /father")
            resources = ManagerHighFather.select()
        except:
            print("[MANAGER_HIGH]:\tERRO no processo de consulta do Resource em /father")
        else:
            return render_template("table_enviar.html", headings=headers, data=resources)
        
    if request.method == 'POST':
        id = request.form.get('id')
        port = request.form.get('port')
        ip = request.form.get('ip')
        row = request.form.get('row')
        print(id)
        print(ip)
        print(port)
        #print(row)
        return redirect(f"http://{ip}:{port}")
    

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
                loc = treeEndress.get()
                loc.parent = p_loc
                loc.save()
                print("[MANAGER_HIGH]:\tUpdating Father")
                query = ManagerHighFather.get()
                if(query.ipManager == ipFather and query.portManager == portFather):
                    query.lastUpdateTime = datetime.now()
                    query.description = descFather
                else:
                    managerdb = ManagerHighFather.create(
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
        
    


if __name__ == "__main__":
    portF = 9091
    hostF = "0.0.0.0"
    print(f"\t\t\t\tThe port used is {portF}")
    temp = input("\n[MANAGER-HIGH]:\t\t\tDo you like to change de port?\n\t\t\t\tPress ENTER to NO or enter with the PORT NUMBER to YES: ")
    if(temp != "" and temp.isdigit()):
        portF = int(temp)
        print(f"\t\t\t\tThe port used now is {portF}")
    else:
        print(f"\t\t\t\tThe port used is {portF}")
    managerDescription = input("[MANAGER-HIGH]:\t\t\tDescriçao do Manager High: ")
    treeLoc = input("[MANAGER-HIGH]:\t\t\tNome para localização na árvore: ")
    treeEndress .create(
        name = treeLoc
    )
    


    ####TEST##### remover
    if False:
        managerdb = ManagerHighSons.create(
                            ipManager = LOCAL_HOST,
                            portManager = portF,
                            description = managerDescription,
                            registerTime = datetime.now()
        )
    ####TEST end
    
    IoTmaganer.run(host = hostF, port = portF, debug=True, use_reloader=False)
