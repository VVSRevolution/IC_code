import zmq

FORMAT = 'utf-8'
PORT = 8080
HOST = "127.0.1.1"


#DShost = input("[APP]:\tEnter directory service host: ")
#DSport = input("[APP]:\tEnter directory service port: ")

def getIp():
    context = zmq.Context()
    p = "tcp://"+ HOST +":"+ str(PORT+1)
    print(p)
    s = context.socket(zmq.SUB)
    s.connect(p)
    s.setsockopt_string(zmq.SUBSCRIBE, "virtualizer ")
    entrada = s.recv().decode(FORMAT).split(" ")
    entrada = entrada[1]
    entrada = entrada.splitlines()

    for i in range(len(entrada)):
        print(f"Opção[{i}]:\thttps://{entrada[i]}")


def sendData():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    print("tcp://"+ DShost +":"+ DSport)
    socket.connect("tcp://"+ HOST +":"+ PORT)
    for request in range(10):
        print("Sending request %s …" % request)

        socket.send(b"Hello")

        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))

    

