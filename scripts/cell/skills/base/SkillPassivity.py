# -*- coding: utf-8 -*-
import KBEngine
import random
from KBEDebug import * 
from skillbases.SObject import SObject

class SkillPassivity(SObject):
	def __init__(self):
		SObject.__init__(self)

	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		Create this object from the dictionary
		"""
		SObject.loadFromDict(self, dictDatas)
