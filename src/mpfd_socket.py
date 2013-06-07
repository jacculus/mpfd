import threading

class ClientSocketThread(threading.Thread):
	def __init__(self, clientSocket, address):
		self.clientSocket=clientSocket
		self.address=address
	
	def run(self):
		pass
		
class ServerSocketThread(threading.Thread):
	def __init__(self):
		self.serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.bind((socket.gethostname(),9850))
		self.serverSocket.listen(5)
		
	def run(self):
		while True:
			(clientSocket, address) = self.serverSocket.accept()
			 ct=ClientSocketThread(clientSocket, address)
			 ct.start()
			 