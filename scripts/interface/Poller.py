# -*- coding: utf-8 -*-
import KBEngine
import Functor
import socket
from KBEDebug import *

class Poller:
	"""
	Demo:
	You can register a socket with kbengine, and the network module of the engine layer handles asynchronous notification sending and receiving.
	usage:
	from Poller import Poller
	poller = Poller()
	
	Open (can be executed in onBaseappReady)
	poller.start("localhost", 12345)
	
	stop
	poller.stop()
	"""
	def __init__(self):
		self._socket = None
		self._clients = {}
		
	def start(self, addr, port):
		"""
		virtual method.
		"""
		self._socket = socket.socket()
		self._socket.bind((addr, port))
		self._socket.listen(10)
		
		KBEngine.registerReadFileDescriptor(self._socket.fileno(), self.onRecv)
		# KBEngine.registerWriteFileDescriptor(self._socket.fileno(), self.onWrite)

	def stop(self):
		if self._socket:
			KBEngine.deregisterReadFileDescriptor(self._socket.fileno())
			self._socket.close()
			self._socket = None
		
	def onWrite(self, fileno):
		pass
		
	def onRecv(self, fileno):
		if self._socket.fileno() == fileno:
			sock, addr = self._socket.accept()
			self._clients[sock.fileno()] = (sock, addr)
			KBEngine.registerReadFileDescriptor(sock.fileno(), self.onRecv)
			DEBUG_MSG("Poller::onRecv: new channel[%s/%i]" % (addr, sock.fileno()))
		else:
			sock, addr = self._clients.get(fileno, None)
			if sock is None:
				return
			
			data = sock.recv(2048)

			if len(data) == 0:
				DEBUG_MSG("Poller::onRecv: %s/%i disconnect!" % (addr, sock.fileno()))
				KBEngine.deregisterReadFileDescriptor(sock.fileno())
				sock.close()
				del self._clients[fileno]
				return

			DEBUG_MSG("Poller::onRecv: %s/%i get data, size=%i" % (addr, sock.fileno(), len(data)))
			self.processData(sock, data)
			
	def processData(self, sock, datas):
		"""
		Processing received data
		"""
		pass