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
        headers= {'Content-type': 'application/json',}

        ipSon = request.form.get("m_sons_ip")
        portSon = request.form.get("m_sons_port")
        descSon = request.form.get("m_sons_desc")

        ipFather = request.form.get("m_father_ip")
        portFather = request.form.get("m_father_port")
        descFather = request.form.get("m_father_desc")     
        

    return render_template("IoTManagerHigh.html")
    

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
    headers = ("id","IpManager","PortManager","Description","Register Time","Last Update","Unregister Time")
    try:
        print("[MANAGER_HIGH]:\tConsultando Resources em /father")
        resources = ManagerHighFather.select()
    except:
        print("[MANAGER_HIGH]:\tERRO no processo de consulta do Resource em /father")
    else:
        return render_template("table.html", headings=headers, data=resources)
    

@IoTmaganer.route('/setupfather',methods =['GET', 'POST', 'DELETE'])
def setupfather():
    if request.method == 'POST':
      
        ipFather = request.form.get("m_sons_ip")
        portFather = request.form.get("m_sons_port")
        descFather = request.form.get("m_sons_desc")

        try:
            print("[MANAGER_HIGH]:\tUpdating Father")
            query = ManagerHighFather.get()
            print(query.unregisterTime)
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
            print("[MANAGER_HIGH]:\tCreateing Father")
            managerdb = ManagerHighFather.create(
                ipManager = "test",
                portManager = "portF",
                description = "managerDescription",
                registerTime = datetime.now()
            )
            print("criador pai")
     

        
        return render_template("IoTManagerHigh.html")
    


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
