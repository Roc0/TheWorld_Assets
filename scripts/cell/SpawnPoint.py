# -*- coding: utf-8 -*-
import KBEngine
import SCDefine
from KBEDebug import *
from interfaces.GameObject import GameObject
import d_entities

class SpawnPoint(KBEngine.Entity, GameObject):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		self.addTimer(1, 0, SCDefine.TIMER_TYPE_SPAWN)
		
	def spawnTimer(self):
		datas = d_entities.datas.get(self.spawnEntityNO)
		
		if datas is None:
			ERROR_MSG("SpawnPoint::spawn:%i not found." % self.spawnEntityNO)
			return
			
		params = {
			"spawnID"	: self.id,
			"spawnPos" : tuple(self.position),
			"uid" : datas["id"],
			"utype" : datas["etype"],
			"modelID" : datas["modelID"],
			"modelScale" : self.modelScale,
			"dialogID" : datas["dialogID"],
			"name" : datas["name"],
			"descr" : datas.get("descr", ''),
		}
		
		e = KBEngine.createEntity(datas["entityType"], self.spaceID, tuple(self.position), tuple(self.direction), params)

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_SPAWN == userArg:
			self.spawnTimer()
		
		GameObject.onTimer(self, tid, userArg)

	def onRestore(self):
		"""
		KBEngine method.
		Part of the entity's cell was successfully restored
		"""
		GameObject.onRestore(self)
		self.addTimer(1, 0, SCDefine.TIMER_TYPE_SPAWN)
		
	def onDestroy(self):
		"""
		KBEngine method.
		The current entity is about to be destroyed by the engine
		You can do some pre-destruction work here
		"""
		DEBUG_MSG("onDestroy(%i)" % self.id)
	
	def onEntityDestroyed(self, entityNO):
		"""
		defined.
		The born entity is destroyed and needs to be rebuilt?
		"""
		self.addTimer(1, 0, SCDefine.TIMER_TYPE_SPAWN)
		
