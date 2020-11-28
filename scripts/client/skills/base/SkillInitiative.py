# -*- coding: utf-8 -*-
import KBEngine
import GlobalConst
from KBEDebug import * 
from skillbases.SObject import SObject

class SkillInitiative(SObject):
	def __init__(self):
		SObject.__init__(self)

	def canUse(self, caster, receiver):
		"""
		virtual method.
		Can it be used 
		@param caster: Skilled users
		@param receiver: Skill-affected
		"""
		return GlobalConst.GC_OK
		
	def use(self, caster, receiver):
		"""
		virtual method.
		Use skills
		@param caster: Skilled users
		@param receiver: Skill-affected
		"""
		pass