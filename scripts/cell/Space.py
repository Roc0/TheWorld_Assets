# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from interfaces.GameObject import GameObject

import d_spaces

class Space(KBEngine.Entity, GameObject):
	"""
	Game scene, here represents the wild map
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		
		# A space represents an abstract space. Here, geometric resource data is added to this abstract space. If the data is a 3D scene
		# Navigate pathfinding in this space uses 3D API, if it is 2D geometric data navigate uses astar pathfinding
		resPath = d_spaces.datas.get(self.spaceUType)['resPath']
		#KBEngine.addSpaceGeometryMapping(self.spaceID, None, resPath, True, {0 : "srv_xinshoucun_1.navmesh", 1 : "srv_xinshoucun.navmesh"})
		KBEngine.addSpaceGeometryMapping(self.spaceID, None, resPath)
		
		DEBUG_MSG('created space[%d] entityID = %i, res = %s.' % (self.spaceUType, self.id, resPath))
		
		KBEngine.globalData["space_%i" % self.spaceID] = self.base
	
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onDestroy(self):
		"""
		KBEngine method.
		"""
		del KBEngine.globalData["space_%i" % self.spaceID]
		self.destroySpace()
		
	def onEnter(self, entityCall):
		"""
		defined method.
		Enter the scene
		"""
		DEBUG_MSG('Space::onEnter space[%d] entityID = %i.' % (self.spaceUType, entityCall.id))
		
	def onLeave(self, entityID):
		"""
		defined method.
		Leave the scene
		"""
		DEBUG_MSG('Space::onLeave space[%d] entityID = %i.' % (self.spaceUType, entityID))
		

