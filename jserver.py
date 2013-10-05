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
        newSocket, address = self.accept( )
        clients[address] = newSocket
        print ("Connected from ", address)
        SecondaryServerSocket(newSocket)

class SecondaryServerSocket(asyncore.dispatcher_with_send):
    def handle_read(self):
        receivedData = self.recv(8192).strip().decode('utf-8')
        if receivedData:
            every = clients.values()
            for one in every:
                one.send(bytes(receivedData + '\n', 'UTF-8'))
        else: self.close( )
    def handle_close(self):
        one = self.getpeername( )
        print ("Disconnected from", one)
        del clients[one]

MainServerSocket(21567)
asyncore.loop( )
