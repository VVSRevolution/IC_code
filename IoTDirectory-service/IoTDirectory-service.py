import peewee
import zmq
import socket
from datetime import datetime

PORT = "8080"
HOST = "127.0.0.1"

db = peewee.SqliteDatabase('IoTDirectory-service/database_ds.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Virtualizer(BaseModel):
    ipADDR = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())

class Gateway(BaseModel):
    ipADDR = peewee.TextField(default=None)
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
s = context.socket(zmq.PUB)    
p = "tcp://"+ HOST +":"+ PORT           # how and where to communicate
t=s.bind(p)                               # bind socket to the address
connectionTime = datetime.now()
print(t)
while True:
    s.send_string("[DirectoryService] " + "HI")
