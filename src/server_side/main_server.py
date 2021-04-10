import socket
from threading import Thread



class Server:
	"""
	With socket library make a server to users can interact with 
	each other.
	"""
	def __init__(self, is_server:bool):

		self.is_server = is_server
		self.server = socket.socket()

		if is_server:
			self.server.bind(("localhost", 1372))
			self.server.listen(2)
			self.connection , self.address = self.server.accept()
		else:
			self.server.connect(("localhost", 1372))

	def server_send_message(self, message:str=None) -> None:
		"""
		Get message from ui and send it.
		"""
		if self.is_server:
			self.connection.send(bytes(message, encoding="utf-8"))
		else:
			self.server.send(bytes(message, encoding="utf-8"))

	def server_receive_message(self) -> str:
		"""
		Get message from server and return it.
		"""
		if self.is_server:
			while True:
				message = self.connection.recv(1024).decode("utf-8")
				yield message
		else:
			while True:
				message = self.server.recv(1024).decode("utf-8")
				yield message