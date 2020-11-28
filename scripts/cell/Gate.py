# -*- coding: utf-8 -*-
import random
import math
import time
import SCDefine
import d_spaces
import KBEngine
from KBEDebug import *
from interfaces.GameObject import GameObject

class Gate(KBEngine.Entity, GameObject):
	"""
	This is a portal entity. When the player enters the portal "self.addProximity(5.0, 0, 0)" area,
	Portals will teleport players to designated locations
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self) 
		
		self.addTimer(1, 0, SCDefine.TIMER_TYPE_HEARDBEAT)				# Heartbeat timer, every 1 second

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_HEARDBEAT == userArg:
			self.onHeardTimer()
		
		GameObject.onTimer(self, tid, userArg)
		
	def onHeardTimer(self):
		"""
		entity heartbeat
		"""
		self.addProximity(5.0, 0, 0)
		
	def onEnterTrap(self, entityEntering, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		There are entities into the trap
		"""
		if entityEntering.isDestroyed or entityEntering.getScriptName() != "Avatar":
			return
			
		DEBUG_MSG("%s::onEnterTrap: %i entityEntering=(%s)%i, range_xz=%s, range_y=%s, controllerID=%i, userarg=%i" % \
						(self.getScriptName(), self.id, entityEntering.getScriptName(), entityEntering.id, \
						range_xz, range_y, controllerID, userarg))
		
		if self.uid == 40001003: # currspace - teleport
			spaceData = d_spaces.datas.get(entityEntering.spaceUType)
			entityEntering.teleport(None, spaceData["spawnPos"], tuple(self.direction))		
		else:					 # teleport to xxspace
			if entityEntering.spaceUType == 3:
				gotoSpaceUType = 4
			else:
				gotoSpaceUType = 3
			
			spaceData = d_spaces.datas.get(gotoSpaceUType)
			entityEntering.teleportSpace(gotoSpaceUType, spaceData["spawnPos"], tuple(self.direction), {})

	def onLeaveTrap(self, entityLeaving, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		There are entities leaving the trap
		"""
		if entityLeaving.isDestroyed or entityLeaving.getScriptName() != "Avatar":
			return
			
		INFO_MSG("%s::onLeaveTrap: %i entityLeaving=(%s)%i." % (self.getScriptName(), self.id, \
				entityLeaving.getScriptName(), entityLeaving.id))
				
