import zmq

FORMAT = 'utf-8'
PORT = "8080"
HOST = "192.168.0.179"
EXIT = "exit"

context = zmq.Context()
s = context.socket(zmq.SUB)   
p = "tcp://"+ HOST +":"+ PORT 
print(p)
s.connect(p) 
s.setsockopt_string(zmq.SUBSCRIBE, "[DirectoryService] ")
print(s.recv())
