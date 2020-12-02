# -*- coding: utf-8 -*-
import random
import math
import time
import KBEngine
import SCDefine
from KBEDebug import *
from interfaces.Combat import Combat
from interfaces.Spell import Spell
from interfaces.Motion import Motion
from interfaces.State import State
from interfaces.Flags import Flags
from interfaces.AI import AI
from interfaces.NPCObject import NPCObject

class Monster(KBEngine.Entity,
			NPCObject, 
			Flags,
			State,
			Motion, 
			Combat, 
			Spell, 
			AI):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		NPCObject.__init__(self)
		Flags.__init__(self) 
		State.__init__(self) 
		Motion.__init__(self) 
		Combat.__init__(self) 
		Spell.__init__(self) 
		AI.__init__(self) 
		
		# The layer where the entity is located, you can set up multiple different navmesh layers to find the way, here 20002001 is the flying dragon in the warring-demo，
		# Level 0 is the ground, level 1 is the wayfinding layer ignoring the building
		if self.modelID == 20002001:
			self.layer = 1 
			
		DEBUG_MSG("%s::__init__: self.layer = %i" % (self.getScriptName(), self.layer))

	def initEntity(self):
		"""
		virtual method.
		"""
		pass

	def checkInTerritory(self):
		"""
		virtual method.
		Check if you are in movable territory
		"""
		return AI.checkInTerritory(self)

	def isMonster(self):
		"""
		virtual method.
		"""
		return True
		
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		NPCObject.onTimer(self, tid, userArg)
		Spell.onTimer(self, tid, userArg)
		AI.onTimer(self, tid, userArg)
		
	def onWitnessed(self, isWitnessed):
		"""
		KBEngine method.
		Whether this entity is observed by a player, this interface is mainly provided to the server to do some performance optimization work,
		Under normal circumstances, some entities are not observed by any client, they do not need to do any work, use this interface
		You can activate or stop any behavior of this entity at the appropriate time.
		@param isWitnessed	: When false, the entity is separated from any observer
		"""
		AI.onWitnessed(self, isWitnessed)
		
	def onForbidChanged_(self, forbid, isInc):
		"""
		virtual method.
		Entity prohibited conditions change
		@param isInc		:	Is it increased
		"""
		State.onForbidChanged_(self, forbid, isInc)
		AI.onForbidChanged_(self, forbid, isInc)
		
	def onStateChanged_(self, oldstate, newstate):
		"""
		virtual method.
		entity state changed
		"""
		State.onStateChanged_(self, oldstate, newstate)
		AI.onStateChanged_(self, oldstate, newstate)
		NPCObject.onStateChanged_(self, oldstate, newstate)
		
	def onSubStateChanged_(self, oldSubState, newSubState):
		"""
		virtual method.
		Substate changed
		"""
		State.onSubStateChanged_(self, oldSubState, newSubState)
		AI.onSubStateChanged_(self, oldSubState, newSubState)

	def onFlagsChanged_(self, flags, isInc):
		"""
		virtual method.
		"""
		Flags.onFlagsChanged_(self, flags, isInc)
		AI.onFlagsChanged_(self, flags, isInc)

	def onEnterTrap(self, entity, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		Engine callback into trap trigger
		"""
		AI.onEnterTrap(self, entity, range_xz, range_y, controllerID, userarg)

	def onLeaveTrap(self, entity, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		Triggered by engine callback leaving trap
		"""
		AI.onLeaveTrap(self, entity, range_xz, range_y, controllerID, userarg)

	def onAddEnemy(self, entityID):
		"""
		virtual method.
		Enemies enter the list
		"""
		AI.onAddEnemy(self, entityID)
		Combat.onAddEnemy(self, entityID)

	def onRemoveEnemy(self, entityID):
		"""
		virtual method.
		Delete enemy
		"""
		AI.onRemoveEnemy(self, entityID)
		Combat.onRemoveEnemy(self, entityID)

	def onEnemyEmpty(self):
		"""
		virtual method.
		Enemy list is empty
		"""
		AI.onEnemyEmpty(self)
		Combat.onEnemyEmpty(self)

	def onDestroy(self):
		"""
		entity destruction
		"""
		NPCObject.onDestroy(self)
		Combat.onDestroy(self)

