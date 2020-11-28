# -*- coding: utf-8 -*-
import KBEngine
import random
import GlobalConst
from KBEDebug import * 
from skillbases.SObject import SObject
from skillbases.SCObject import SCObject

class SkillInitiative(SObject):
	def __init__(self):
		SObject.__init__(self)
		
	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		Create this object from the dictionary
		"""
		SObject.loadFromDict(self, dictDatas)
		
		# Spell speed
		self.speed = dictDatas.get('speed', 0)
		
		# Chant time
		self.intonateTime = dictDatas.get("intonateTime", 0.0)
		
		# Minimum and maximum cast range
		self.rangeMin = dictDatas.get('rangeMin', 0)
		self.rangeMax = dictDatas.get('rangeMax', 2)
		self.__castMaxRange = dictDatas.get("rangeMaxAdd", 10.0)
		
		# Casting Turn
		self.__isRotate	= dictDatas.get("isRotate", True)
		
		# Maximum number of operations
		self.maxReceiveCount = dictDatas.get("maxReceiverCount", 999)
		
		# cd
		self.limitCDs = dictDatas.get("limitCDs", [1])
		self.springCDs = dictDatas.get("springCDs", [])
		
	def getRangeMin(self, caster):
		"""
		virtual method.
		"""
		return self.rangeMin

	def getRangeMax(self, caster):
		"""
		virtual method.
		"""
		return self.rangeMax
		
	def getIntonateTime(self, caster):
		"""
		virtual method.
		"""
		return self.intonateTime
		
	def getCastMaxRange(self, caster):
		return self.getRangeMax(caster) + self.__castMaxRange

	def getSpeed(self):
		return self.speed

	def isRotate(self):
		return self.__isRotate

	def getMaxReceiverCount(self):
		return self.maxReceiverCount

	def canUse(self, caster, scObject):
		"""
		virtual method.
		Can it be used 
		@param caster: Skilled users
		@param receiver: Skill-affected
		"""
		return GlobalConst.GC_OK
		
	def use(self, caster, scObject):
		"""
		virtual method.
		使用技能
		@param caster: Skilled users
		@param receiver: Skill-affected
		"""
		self.cast(caster, scObject)
		return GlobalConst.GC_OK
		
	def cast(self, caster, scObject):
		"""
		virtual method.
		Casting skills
		"""
		delay = self.distToDelay(caster, scObject)
		#INFO_MSG("%i cast skill[%i] delay=%s." % (caster.id, self.id, delay))
		if delay <= 0.1:
			self.onArrived(caster, scObject)
		else:
			#INFO_MSG("%i add castSkill:%i. delay=%s." % (caster.id, self.id, delay))
			caster.addCastSkill(self, scObject, delay)

		self.onSkillCastOver_(caster, scObject)
		
	def distToDelay(self, caster, scObject):
		"""
		"""
		return scObject.distToDelay(self.getSpeed(), caster.position)
		
	def onArrived(self, caster, scObject):
		"""
		virtual method.
		Reached the goal
		"""
		self.receive(caster, scObject.getObject())
		
	def receive(self, caster, receiver):
		"""
		virtual method.
		Can do something to the subject
		"""
		pass

	def onSkillCastOver_(self, caster, scObject):
		"""
		virtual method.
		Spell cast notification
		"""
		pass
