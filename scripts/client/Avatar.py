# -*- coding: utf-8 -*-
import KBEngine
import KBExtra
import kbesystem
from KBEDebug import *
from kbesystem.event.EventHandler import EventHandler
from interfaces.GameObject import GameObject
from interfaces.Dialog import Dialog
from interfaces.Teleport import Teleport
from interfaces.State import State
from interfaces.Flags import Flags
from interfaces.Combat import Combat
from interfaces.Spell import Spell
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
			Dialog,
			Teleport):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		Flags.__init__(self) 
		State.__init__(self) 
		Motion.__init__(self) 
		SkillBox.__init__(self) 
		Combat.__init__(self) 
		Spell.__init__(self) 
		Dialog.__init__(self)
		Teleport.__init__(self)
		
	def onEnterSpace(self):
		"""
		KBEngine method.
		This entity has entered a new space
		"""
		DEBUG_MSG("%s::onEnterSpace: %i." % (self.getScriptName(), self.id))

	def onLeaveSpace(self):
		"""
		KBEngine method.
		This entity will leave the current space
		"""
		DEBUG_MSG("%s::onLeaveSpace: %i." % (self.getScriptName(), self.id))
		
	def onBecomePlayer( self ):
		"""
		KBEngine method.
		Called when this entity is defined as a player by the engine
		"""
		DEBUG_MSG("%s::onBecomePlayer: %i." % (self.getScriptName(), self.id))

	def onBecomeNonPlayer( self ):  
		"""
		KBEngine method.
		Called when this entity changes from player to non-player
		"""
		DEBUG_MSG("%s::onBecomeNonPlayer: %i." % (self.getScriptName(), self.id))

	def relive(self):
		"""
		resurrection
		"""
		DEBUG_MSG("%s::relive: %i." % (self.getScriptName(), self.id))
		self.cell.relive(1)
		
	def onJump(self):
		"""
		defined method.
		Player jumping
		"""
		pass
		
	def set_own_val(self, oldValue):
		"""
		Property method.
		The server has set properties
		"""
		DEBUG_MSG("%s::set_own_val: %i changed:%s->%s" % (self.getScriptName(), self.id, oldValue, self.own_val))
		
class PlayerAvatar(Avatar, EventHandler):
	def __init__(self): # This engine will not be called automatically
		EventHandler.__init__(self)
		self.registerEvents()
	
	def registerEvents(self):
		"""
		Register event listener
		"""
		kbesystem.eventMgr.registerEventHandler("TargetMgr.onTargetChanged", self.onTargetChanged)
	
	def unregisterEventHandler(self):
		kbesystem.eventMgr.unregisterEventHandler("TargetMgr.onTargetChanged", self.onTargetChanged)
		
	def onTargetChanged(self, _preTargetID, _currTargetID):
		"""
		An event occurs, the goal changes
		"""
		DEBUG_MSG("%s::onTargetChanged: %i, preTargetID=%i, currTargetID=%i." % \
			(self.getScriptName(), self.id, _preTargetID, _currTargetID))
		
		if _preTargetID == _currTargetID:
			self.spellTarget(1, _currTargetID)

	def onBecomePlayer( self ):
		"""
		KBEngine method.
		Called when this entity is defined as a player by the engine
		"""
		DEBUG_MSG("%s::onBecomePlayer: %i." % (self.getScriptName(), self.id))
		self.__init__()
		self.pullSkills()
		
	def onBecomeNonPlayer( self ):  
		"""
		KBEngine method.
		Called when this entity changes from player to non-player
		"""
		DEBUG_MSG("%s::onBecomeNonPlayer: %i." % (self.getScriptName(), self.id))
		self.unregisterEventHandler()
		
	def onJump(self):
		"""
		defined method.
		Player jumping
		"""
		pass