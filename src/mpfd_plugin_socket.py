import threading
import socket
import json
import mpfd

class ClientSocketThread(threading.Thread):
    def __init__(self, clientSocket, address):
        super(ClientSocketThread, self).__init__()
        self.daemon=True
        self.clientSocket=clientSocket
        self.address=address
    
    def run(self):
        buf=""
        while True:
            receivedData=self.clientSocket.recv(4096)
            if len(receivedData)==0:
                print "Client thread exiting"
                break
            buf += receivedData
            #Process the received data
            if "\n" in buf:
                bufParts=buf.split("\n")
                buf=bufParts.pop()
                for line in bufParts:
                    response={'ok':False}
                    try:
                        content=json.loads(line)
                        if 'command' in content:
                            if content['command']=='list':
                                if 'dir' in content:
                                    listing=mpfd.listDir(content['dir'])
                                    response['listing']=listing
                                    response['ok']=True
                                else:
                                    response['error']="No dir parameter supplied"
                        self.clientSocket.send(json.dumps(response)+"\n")
                    except ValueError as ex:
                        print ex
                        self.clientSocket.send(json.dumps({'ok':False})+"\n")
                    
        
class ServerSocketThread(threading.Thread):
    def __init__(self,ip,port):
        super(ServerSocketThread, self).__init__()
        self.daemon=True
        self.serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((ip,port))
        self.serverSocket.listen(5)
        
    def run(self):
        while True:
            (clientSocket, address) = self.serverSocket.accept()
            ct=ClientSocketThread(clientSocket, address)
            ct.start()

class MPFDSocketPlugin:
    def __init__(self,addresses):
        self.socketThreads=[ServerSocketThread(x['ip'],x['port']) for x in addresses]
        
    def start(self):
        for t in self.socketThreads:
            t.start()
            
def createInstance(config):
    return MPFDSocketPlugin([{'ip': config[x], 'port': int(config["port"+x[2:]])} for x in config if x.startswith("ip")])            