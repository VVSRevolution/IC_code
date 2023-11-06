from protocolClients import MqttClass
from protocolClients import CoapClass
from db import DB
from create_db import Sensors
import socket, threading, zmq, time
import psutil

from flask import Flask, request, jsonify, render_template
from flask.wrappers import Response

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
my_eip = s.getsockname()[0]
nics = psutil.net_if_addrs()
my_enic = [i for i in nics for j in nics[i]
           if j.address == my_eip and j.family == socket.AF_INET][0]
print('\033[1m[GATEWAY]:\033[0m\t\t\tEthernet NIC name is {0}\n\t\t\t\tIPv4 address is {1}.'.format(
    my_enic, my_eip))
LOCAL_HOST = format(my_eip)
FORMAT = 'utf-8'

app = Flask(__name__)

@app.route('/')
def index():
    return "HW"

@app.route('/virtualizers', methods=['GET', 'POST', 'DELETE']) # METODO INCOMPLETO 
def virtualizers():
    if request.method == 'GET':
        return "return all virtualizers addrs"
    if request.method == 'POST':
        try:
          data = request.get_json()
          db = DB()
          db.setVirtualizer(data["uuid"],data["addr"])
          return jsonify("{}")
        except:
            return "Erro no cadastro do virtualizador no IOTGateway"

@app.route('/sensor', methods=['GET']) # METODO INCOMPLETO 
def sensors():
    if request.method == 'GET':
        headers = ("id","local_id","uuid")
        try:
            print("[DB_SENSOR]:\tConsultando Resources")
            resources = Sensors.select()
        except:
            print("[DB_SENSOR]:\tERRO no processo de consulta do Resource")
        else:
            return render_template("table.html", headings=headers, data=resources)
        

def sendToDS(portF):
    
    print("\n-----------------------------------DIRECTORY SERVICE-----------------------------------\n")
    DShost = input("[GATEWAY]:\tEnter directory service host: ")
    DSport = input("[GATEWAY]:\tEnter directory service port: ")   
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://"+ DShost +":"+ DSport)

        socket.send_string(f"G${LOCAL_HOST}${portF}")
        msg = socket.recv().decode(FORMAT)
        print(msg)
    except:
        print("[GATEWAY]:\t ERROR ao mandar ADDR ao Directory Service ")

if __name__ == "__main__":

    mqttGateway = MqttClass('gateway1','soldier.cloudmqtt.com',10514,1,'test5')
    coapGateway = CoapClass()

    hostF = "0.0.0.0"
    portF = 8000

    #mqttGateway.startListening("ctuqpqym","Xk5GNcWqcmZG")
    #sthread_coap_server = coapGateway.startListening()
    #sthread_coap_client = coapGateway.requestSensorData()

    w1 = threading.Thread(target = mqttGateway.startListening, args=("ctuqpqym","Xk5GNcWqcmZG"))
    w1.start()

    #w2 = threading.Thread(target = coapGateway.startListening)
    #w3 = threading.Thread(target= coapGateway.requestSensorData)
    #w4 = threading.Thread(target = app.run) # Flask
    time.sleep(2)

    print("\n-----------------------------------------FLASK-----------------------------------------\n")
    threading.Thread(target=lambda: app.run(host = hostF, port = portF, debug=True, use_reloader=False)).start()
    #w4.start()
    
    sendDS = threading.Thread(target = sendToDS, args=(portF,))

    #w4.start()
    time.sleep(1)
    sendDS.start()

'''    while(1):
        coapGateway.requestSensorData()
        time.sleep(5)
'''