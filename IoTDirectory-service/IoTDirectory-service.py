import peewee
import zmq
import socket
from datetime import datetime

PORT = "8080"
HOST = socket.gethostbyname(socket.gethostname())
HOST = "127.0.1.1"

FORMAT = 'utf-8'

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

context = zmq.Context()
socket = context.socket(zmq.REP)   
on = socket.bind("tcp://"+ HOST +":"+ PORT)
print(on)

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
    