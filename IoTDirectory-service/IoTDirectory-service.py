
import peewee 
from datetime import datetime

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