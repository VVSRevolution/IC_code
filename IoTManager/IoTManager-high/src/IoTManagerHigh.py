from flask import *
import socket, requests, json
from datetime import datetime
from DBManagerHigh import *
from playhouse.shortcuts import model_to_dict, dict_to_model
import sys, os


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

        # tenho q atualisar a descrisao, pois nao recebe o nome atualisado do pai 

        print(f"[MANAGER_HIGH]:\tCadastrando {ipSon}:{portSon} ...")
        if(ipSon!= None and portSon!=None):
            
            print(f"[MANAGER_HIGH]:\tConectando com {ipSon}:{portSon} ... ")
            msg = {
                    "ip":LOCAL_HOST,
                    "port": portF,
                    "description":managerDescription,
                    "parentLoc": fullLoc
                } 
            try:
                respose = requests.post (f'http://{ipSon}:{portSon}/setupfather', data = json.dumps(msg),headers=headers)
                print(f"Retorno = {respose.text}")
                if(respose.text != "@erro404"):
                    print(f"[MANAGER_HIGH]:\tPOST \"http://{ipSon}:{portSon}/setupfather\" realizado")
                    managerdb = ManagerHighSons.create(
                            ipManager = ipSon,
                            portManager = portSon,
                            description = descSon,
                            nameinTree = respose.text,
                            registerTime = datetime.now()
                    )
                else:
                    print(f"[MANAGER_HIGH]:\tERRO ao cadastrando Filho em: \"http://{ipSon}:{portSon}/setupfather\"")

            except:
                print(f"[MANAGER_HIGH]:\tERRO ao cadastrando Filho em: \"http://{ipSon}:{portSon}/setupfather\"")

        
    #return fullLoc
    return render_template("IoTManagerHigh.html", loc=fullLoc)
    

@IoTmaganer.route('/sons',methods =['GET', 'POST'])
def sons():
    if request.method == 'GET':
        headers = ("ID","IP","Port","Description","Nome na árvore","RegisterTime")
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
                loc = treeEndress.get(treeEndress.id == 1)
                loc.parent = p_loc
                loc.save()
                print("[MANAGER_HIGH]:\tUpdating Father")
                
                try:
                    query = ManagerHighFather.get(
                            (ManagerHighFather.ipManager == ipFather) and
                            (ManagerHighFather.portManager == portFather)
                        )
                except ManagerHighFather.DoesNotExist:
                    query = ManagerHighFather.create(
                        ipManager = ipFather,
                        portManager = portFather
                    )
                
                if(query.ipManager == ipFather and query.portManager == str(portFather)):
                    query.description = descFather
                    query.lastUpdateTime = datetime.now()
                    query.description = descFather
                else:
                    managerdb = ManagerHighFather.create(
                        ipManager = query.ipManager,
                        portManager = query.portManager,
                        description = query.description,
                        registerTime = query.registerTime,
                        lastUpdateTime = query.lasuttUpdateTime,
                        unregisterTime = datetime.now()
                    )
                    query.ipManager = ipFather
                    query.portManager = portFather
                    query.description = descFather
                    query.lastUpdateTime = None
                    query.registerTime = datetime.now()
                query.save()
                localName = treeEndress.get()
                print(f"mandando repouse = {localName.name}")
                return localName.name
            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()

                print("[MANAGER_HIGH]:\tERRO ao atualizar Father", error)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)    
        except:
            print(f"[MANAGER_HIGH]:\tERRO ao receber cadastro do Pai")

    return "@erro404"

@IoTmaganer.route('/allfather',methods =['GET','DELETE'])
def getFather():
    if request.method == 'GET':
        headers= {'Content-type': 'application/json',}
        data = []
        query = ManagerHighFather.select().paginate(1, ManagerHighFather.select().count())
        for i in query:
            data.append(model_to_dict(i))
        print(json.dumps(data, indent=4,sort_keys=True, default=str))

        return json.dumps(data, indent=4, sort_keys=True, default=str)
    if request.method == 'DELETE':
        query = ManagerHighFather.select().paginate(1, ManagerHighFather.select().count())
        for i in query:
            i.delete_instance()
        return jsonify({"@message":"ALL DELETED"})


@IoTmaganer.route('/allsons',methods =['GET','DELETE'])
def getSons():
    if request.method == 'GET':
        headers= {'Content-type': 'application/json',}
        data = []
        query = ManagerHighSons.select().paginate(1, ManagerHighSons.select().count())
        for i in query:
            data.append(model_to_dict(i))
        print(json.dumps(data, indent=4,sort_keys=True, default=str))

        return json.dumps(data, indent=4, sort_keys=True, default=str)
    if request.method == 'DELETE':
        query = ManagerHighSons.select().paginate(1, ManagerHighSons.select().count())
        for i in query:
            i.delete_instance()
        return jsonify({"@message":"ALL DELETED"})

    
@IoTmaganer.route('/son/<string:idd>',methods =['GET','DELETE'])
def deleteSons(idd):
    if request.method == 'GET':
        try:
            query = ManagerHighSons.select().where(ManagerHighSons.id == idd).get()
            msg={
                "id":query.id,
                "ip":query.ipManager,
                "port":query.portManager,
                "descripition":query.description,
                "registered":query.registerTime
            }
            return jsonify(msg)

        except:
            return jsonify({"@message":"ERROR"})
    if request.method == 'DELETE':
        try:
            query = ManagerHighSons.select().where(ManagerHighSons.id == idd).get()
            msg={
                "@message":"DELETED",
                "id":query.id,
                "ip":query.ipManager,
                "port":query.portManager,
                "descripition":query.description,
                "registered":query.registerTime
            }
            query.delete_instance()
            return jsonify(msg)

        except:
            return jsonify({"@message":"ERROR"})
    
@IoTmaganer.route('/alltreehistory',methods =['GET','DELETE'])
def getTree():
    if request.method == 'GET':
        headers= {'Content-type': 'application/json',}
        data = []
        query = treeEndress.select().paginate(1, treeEndress.select().count())
        for i in query:
            data.append(model_to_dict(i))
        print(json.dumps(data, indent=4,sort_keys=True, default=str))

        return json.dumps(data, indent=4, sort_keys=True, default=str)

    if request.method == 'DELETE':
        query = treeEndress.select().paginate(1, treeEndress.select().count())
        for i in query:
            i.delete_instance()
        return jsonify({"@message":"ALL DELETED"})

@IoTmaganer.route('/getVirtualizers',methods =['POST'])
def getVirtualizers():
    localName = treeEndress.get()
    #curl http://172.24.219.147:9091/getVirtualizers -d "a/b/c/d/e"
    fullLoc = f"{localName.parent}/{localName.name}"
    #fullLoc = "a/b/d"
    fullLoc = fullLoc.split("/")

    entrada = request.get_data().decode('utf-8')
    add = entrada.split("/")

    if(len(fullLoc)>len(add)):
        print("post")
        pai = ManagerHighFather.get()
        
        requests.post (f'http://{pai.ipManager}:{pai.portManager}/getVirtualizers', data = entrada)
        print("post")
        return "ir para o pai"
        
    
    count = 0
    for i in range(len(fullLoc)):
        if(fullLoc[i] == add[i]):
            count=count+1
        else:
            break
    print(f"Parrou no {count}")

    if(count < len(add) and count == len(fullLoc)):
        return f"ir para o filho {add[count]}"
    else:
        return "ir para o pai"


#main
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

    try:
        query  = treeEndress.get(treeEndress.id == 1)
        treeEndress.create(
            name = query.name,
            parent = query.parent,
            registerTime = query.registerTime,
            unregisterTime = datetime.now()
        )
        query.name = treeLoc
        query.parent = ""
        query.registerTime = datetime.now()
        query.save()
    except treeEndress.DoesNotExist:
        query = treeEndress.create(name = treeLoc)

    

    
    IoTmaganer.run(host = hostF, port = portF, debug=True, use_reloader=False)
