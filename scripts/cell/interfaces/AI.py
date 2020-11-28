# -*- coding: utf-8 -*-
import KBEngine
import SCDefine
import time
import random
import GlobalDefine
from KBEDebug import * 
from skillbases.SCObject import SCObject

import d_entities

__TERRITORY_AREA__ = 30.0

class AI:
	def __init__(self):
		self.enable()
	
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
		ret = self.position.distTo(self.spawnPos) <= __TERRITORY_AREA__
		if not ret:
			INFO_MSG("%s::checkInTerritory: %i is False." % (self.getScriptName(), self.id))
			
		return ret

	def addTerritory(self):
		"""
		Add territory
		Some entities entering the territory will be considered as enemies
		"""
		assert self.territoryControllerID == 0 and "territoryControllerID != 0"
		trange = __TERRITORY_AREA__ / 2.0
		self.territoryControllerID = self.addProximity(trange, 0, 0)
		
		if self.territoryControllerID <= 0:
			ERROR_MSG("%s::addTerritory: %i, range=%i, is error!" % (self.getScriptName(), self.id, trange))
		else:
			INFO_MSG("%s::addTerritory: %i range=%i, id=%i." % (self.getScriptName(), self.id, trange, self.territoryControllerID))
			
	def delTerritory(self):
		"""
		Remove territory
		"""
		if self.territoryControllerID > 0:
			self.cancelController(self.territoryControllerID)
			self.territoryControllerID = 0
			INFO_MSG("%s::delTerritory: %i" % (self.getScriptName(), self.id))
			
	def enable(self):
		"""
		Activate entity
		"""
		self.heartBeatTimerID = \
		self.addTimer(random.randint(0, 1), 1, SCDefine.TIMER_TYPE_HEARDBEAT)				# 心跳timer, 每1秒一次
		
	def disable(self):
		"""
		Prohibit this entity from doing anything
		"""
		self.delTimer(self.heartBeatTimerID)
		self.heartBeatTimerID = 0
	
	def think(self):
		"""
		virtual method.
		"""
		if self.isState(GlobalDefine.ENTITY_STATE_FREE):
			self.onThinkFree()
		elif self.isState(GlobalDefine.ENTITY_STATE_FIGHT):
			self.onThinkFight()
		else:
			self.onThinkOther()
		
		if not self.isWitnessed:
			self.disable()
		
	def choiceTarget(self):
		"""
		Choose an enemy from the hate table
		"""
		if len(self.enemyLog) > 0:
			self.targetID = self.enemyLog[0]
		else:
			self.targetID = 0
	
	def setTarget(self, entityID):
		"""
		Set goals
		"""
		self.targetID = entityID
		self.onTargetChanged()
	
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onHeardTimer(self):
		"""
		entity heartbeat
		"""
		self.think()
		
	def onTargetChanged(self):
		"""
		virtual method.
		Goal change
		"""
		pass
		
	def onWitnessed(self, isWitnessed):
		"""
		KBEngine method.
		Whether this entity is observed by a player, this interface is mainly provided to the server to do some performance optimization work,
		Under normal circumstances, some entities are not observed by any client, they do not need to do any work, use this interface
		You can activate or stop any behavior of this entity at the appropriate time.
		@param isWitnessed	: When false, the entity is separated from any observer
		"""
		INFO_MSG("%s::onWitnessed: %i isWitnessed=%i." % (self.getScriptName(), self.id, isWitnessed))
		
		if isWitnessed:
			self.enable()
			
	def onThinkFree(self):
		"""
		virtual method.
		Think when idle
		"""
		if self.territoryControllerID <= 0:
			self.addTerritory()
		
		self.randomWalk(self.spawnPos)

	def onThinkFight(self):
		"""
		virtual method.
		Think while fighting
		"""
		if self.territoryControllerID > 0:
			self.delTerritory()
		
		self.checkEnemys()
		
		if self.targetID <= 0:
			return
		
		dragon = (self.modelID == 20002001)

		# The demo is simple to implement. If it is a dragon, the attack distance is relatively long. Different skills should be used to determine the attack distance.
		attackMaxDist = 2.0
		if dragon:
			attackMaxDist = 20.0
			
		entity = KBEngine.entities.get(self.targetID)

		if entity.position.distTo(self.position) > attackMaxDist:
			runSpeed = self.getDatas()["runSpeed"]
			if runSpeed != self.moveSpeed:
				self.moveSpeed = runSpeed
			self.gotoPosition(entity.position, attackMaxDist - 0.2)
			return
		else:
			self.resetSpeed()
			
			skillID = 1
			if dragon:
				skillID = 7000101

			self.spellTarget(skillID, entity.id)
			
	def onThinkOther(self):
		"""
		virtual method.
		Think at other times
		"""
		pass
		
	def onForbidChanged_(self, forbid, isInc):
		"""
		virtual method.
		Entity prohibited conditions change
		@param isInc		:	Is it increased
		"""
		pass

	def onStateChanged_(self, oldstate, newstate):
		"""
		virtual method.
		entity state changed
		"""
		if self.isState(GlobalDefine.ENTITY_STATE_DEAD):
			if self.isMoving:
				self.stopMotion()
				
	def onSubStateChanged_(self, oldSubState, newSubState):
		"""
		virtual method.
		Substate changed
		"""
		#INFO_MSG("%i oldSubstate=%i to newSubstate=%i" % (self.id, oldSubState, newSubState))
		pass

	def onFlagsChanged_(self, flags, isInc):
		"""
		virtual method.
		"""
		pass
	
	def onEnterTrap(self, entityEntering, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		There are entities into the trap
		"""
		if controllerID != self.territoryControllerID:
			return
		
		if entityEntering.isDestroyed or entityEntering.getScriptName() != "Avatar" or entityEntering.isDead():
			return
		
		if not self.isState(GlobalDefine.ENTITY_STATE_FREE):
			return
			
		DEBUG_MSG("%s::onEnterTrap: %i entityEntering=(%s)%i, range_xz=%s, range_y=%s, controllerID=%i, userarg=%i" % \
						(self.getScriptName(), self.id, entityEntering.getScriptName(), entityEntering.id, \
						range_xz, range_y, controllerID, userarg))
		
		self.addEnemy(entityEntering.id, 0)

	def onLeaveTrap(self, entityLeaving, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		There are entities leaving the trap
		"""
		if controllerID != self.territoryControllerID:
			return
		
		if entityLeaving.isDestroyed or entityLeaving.getScriptName() != "Avatar" or entityLeaving.isDead():
			return
			
		INFO_MSG("%s::onLeaveTrap: %i entityLeaving=(%s)%i." % (self.getScriptName(), self.id, \
				entityLeaving.getScriptName(), entityLeaving.id))

	def onAddEnemy(self, entityID):
		"""
		virtual method.
		Enemies enter the list
		"""
		if not self.isState(GlobalDefine.ENTITY_STATE_FIGHT):
			self.changeState(GlobalDefine.ENTITY_STATE_FIGHT)
		
		if self.targetID == 0:
			self.setTarget(entityID)
			
	def onRemoveEnemy(self, entityID):
		"""
		virtual method.
		Delete enemy
		"""
		if self.targetID == entityID:
			self.onLoseTarget()

	def onLoseTarget(self):
		"""
		Enemy lost
		"""
		INFO_MSG("%s::onLoseTarget: %i target=%i, enemyLogSize=%i." % (self.getScriptName(), self.id, \
				self.targetID, len(self.enemyLog)))
				
		self.targetID = 0
		
		if len(self.enemyLog) > 0:
			self.choiceTarget()

	def onEnemyEmpty(self):
		"""
		virtual method.
		Enemy list is empty
		"""
		INFO_MSG("%s::onEnemyEmpty: %i" % (self.getScriptName(), self.id))

		if not self.isState(GlobalDefine.ENTITY_STATE_FREE):
			self.changeState(GlobalDefine.ENTITY_STATE_FREE)
			
		self.backSpawnPos()
		
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_HEARDBEAT == userArg:
			self.onHeardTimer()
