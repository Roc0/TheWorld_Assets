# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class GameObject:
	"""
	Basic interface class of server game object
	"""
	def __init__(self):
		pass

	def getScriptName(self):
		return self.__class__.__name__

	def destroySelf(self):
		"""
		virtual method
		"""
		if self.cell is not None:
			# Destroy the cell entity
			self.destroyCellEntity()
			return
			
		# Destroy base
		self.destroy()
		
	def getSpaces(self):
		"""
		Get Scene Manager
		"""
		return KBEngine.globalData["Spaces"]

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if self.isDestroyed:
			self.delTimer(tid)
			return
			
	def onGetCell(self):
		"""
		KBEngine method.
		Part of the entity's cell was successfully created
		"""
		#DEBUG_MSG("%s::onGetCell: %i" % (self.getScriptName(), self.id))
		pass
		
	def onLoseCell(self):
		"""
		KBEngine method.
		Part of the entity's cell is missing
		"""
		DEBUG_MSG("%s::onLoseCell: %i" % (self.getScriptName(), self.id))
		self.destroySelf()

	def onRestore(self):
		"""
		KBEngine method.
		Part of the entity's cell was successfully restored
		"""
		DEBUG_MSG("%s::onRestore: %s" % (self.getScriptName(), self.cell))
		

