import zmq

FORMAT = 'utf-8'
PORT = "8080"
HOST = "127.0.1.1"
EXIT = "exit"

#DShost = input("[APP]:\tEnter directory service host: ")
#DSport = input("[APP]:\tEnter directory service port: ")    


context = zmq.Context()
socket = context.socket(zmq.REQ)
print("tcp://"+ DShost +":"+ DSport)
socket.connect("tcp://"+ HOST +":"+ PORT)
for request in range(10):
    print("Sending request %s …" % request)

    socket.send(b"Hello")

    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))

    

