# -*- coding: utf-8 -*-
import KBEngine
import random
import SCDefine
import time
import GlobalConst
import d_spaces
import d_avatar_inittab
from KBEDebug import *
from interfaces.GameObject import GameObject
from interfaces.Teleport import Teleport

class Avatar(KBEngine.Proxy,
			GameObject,
			Teleport):
	"""
	Role entity
	"""
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		GameObject.__init__(self)
		Teleport.__init__(self)
		
		self.accountEntity = None
		self.cellData["dbid"] = self.databaseID
		self.nameB = self.cellData["name"]
		self.spaceUTypeB = self.cellData["spaceUType"]
		
		self._destroyTimer = 0

	def onClientEnabled(self):
		"""
		KBEngine method.
		The entity is officially activated and ready for use. At this time, the entity has established the corresponding entity of the client, and you can create it here.
		cell part.
		"""
		INFO_MSG("Avatar[%i-%s] entities enable. spaceUTypeB=%s, entityCall:%s" % (self.id, self.nameB, self.spaceUTypeB, self.client))
		Teleport.onClientEnabled(self)
		
		if self._destroyTimer > 0:
			self.delTimer(self._destroyTimer)
			self._destroyTimer = 0

	def onGetCell(self):
		"""
		KBEngine method.
		Part of the entity's cell was successfully created
		"""
		DEBUG_MSG('Avatar::onGetCell: %s' % self.cell)
		
	def createCell(self, space):
		"""
		defined method.
		Create cell entity
		"""
		self.createCellEntity(space)
	
	def destroySelf(self):
		"""
		"""
		if self.client is not None:
			return
			
		if self.cell is not None:
			# Destroy the cell entity
			self.destroyCellEntity()
			return
			
		# If the account ENTITY exists, it will be notified to destroy it
		if self.accountEntity != None:
			if time.time() - self.accountEntity.relogin > 1:
				self.accountEntity.destroy()
			else:
				DEBUG_MSG("Avatar[%i].destroySelf: relogin =%i" % (self.id, time.time() - self.accountEntity.relogin))
				
		# Destroy base
		if not self.isDestroyed:
			self.destroy()

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_DESTROY == userArg:
			self.onDestroyTimer()
		
		GameObject.onTimer(self, tid, userArg)
		
	def onClientDeath(self):
		"""
		KBEngine method.
		entity lost client entity
		"""
		DEBUG_MSG("Avatar[%i].onClientDeath:" % self.id)
		# To prevent the client from disconnecting while requesting to create a cell, we delay the execution of the cell destruction until the base is destroyed
		# During this time, the client's short connection login will activate the entity
		self._destroyTimer = self.addTimer(10, 0, SCDefine.TIMER_TYPE_DESTROY)
			
	def onClientGetCell(self):
		"""
		KBEngine method.
		The client has obtained relevant data of some cell entities
		"""
		INFO_MSG("Avatar[%i].onClientGetCell:%s" % (self.id, self.client))
		self.client.component3.helloCB(777)

	def onDestroyTimer(self):
		DEBUG_MSG("Avatar::onDestroyTimer: %i" % (self.id))
		self.destroySelf()
		
	def onDestroy(self):
		"""
		KBEngine method.
		entity destruction
		"""
		DEBUG_MSG("Avatar::onDestroy: %i." % self.id)
		
		if self.accountEntity != None:
			self.accountEntity.activeAvatar = None
			self.accountEntity = None



