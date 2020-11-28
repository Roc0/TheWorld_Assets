# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 
from skills.base.SkillInitiative import SkillInitiative

class SkillAttack(SkillInitiative):
	def __init__(self):
		SkillInitiative.__init__(self)

	def canUse(self, caster, receiver):
		"""
		virtual method.
		Can it be used 
		@param caster: Skilled users
		@param receiver: Skill-affected
		"""
		return SkillInitiative.canUse(self, caster, receiver)
		
	def use(self, caster, receiver):
		"""
		virtual method.
		Use skills
		@param caster: Skilled users
		@param receiver: Skill-affected
		"""
		caster.teleportSpace(10013004, (0,0,0), (4,5,6), {})