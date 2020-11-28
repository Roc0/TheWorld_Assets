# -*- coding: utf-8 -*-
import KBEngine
import skills
import GlobalConst
import SCDefine
from KBEDebug import * 

class SkillBox:
	def __init__(self):
		# If the player does not learn skills, these skills are added by default
		if len(self.skills) == 0:
			self.skills.append(1)
			self.skills.append(1000101)
			self.skills.append(2000101)
			self.skills.append(3000101)
			self.skills.append(4000101)
			self.skills.append(5000101)
			self.skills.append(6000101)

	def hasSkill(self, skillID):
		"""
		"""
		return skillID in self.skills

	#--------------------------------------------------------------------------------------------
	#                              defined
	#--------------------------------------------------------------------------------------------
	def requestPull(self, exposed):
		"""
		exposed
		"""
		if self.id != exposed:
			return
		
		DEBUG_MSG("SkillBox::requestPull: %i skills=%i" % (self.id, len(self.skills)))
		for skillID in self.skills:
			self.client.onAddSkill(skillID)
			
	def addSkill(self, skillID):
		"""
		defined method.
		"""
		self.skills.append(skillID)

	def removeSkill(self, skillID):
		"""
		defined method.
		"""
		self.skills.remove(skillID)
		
	def useTargetSkill(self, srcEntityID, skillID, targetID):
		"""
		exposed.
		Cast a skill on a target entity
		"""
		if srcEntityID != self.id:
			return
		
		self.spellTarget(skillID, targetID)
