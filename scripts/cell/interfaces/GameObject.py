# -*- coding: utf-8 -*-
import KBEngine
import d_spaces
import SCDefine
import GlobalDefine
from KBEDebug import * 

import d_entities
import d_avatar_inittab

class GameObject:
	"""
	Basic interface class of server game object
	"""
	def __init__(self):
		pass

	def initEntity(self):
		"""
		virtual method.
		"""
		pass
	
	def isPlayer(self):
		"""
		virtual method.
		"""
		return False

	def isNPC(self):
		"""
		virtual method.
		"""
		return False
		
	def isMonster(self):
		"""
		virtual method.
		"""
		return False
	
	def getDatas(self):
		if self.isPlayer():
			return d_avatar_inittab.datas[self.uid]
		
		return d_entities.datas[self.uid]
		
	def getScriptName(self):
		return self.__class__.__name__
		
	def getCurrSpaceBase(self):
		"""
		Get the entity baseEntityCall of the current space
		"""
		return KBEngine.globalData["space_%i" % self.spaceID]

	def getCurrSpace(self):
		"""
		Get the entity of the current space
		"""
		spaceBase = self.getCurrSpaceBase()
		return KBEngine.entities.get(spaceBase.id, None)
		
	def getSpaces(self):
		"""
		Get Scene Manager
		"""
		return KBEngine.globalData["Spaces"]
	
	def startDestroyTimer(self):
		"""
		virtual method.
		
		Start destroying entitytimer
		"""
		if self.isState(GlobalDefine.ENTITY_STATE_DEAD):
			self.addTimer(5, 0, SCDefine.TIMER_TYPE_DESTROY)
			DEBUG_MSG("%s::startDestroyTimer: %i running." % (self.getScriptName(), self.id))
	
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
			self.onDestroyEntityTimer()
			
	def onStateChanged_(self, oldstate, newstate):
		"""
		virtual method.
		entity state changed
		"""
		self.startDestroyTimer()
			
	def onWitnessed(self, isWitnessed):
		"""
		KBEngine method.
		Whether this entity is observed by a player, this interface is mainly provided to the server to do some performance optimization work,
		Under normal circumstances, some entities are not observed by any client, they do not need to do any work, use this interface
		You can activate or stop any behavior of this entity at the appropriate time.
		@param isWitnessed	: When false, the entity is separated from any observer
		"""
		DEBUG_MSG("%s::onWitnessed: %i isWitnessed=%i." % (self.getScriptName(), self.id, isWitnessed))
		
	def onEnterTrap(self, entityEntering, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		Engine callback into trap trigger
		"""
		if entityEntering.getScriptName() == "Avatar":
			DEBUG_MSG("%s::onEnterTrap: %i entityEntering=%i, range_xz=%s, range_y=%s, controllerID=%i, userarg=%i" % \
							(self.getScriptName(), self.id, entityEntering.id, range_xz, range_y, controllerID, userarg))

	def onLeaveTrap(self, entityLeaving, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		Triggered by engine callback leaving trap
		"""
		if entityLeaving.getScriptName() == "Avatar":
			DEBUG_MSG("%s::onLeaveTrap: %i entityLeaving=%i, range_xz=%s, range_y=%s, controllerID=%i, userarg=%i" % \
							(self.getScriptName(), self.id, entityLeaving.id, range_xz, range_y, controllerID, userarg))

	def onRestore(self):
		"""
		KBEngine method.
		Part of the entity's cell was successfully restored
		"""
		DEBUG_MSG("%s::onRestore: %s" % (self.getScriptName(), self.base))

	def onDestroyEntityTimer(self):
		"""
		entity's delayed destruction timer
		"""
		self.destroy()
