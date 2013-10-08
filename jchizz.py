try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import _thread
import sys

from socket import *

HOST = '192.168.1.34'
PORT = 21567
BUFSIZE = 1024
tcpCliSock = socket(AF_INET, SOCK_STREAM)

class Application(Frame):
	def __init__(self, master, argv):
		Frame.__init__(self, master)

		# Setup handle
		self.name = ""
		if len(argv) > 1:
			# First param is username
			self.name = argv[1]
		else:
			self.name = "Anonymous"
		print("name is ", self.name)

		ADDR = (HOST, PORT)
		if len(argv) > 2:
			# Second param is hostname
			print("Received hostname ", argv[2])
			ADDR = (argv[2], PORT)

		# Connect to the server
		tcpCliSock.connect(ADDR)
		print("connected to ", ADDR )

		self.grid()
		self.create_widgets()
		self.socket()

	def callback(self, event):
		message = self.entry_field.get()
		name = self.name
		message = name + ": " + message
		tcpCliSock.send(bytes(message, 'UTF-8'))

		# Clear the entry field
		self.entry_field.delete(0,END)

	def create_widgets(self):
		self.messaging_field = Text(self, width = 110, height = 20, wrap = WORD)
		self.messaging_field.grid(row = 0, column = 0, columnspan = 2, sticky = W)
		self.messaging_field.config(state=DISABLED)

		self.entry_field = Entry(self, width = 92)
		self.entry_field.grid(row = 1, column = 0, sticky = W)
		self.entry_field.bind('<Return>', self.callback)

		self.label = Label(self, text='Hit Enter Key to Send a Message')
		self.label.grid(row = 2, column = 0, sticky = W)

	def add(self, data):
		self.messaging_field.config(state=NORMAL)
		self.messaging_field.insert(END, data )

		# Scroll to the end of the messaging field
		self.messaging_field.yview(END)
		self.messaging_field.config(state=DISABLED)

	def socket(self):
		def loop0():
			while 1:
				data = tcpCliSock.recv(BUFSIZE)
				if data: self.add( data )

		_thread.start_new_thread(loop0, ())

root = Tk()
root.title("jchizz chat client")
root.geometry("750x360")

app = Application(root,sys.argv)

root.mainloop()