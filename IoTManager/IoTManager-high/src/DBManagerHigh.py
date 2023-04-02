import peewee,socket,threading
from datetime import datetime

FORMAT = 'utf-8'

db = peewee.SqliteDatabase('IoTManager/IoTManager-high/Database_Manager-high.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class ManagerHighFather(BaseModel):
    ipManager = peewee.TextField(default=None)
    portManager = peewee.TextField(default=None)
    description = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())
    lastUpdateTime = peewee.DateTimeField(null=True)
    unregisterTime = peewee.DateTimeField(null=True)

class ManagerHighSons(BaseModel):
    ipManager = peewee.TextField(default=None)
    portManager = peewee.TextField(default=None)
    description = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())

try:
    db.create_tables([
        ManagerHighFather,
        ManagerHighSons    
    ])
    print("[DATABASE_MANAGER-HIGH]:\t[OK] Database")
except:
    print("[DATABASE_MANAGER-HIGH]:\t[ERRO] Database")

