# -*- coding: utf-8 -*-
import KBEngine
import skills
import GlobalConst
import SCDefine
from KBEDebug import * 
import skillbases.SCObject as SCObject

class Spell:
	def __init__(self):
		#self.addTimer(1,1,SCDefine.TIMER_TYPE_BUFF_TICK)
		pass
		
	def addDBuff(self, buffData):
		"""
		defined method.
		Add buff
		"""
		pass

	def removeDBuff(self, buffData):
		"""
		defined method.
		Remove buff
		"""
		pass
	
	def intonate(self, skill, scObject):
		"""
		Chanting Skills
		"""
		pass
		
	def spellTarget(self, skillID, targetID):
		"""
		defined.
		Cast a skill on a target entity
		"""
		DEBUG_MSG("Spell::spellTarget(%i):skillID=%i, targetID=%i" % (self.id, skillID, targetID))
		
		skill = skills.getSkill(skillID)
		if skill is None:
			ERROR_MSG("Spell::spellTarget(%i):skillID=%i not found" % (self.id, skillID))
			return

		target = KBEngine.entities.get(targetID)
		if target is None:
			ERROR_MSG("Spell::spellTarget(%i):targetID=%i not found" % (self.id, targetID))
			return
		
		scobject = SCObject.createSCEntity(target)
		ret = skill.canUse(self, scobject)
		if ret != GlobalConst.GC_OK:
			ERROR_MSG("Spell::spellTarget(%i): cannot spell skillID=%i, targetID=%i, code=%i" % (self.id, skillID, targetID, ret))
			return
			
		skill.use(self, scobject)
	
	def spellPosition(self, position):
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
		if SCDefine.TIMER_TYPE_BUFF_TICK == userArg:
			self.onBuffTick()

	def onBuffTick(self):
		"""
		buff's tick
		Here you can poll all the buffs and execute the buffs that need to be executed
		"""
		DEBUG_MSG("onBuffTick")
