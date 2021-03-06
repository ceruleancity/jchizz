import asyncore
import socket

clients = {}

class MainServerSocket(asyncore.dispatcher):
	def __init__(self, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(('',port))
		self.listen(5)
	def handle_accept(self):
		try:
			newSocket, address = self.accept()
			clients[address] = newSocket
			print ("Connected from ", address)
			clients_list = clients.values()
			for i in clients_list:
				i.send(bytes('Connected from ' + str(address) + '\n', 'UTF-8'))
			SecondaryServerSocket(newSocket)
		except socket.error:
			print("Socket error connecting client")
		except Exception:
			print("Unknown error connecting client")

class SecondaryServerSocket(asyncore.dispatcher_with_send):
	def handle_read(self):
		receivedData = self.recv(8192).strip().decode('utf-8')
		if receivedData:
			clients_list = clients.values()
			for i in clients_list:
				i.send(bytes(receivedData + '\n', 'UTF-8'))
		else: self.close()
	def handle_close(self):
		try:
			peername = self.getpeername()
			print ("Disconnected from ", peername)
			clients_list = clients.values()
			for i in clients_list:
				i.send(bytes('Disconnected from ' + str(peername) + '\n', 'UTF-8'))
			del clients[peername]
		except socket.error:
			print("Socket error disconnecting client...")
		except Exception:
			print("Unknown error disconnecting client")

MainServerSocket(21567)
asyncore.loop( )
