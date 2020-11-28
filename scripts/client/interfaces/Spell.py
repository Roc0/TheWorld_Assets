# -*- coding: utf-8 -*-
import KBEngine
import skills
import GlobalConst
from KBEDebug import * 
from skillbases.SCObject import SCObject

class Spell:
	def __init__(self):
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
		
	def onBuffTick(self, tid):
		"""
		buff's tick
		"""
		DEBUG_MSG("onBuffTick:%i" % tid)
		
	def spellTarget(self, skillID, targetID):
		"""
		Cast a skill on a target entity
		"""
		self.cell.useTargetSkill(skillID, targetID)

Spell._timermap = {}