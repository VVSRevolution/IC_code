from atexit import register
from ipaddress import ip_address
from time import time
import peewee
from datetime import datetime

db = peewee.SqliteDatabase('IoTDirectory-service/database_ds.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Sensor(BaseModel):
    uuid=peewee.TextField(primary_key=True)
    description = peewee.TextField(default=None)
    capabilities = peewee.TextField(default=None)

class Virtualizer(BaseModel):
    ipADDR = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())

class Gateway(BaseModel):
    ipADDR = peewee.TextField(default=None)
    sensor = peewee.ForeignKeyField(Sensor, backref='sensor')
    registerTime = peewee.DateTimeField(default=datetime.now())

try:
    db.create_tables([
        Virtualizer,
        Gateway,
        Sensor      
    ])
    print("[DATABASE]:\t[OK] ao criar tabela")
except:
    print("[DATABASE]:\t[ERRO] ao criar tabela")