# -*- coding: utf-8 -*-
import KBEngine
import random
from KBEDebug import * 
from skills.base.SkillInitiative import SkillInitiative

class SkillAttack(SkillInitiative):
	def __init__(self):
		SkillInitiative.__init__(self)

	def canUse(self, caster, scObject):
		"""
		virtual method.
		Can it be used 
		@param caster: Skilled users
		@param receiver: Skill-affected
		"""
		return SkillInitiative.canUse(self, caster, scObject)
		
	def use(self, caster, scObject):
		"""
		virtual method.
		使用技能
		@param caster: Skilled users
		@param receiver: Skill-affected
		"""
		return SkillInitiative.use(self, caster, scObject)
		
	def receive(self, caster, receiver):
		"""
		virtual method.
		Can do something to the subject
		"""
		if self.getID() == 1:
			receiver.recvDamage(caster.id, self.getID(), 0, random.randint(0, 10))
		elif self.getID() == 1000101:
			#caster.position = caster.getStopPoint(caster.yaw, 15.0)
			receiver.recvDamage(caster.id, self.getID(), 0, random.randint(0, 100))
		elif self.getID() == 2000101:
			receiver.recvDamage(caster.id, self.getID(), 0, random.randint(0, 100))
		elif self.getID() == 3000101:
			receiver.recvDamage(caster.id, self.getID(), 0, random.randint(0, 100))
		elif self.getID() == 4000101:
			receiver.recvDamage(caster.id, self.getID(), 0, random.randint(0, 100))
		elif self.getID() == 5000101:
			receiver.recvDamage(caster.id, self.getID(), 0, random.randint(0, 100))
		elif self.getID() == 6000101:
			receiver.recvDamage(caster.id, self.getID(), 0, random.randint(0, 100))
		elif self.getID() == 7000101:
			receiver.recvDamage(caster.id, self.getID(), 0, random.randint(0, 10))