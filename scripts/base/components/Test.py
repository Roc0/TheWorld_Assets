# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class Test(KBEngine.EntityComponent):
	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		print("+++++++++++++++++++++++name=%s, bb=%i" % (self.name, self.bb))

		if hasattr(self.owner, "cellData"):
			print("+++++++++++++++++++++++cellData=%s" % self.owner.cellData[self.name])

	def onAttached(self, owner):
		"""
		"""
		INFO_MSG("Test::onAttached(): owner=%i" % (owner.id))
		
	def onDetached(self, owner):
		"""
		"""
		INFO_MSG("Test::onDetached(): owner=%i" % (owner.id))

	def say(self, iii):
		print("+++++++++++++++++++++++say", iii)
		if self.owner.cell is not None:
			self.cell.hello(33321)

	def onClientEnabled(self):
		"""
		KBEngine method.
		The entity is officially activated and ready for use. At this time, the entity has established the corresponding entity of the client, and you can create it here.
		cell part.
		"""
		INFO_MSG("Test[%i]::onClientEnabled:entities enable." % (self.ownerID))
		self.tid = self.addTimer(10, 0, 123)

	def onClientDeath(self):
		"""
		KBEngine method.
		The client's corresponding entity has been destroyed
		"""
		DEBUG_MSG("Test[%i].onClientDeath:" % self.ownerID)

		if self.tid > 0:
			self.delTimer(self.tid)

	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.name, self.ownerID, tid, userArg))

		if self.tid == tid:
			self.tid = 0