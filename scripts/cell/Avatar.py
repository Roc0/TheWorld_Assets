# -*- coding: utf-8 -*-
import KBEngine
import GlobalDefine
from KBEDebug import *
from interfaces.GameObject import GameObject
from interfaces.Combat import Combat
from interfaces.Spell import Spell
from interfaces.Teleport import Teleport
from interfaces.Dialog import Dialog
from interfaces.State import State
from interfaces.Flags import Flags
from interfaces.Motion import Motion
from interfaces.SkillBox import SkillBox

class Avatar(KBEngine.Entity,
			GameObject, 
			Flags,
			State,
			Motion, 
			SkillBox,
			Combat, 
			Spell, 
			Teleport,
			Dialog):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self) 
		Flags.__init__(self) 
		State.__init__(self) 
		Motion.__init__(self) 
		SkillBox.__init__(self) 
		Combat.__init__(self) 
		Spell.__init__(self) 
		Teleport.__init__(self) 
		Dialog.__init__(self) 
		
		# Set the fastest speed allowed per second, overspeed will be pulled back
		self.topSpeed = self.moveSpeed + 5.0
		# self.topSpeedY = 10.0
		
		# If it is 7, it means that it is in the UE4 map, so in order to match the movement speed of the demo, we set the limit to be larger
		if self.spaceUType == 7:
			self.topSpeed = 0

	def isPlayer(self):
		"""
		virtual method.
		"""
		return True
		
	def startDestroyTimer(self):
		"""
		virtual method.
		
		Start destroying entitytimer
		"""
		pass

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		GameObject.onTimer(self, tid, userArg)
		Spell.onTimer(self, tid, userArg)
		
	def onGetWitness(self):
		"""
		KBEngine method.
		An observer (client) is bound
		"""
		DEBUG_MSG("Avatar::onGetWitness: %i." % self.id)

	def onLoseWitness(self):
		"""
		KBEngine method.
		Unbind an observer (client)
		"""
		DEBUG_MSG("Avatar::onLoseWitness: %i." % self.id)
	
	def onDestroy(self):
		"""
		KBEngine method.
		entity destruction
		"""
		DEBUG_MSG("Avatar::onDestroy: %i." % self.id)
		Teleport.onDestroy(self)
		Combat.onDestroy(self)
		
	def relive(self, exposed, type):
		"""
		defined.
		resurrection
		"""
		if exposed != self.id:
			return
			
		DEBUG_MSG("Avatar::relive: %i, type=%i." % (self.id, type))
		
		# Resurrection
		if type == 0:
			pass
			
		self.fullPower()
		self.changeState(GlobalDefine.ENTITY_STATE_FREE)

	def jump(self, exposed):
		"""
		defined.
		The player jumps and we broadcast this behavior
		"""
		if exposed != self.id:
			return
		
		self.otherClients.onJump()
		
	def onAddEnemy(self, entityID):
		"""
		virtual method.
		Enemies enter the list
		"""
		if not self.isState(GlobalDefine.ENTITY_STATE_FIGHT):
			self.changeState(GlobalDefine.ENTITY_STATE_FIGHT)

	def onEnemyEmpty(self):
		"""
		virtual method.
		Enemy list is empty
		"""
		self.changeState(GlobalDefine.ENTITY_STATE_FREE)
