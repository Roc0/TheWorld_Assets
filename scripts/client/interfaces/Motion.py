# -*- coding: utf-8 -*-
import KBEngine
import KBExtra
from KBEDebug import * 

class Motion:
	def __init__(self):
		self.set_moveSpeed(0)

	def onMove(self, controllerId, userarg):
		"""
		KBEngine method.
		Use any mobile related interface of the engine, this interface will be called when a move of the entity is completed
		"""
		DEBUG_MSG("%s::onMove: %i controllerId =%i, userarg=%s" % \
						(self.getScriptName(), self.id, controllerId, userarg))

	def onMoveFailure(self, controllerId, userarg):
		"""
		KBEngine method.
		Use any mobile related interface of the engine, this interface will be called when a move of the entity is completed
		"""
		DEBUG_MSG("%s::onMoveFailure: %i controllerId =%i, userarg=%s" % \
						(self.getScriptName(), self.id, controllerId, userarg))
		
	def onMoveOver(self, controllerId, userarg):
		"""
		KBEngine method.
		Any mobile related interface using the engine will call this interface at the end of the entity movement
		"""
		DEBUG_MSG("%s::onMoveOver: %i controllerId =%i, userarg=%s" % \
						(self.getScriptName(), self.id, controllerId, userarg))
		
	def set_moveSpeed(self, oldValue):
		"""
		Property method.
		The server sets the moveSpeed ​​property
		"""
		DEBUG_MSG("%s::set_moveSpeed: %i changed:%s->%s" % (self.getScriptName(), self.id, oldValue, self.moveSpeed))

		# 设置引擎层entity移动速度
		self.velocity = self.moveSpeed * 0.1

