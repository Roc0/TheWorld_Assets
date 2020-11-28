# -*- coding: utf-8 -*-
import KBEngine
import Functor
import d_spaces
import SCDefine
import Watcher
from KBEDebug import *
from SpaceAlloc import *
from interfaces.GameObject import GameObject

class Spaces(KBEngine.Entity, GameObject):
	"""
	This is a space manager encapsulated by the script layer
	KBEngine's space is an abstract space concept. A space can be regarded as a game scene, game room, or even a universe by the script layer.
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		
		# Initialize the space allocator
		self.initAlloc()
		
		# Register the entityCall of this manager to the global shared data for easy access in all logical processes
		KBEngine.globalData["Spaces"] = self
	
	def initAlloc(self):
		# Register a timer, in this timer we create some NPC every cycle until all the creation is completed
		self._spaceAllocs = {}
		DEBUG_MSG("%s::initAlloc: %i, Registering timer to create Space" % (self.getScriptName(), self.id))
		id_timer = self.addTimer(3, 1, SCDefine.TIMER_TYPE_CREATE_SPACES)
		DEBUG_MSG("%s::initAlloc: %i, Registered timer to create Space (timer id %i)" % (self.getScriptName(), self.id, id_timer))
		#id_timer = self.addTimer(11, 22, SCDefine.TIMER_TYPE_CREATE_SPACES)
		#DEBUG_MSG("%s::initAlloc: %i, Registered timer to create Space (timer id %i)" % (self.getScriptName(), self.id, id_timer))
		
		self._tmpDatas = list(d_spaces.datas.keys())
		for utype in self._tmpDatas:
			spaceData = d_spaces.datas.get(utype)
			if spaceData["entityType"] == "SpaceDuplicate":
				self._spaceAllocs[utype] = SpaceAllocDuplicate(utype)
			else:
				self._spaceAllocs[utype] = SpaceAlloc(utype)
	
	def getSpaceAllocs(self):
		return self._spaceAllocs
		
	def createSpaceOnTimer(self, tid):
		"""
		Create space
		"""
		if len(self._tmpDatas) > 0:
			spaceUType = self._tmpDatas.pop(0)
			self._spaceAllocs[spaceUType].init()
			
		if len(self._tmpDatas) <= 0:
			del self._tmpDatas
			self.delTimer(tid)
			
	def loginToSpace(self, avatarEntity, spaceUType, context):
		"""
		defined method.
		A player requests to log in to a space
		"""
		self._spaceAllocs[spaceUType].loginToSpace(avatarEntity, context)
	
	def logoutSpace(self, avatarID, spaceKey):
		"""
		defined method.
		A player requested to log out of this space
		"""
		for spaceAlloc in self._spaceAllocs.values():
			space = spaceAlloc.getSpaces().get(spaceKey)
			if space:
				space.logoutSpace(avatarID)
				
	def teleportSpace(self, entityCall, spaceUType, position, direction, context):
		"""
		defined method.
		Request to enter a space
		"""
		self._spaceAllocs[spaceUType].teleportSpace(entityCall, position, direction, context)

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_CREATE_SPACES == userArg:
			self.createSpaceOnTimer(tid)
		
		GameObject.onTimer(self, tid, userArg)
		
	def onSpaceLoseCell(self, spaceUType, spaceKey):
		"""
		defined method.
		The cell of space is destroyed
		"""
		self._spaceAllocs[spaceUType].onSpaceLoseCell(spaceKey)
		
	def onSpaceGetCell(self, spaceUType, spaceEntityCall, spaceKey):
		"""
		defined method.
		The cell of space is created
		"""
		self._spaceAllocs[spaceUType].onSpaceGetCell(spaceEntityCall, spaceKey)

