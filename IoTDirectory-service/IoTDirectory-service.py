import peewee,zmq,socket,threading
from datetime import datetime

FORMAT = 'utf-8'
PORT = 808080
HOST = socket.gethostbyname(socket.gethostname())
HOST = "127.0.1.1" #just for test <------------------- REMOVE THIS LINE

db = peewee.SqliteDatabase('IoTDirectory-service/database_ds.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Virtualizer(BaseModel):
    ipVirtualizer = peewee.TextField(default=None)
    portVirtualizer = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())

class Gateway(BaseModel):
    ipGateway = peewee.TextField(default=None)
    portGateway = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())

try:
    db.create_tables([
        Virtualizer,
        Gateway    
    ])
    print("[DATABASE]:\t[OK] ao criar tabela")
except:
    print("[DATABASE]:\t[ERRO] ao criar tabela")


def sendIp(): # envia os ADDR dos virtualizers e geteways
    context = zmq.Context()
    s = context.socket(zmq.PUB)
    PortSend = str(PORT + 1)
    p = f"tcp://{(HOST)}:{PortSend}"
    print(f"[DIRECTORY SERVICE]:\t Mandando dados em {p}")
    s.bind(p)

    query = Virtualizer.select(Virtualizer.ipVirtualizer, Virtualizer.portVirtualizer)
    virtualizerData = ""
    for virtualizer in query:
        virtualizerData += f"{virtualizer.ipVirtualizer}:{virtualizer.portVirtualizer}\n"

    query = Gateway.select(Gateway.ipGateway, Gateway.portGateway)
    gatewayData = ""
    for gateway in query:
        gatewayData += f"{gateway.ipGateway}:{gateway.portGateway}\n"

    #testar saida de dados 
    #print(virtualizerData) 
    #print(gatewayData)


    s.send_string("virtualizer" + virtualizerData)
    s.send_string("gateway" + gatewayData)


def getIp(): # recebe os ADDR dos virtualizers e geteways
    context = zmq.Context()
    socket = context.socket(zmq.REP)   
    p = "tcp://"+ HOST +":"+ str(PORT)
    print(f"[DIRECTORY SERVICE]:\t Recebendo dados em {p}")
    socket.bind(p)

    while True:
        message = socket.recv().decode(FORMAT)
        print("Received request: %s" % message)
        try:

            data = message.split("$")
            ip = data[1]
            port = data[2]
        
        
            if(data[0].upper() == "V"):
                try:
                    virtualizer = Virtualizer.create(
                        ipVirtualizer = ip,
                        portVirtualizer = port,
                        registerTime = datetime.now()
                    )
                    status = f"[DIRECTORY SERVICE]:\tVirtualizer {ip}:{port} foi cadastrado."
                except:
                    status = f"[DIRECTORY SERVICE]:\tVirtualizer {ip}:{port} já esta cadastrado."

            if(data[0].upper() == "G"):
                try:
                    virtualizer = Gateway.create(
                        ipGateway = ip,
                        portGateway = port,
                        registerTime = datetime.now()
                    )
                    status = f"[DIRECTORY SERVICE]:\tVirtualizer {ip}:{port} foi cadastrado."
                except:
                    status = f"[DIRECTORY SERVICE]:\tVirtualizer {ip}:{port} já esta cadastrado."
            socket.send_string(status)
        except:
            status ="[DIRECTORY SERVICE]:\t ERROR estrada não formatada corretamente"
            socket.send_string(status)
    

sendIP = threading.Thread(target = sendIp)
getIP = threading.Thread(target = getIp)
getIP.start()
sendIP.start()
