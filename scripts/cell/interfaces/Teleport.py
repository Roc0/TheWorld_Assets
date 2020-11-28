# -*- coding: utf-8 -*-
import KBEngine
import SpaceContext
from KBEDebug import * 

class Teleport:
	def __init__(self):
		pass
		
	def teleportSpace(self, spaceUType, position, direction, context):
		"""
		defined.
		Send to a scene
		"""
		assert self.base != None
		self.lastSpaceUType = self.spaceUType
		
		inputContext = SpaceContext.createContext(self, spaceUType)
		if type(context) == dict:
			inputContext.update(context)

		self.getSpaces().teleportSpace(self.base, spaceUType, position, direction, inputContext)

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTeleportSpaceCB(self, spaceCellEntityCall, spaceUType, position, direction):
		"""
		defined.
		baseapp returns teleportSpace callback
		"""
		DEBUG_MSG("Teleport::onTeleportSpaceCB: %i spaceID=%s, spaceUType=%i, pos=%s, dir=%s." % \
					(self.id, spaceCellEntityCall.id, spaceUType, position, direction))
		
		
		self.getCurrSpaceBase().onLeave(self.id)
		self.teleport(spaceCellEntityCall, position, direction)
		
	def onTeleportSuccess(self, nearbyEntity):
		"""
		KBEngine method.
		"""
		DEBUG_MSG("Teleport::onTeleportSuccess: %s" % (nearbyEntity))
		self.getCurrSpaceBase().onEnter(self.base)
		self.spaceUType = self.getCurrSpace().spaceUType
		
	def onDestroy(self):
		"""
		entity destruction
		"""
		self.getCurrSpaceBase().logoutSpace(self.id)
