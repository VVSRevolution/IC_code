import peewee,zmq,socket,threading,time,psutil,sys
from datetime import datetime
from playhouse.shortcuts import model_to_dict, dict_to_model

ErroDS = False
FORMAT = 'utf-8'
PORT = 8080


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
my_eip = s.getsockname()[0]
nics = psutil.net_if_addrs()
my_enic = [i for i in nics for j in nics[i]
           if j.address == my_eip and j.family == socket.AF_INET][0]
print('\033[1m[DIRECTORY SERVICE]:\033[0m\tEthernet NIC name is {0}\n\t\t\tIPv4 address is {1}.\n'.format(
    my_enic, my_eip))
HOST = format(my_eip)
db = peewee.SqliteDatabase('IoTManager/IoTManager-low/database_ds.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Manager(BaseModel):
    ipManager = peewee.TextField(default=None)
    portManager = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())

class Virtualizer(BaseModel):
    ipVirtualizer = peewee.TextField(default=None)
    portVirtualizer = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())

class Gateway(BaseModel):
    ipGateway = peewee.TextField(default=None)
    portGateway = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())

class ManagerFather(BaseModel):
    ipManager = peewee.TextField(default=None)
    portManager = peewee.TextField(default=None)
    description = peewee.TextField(default=None)
    registerTime = peewee.DateTimeField(default=datetime.now())
    lastUpdateTime = peewee.DateTimeField(null=True)
    unregisterTime = peewee.DateTimeField(null=True)
class treeAddress(BaseModel):
    name = peewee.TextField(default=None)
    parent = peewee.TextField(default="")
    registerTime = peewee.DateTimeField(default=datetime.now())
    unregisterTime = peewee.DateTimeField(null=True)


try:
    db.create_tables([
        Virtualizer,
        Gateway,
        Manager,
        ManagerFather,
        treeAddress  
    ])
    print("\033[1m[DATABASE]:\t\t[OK]\033[0m ao criar tabela\n")
except:
    print("\033[1m[DATABASE]:\t[ERRO]\033[0m ao criar tabela\n")

def sendIpToDs(portUsed):
    global ipDS
    if(ErroDS):
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            conc = f"tcp://{ipDS}:{PORT}"
            socket.setsockopt(zmq.RCVTIMEO, 1000)
            print(f"\033[1m[DIRECTORY SERVICE]:\033[0m\tMandando para \033[3mDIRECTORY SERVICE\033[0m: {conc}\n\t\t\t . . .")
            socket.connect(conc)
            socket.send_string(f"M${HOST}${portUsed}")
            msg = socket.recv().decode(FORMAT)
            return
        except:
            print(f"\033[1m[DIRECTORY SERVICE]:\033[0m\tERROR ao mandar ADDR ao \033[3mDIRECTORY SERVICE\033[0m\n\t\t\tNão foi possivel conectar ao {conc}")
            socket.close()
            return

        return

def sendIp(): # um pub/sub que envia os ADDR dos virtualizers, geteways e managers
    context = zmq.Context()
    s = context.socket(zmq.PUB)
    PortSend = str(PORT + 1)
    p = f"tcp://{(HOST)}:{PortSend}"

    try:
        s.bind(p)
    except Exception as error:
        global ErroDS
        ErroDS = True
        saida = f"\n\33[1m[DIRECTORY SERVICE]:\033[0m \tNa função \033[3msendIP\033[0m:\n\t\t\tOcorreu erro ao tentar fazer um bind \033[3mem {p}\033[0m:"
        print(saida,error)
        return

    print(f"\033[1m[DIRECTORY SERVICE]:\033[0m\tMandando dados \033[3mem {p}\033[0m")
    while(True):
        manager = []
        query = Manager.select().paginate(1, Manager.select().count())
        for i in query:
            manager.append(model_to_dict(i))

        query = Virtualizer.select(Virtualizer.ipVirtualizer, Virtualizer.portVirtualizer)
        virtualizerData = ""
        for virtualizer in query:
            virtualizerData += f"{virtualizer.ipVirtualizer}:{virtualizer.portVirtualizer}\n"

        query = Gateway.select(Gateway.ipGateway, Gateway.portGateway)
        gatewayData = ""
        for gateway in query:
            gatewayData += f"{gateway.ipGateway}:{gateway.portGateway}\n"

        s.send_string("virtualizer " + virtualizerData)
        s.send_string("gateway " + gatewayData)


def getIp(): # recebe os ADDR dos virtualizers e geteways
    context = zmq.Context()
    socket = context.socket(zmq.REP)   
    p = "tcp://"+ HOST +":"+ str(PORT)
    
    try:    
        socket.bind(p)
    except Exception as error:
        global ErroDS
        ErroDS = True
        saida = f"\033[1m[DIRECTORY SERVICE]:\033[0m \tNa função \033[3mgetIP\033[0m:\n\t\t\tOcorreu erro ao tentar fazer um bind \033[3mem {p}\033[0m:"
        print(saida,error)
        return
    print(f"\033[1m[DIRECTORY SERVICE]:\033[0m\tRecebendo dados \033[3mem {p}\033[0m")
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
                    status = f"\033[1m[DIRECTORY SERVICE]:\033[0m\tVirtualizer {ip}:{port} foi cadastrado."
                except:
                    status = f"\033[1m[DIRECTORY SERVICE]:\033[0m\tVirtualizer {ip}:{port} já esta cadastrado."

            if(data[0].upper() == "G"):
                try:
                    gateway = Gateway.create(
                        ipGateway = ip,
                        portGateway = port,
                        registerTime = datetime.now()
                    )
                    status = f"\033[1m[DIRECTORY SERVICE]:\033[0m\tGateway {ip}:{port} foi cadastrado."
                except:
                    status = f"\033[1m[DIRECTORY SERVICE]:\033[0m\tGateway {ip}:{port} já esta cadastrado."

            if(data[0].upper() == "M"):
                try:
                    query = Manager.get(
                                Manager.ipManager == ip and
                                Manager.portManager == port
                            )
                except ManagerFather.DoesNotExist:
                    query = Manager.create(
                        ipManager = ip,
                        portManager = port,
                        registerTime = datetime.now()

                    )
            socket.send_string(status)
        except:
            status ="\033[1m[DIRECTORY SERVICE]:\033[0m\t ERROR estrada não formatada corretamente"
            socket.send_string(status)


iniciarDS = input(f"\033[1m[DIRECTORY SERVICE]:\t\033[0mGostaria de iniciar o \033[3mDIRECTORY SERVICE\033[0m? \033[3mYES\033[0m ou \033[3mNO\033[0m:\n\t\t\t\033[3mRecomenda-se apenas um DIRECTORY SERVICE por rede local.\n\t\t\t\033[0m" )
while (iniciarDS.upper() != "NO" and iniciarDS.upper() != "YES"):
    iniciarDS = input(f"\033[1m[DIRECTORY SERVICE]:\033[0m\t\033[3mYES\033[0m ou \033[3mNO\033[0m?" )
if iniciarDS.upper() == "NO":
    ErroDS = True


sendIP = threading.Thread(target = sendIp)
getIP = threading.Thread(target = getIp)
if(not ErroDS):
    getIP.start()
    time.sleep(0.1)
    sendIP.start()

if(ErroDS):

    time.sleep(1)
    print("\n\033[1m[DIRECTORY SERVICE]:\033[0m \tO \033[3mDIRECTORY SERVICE\033[0m já esta rodando em outro local na rede ou outro serviço esta impedindo sua inicialização!\n")
    ipDS = input("\033[1m[DIRECTORY SERVICE]:\033[0m\tSe o \033[3mDIRECTORY SERVICE\033[0m já estiver rodando na rede entre com o IP:")
    while(ipDS == ""):
        ipDS = input("\033[1m[DIRECTORY SERVICE]:\033[0m\t ERRO IP não valido, entre com IP valido: ")
    

else:
    print("\n\033[1m[DIRECTORY SERVICE]:\033[0m\tINICIADO")            
