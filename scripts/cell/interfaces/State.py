# -*- coding: utf-8 -*-
#
"""
Handle some states of entity
"""
import GlobalDefine
from KBEDebug import *

class State:
	"""
	"""
	def __init__(self):
		self._forbidCounter = [0] * len(GlobalDefine.FORBID_ALL)
		self.forbidCounterInc(GlobalDefine.FORBID_ACTIONS[self.state])

	def initEntity(self):
		"""
		virtual method.
		"""
		pass
		
	def isState(self, state):
		return self.state == state
	
	def isSubState(self, state):
		return self.subState == state
	
	def isForbid(self, forbid):
		return self.forbids & forbid
	
	def getState(self):
		return self.state

	def getSubState(self):
		return self.subState

	def getForbidCounter(self, forbid):
		"""
		Get the data of the prohibited counter
		"""
		return self._forbidCounter[GlobalDefine.FORBID_ALL.index(forbid)]
					
	def changeSubState(self, subState):
		"""
		Change current substate
		GlobalDefine.ENTITY_SUB_STATE_**
		"""
		if self.subState != subState:
			oldSubState = self.subState
			self.subState = subState
			self.onSubStateChanged_(oldSubState, self.subState)

	def forbidCounterInc(self, forbids):
		"""
		Prohibit counter increment
		"""
		fbList = []
		for i, fb in enumerate(GlobalDefine.FORBID_ALL):
			if forbids & fb:
				if self._forbidCounter[i] == 0:
					fbList.append(fb)
				self._forbidCounter[i] += 1

		# kbe Any time a value is assigned to a defined attribute will generate an event
		if len(fbList) > 0:
			self.forbids |= forbids
			for fb in fbList:
				self.onForbidChanged_(fb, True)

	def forbidCounterDec(self, forbids):
		"""
		禁止计数器减一
		"""
		fbList = []
		for i, fb in enumerate(GlobalDefine.FORBID_ALL):
			if forbids & fb:
				self._forbidCounter[i] -= 1
				if self._forbidCounter[i] == 0:
					fbList.append(fb)

		# kbe Any time a value is assigned to a defined attribute will generate an event
		if len(fbList) > 0:
			self.forbids &= ~forbids
			for fb in fbList:
				self.onForbidChanged_(fb, False)
		
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onForbidChanged_(self, forbid, isInc):
		"""
		virtual method.
		Entity prohibited conditions change
		@param isInc		:	Is it increased
		"""
		pass

	def onStateChanged_(self, oldstate, newstate):
		"""
		virtual method.
		entity state changed
		"""
		self.changeSubState(GlobalDefine.ENTITY_SUB_STATE_NORMAL)
		INFO_MSG("%s:onStateChanged_: %i oldstate=%i to newstate=%i, forbids=%s, subState=%i." % (self.getScriptName(), \
				self.id, oldstate, newstate, self._forbidCounter, self.subState))

	def onSubStateChanged_(self, oldSubState, newSubState):
		"""
		virtual method.
		Substate changed
		"""
		#INFO_MSG("%i oldSubstate=%i to newSubstate=%i" % (self.id, oldSubState, newSubState))
		pass
		
	#--------------------------------------------------------------------------------------------
	#                              defined
	#--------------------------------------------------------------------------------------------
	def changeState(self, state):
		"""
		defined
		Change the current main state
		GlobalDefine.ENTITY_STATE_**
		"""
		if self.state != state:
			oldstate = self.state
			self.state = state
			self.forbidCounterDec(GlobalDefine.FORBID_ACTIONS[oldstate])
			self.forbidCounterInc(GlobalDefine.FORBID_ACTIONS[state])
			self.onStateChanged_(oldstate, state)


