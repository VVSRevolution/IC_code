from protocolClients import MqttClass
from protocolClients import CoapClass
from db import DB
import socket, threading, zmq, time

from flask import Flask, request, jsonify, render_template
from flask.wrappers import Response

LOCAL_HOST = socket.gethostbyname(socket.gethostname())
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