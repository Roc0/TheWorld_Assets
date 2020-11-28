# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 
from skillbases.SObject import SObject

class DBuff(SObject):
	def __init__(self):
		SObject.__init__(self)

		self._loopTime = 0		# Cycle trigger time
		self._totalTime = 0		# duration
		
	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		Create this object from the dictionary
		"""
		SObject.loadFromDict(self, dictDatas)
		self._loopTime = dictDatas.get('looptime', 0)
		self._totalTime = dictDatas.get('totaltime', 0)
		
	def onLoopTrigger(self, context):
		"""
		virtual method.
		Periodic trigger
		@param context: buff/debuff context
		"""
		pass
		
	def onAttach(self, context):
		"""
		virtual method.
		When buff/debuff is bound
		@param context: buff/debuff context
		"""
		pass
		
	def onDetach(self, context):
		"""
		virtual method.
		When buff/debuff is unbound
		@param context: buff/debuff context
		"""
		pass
