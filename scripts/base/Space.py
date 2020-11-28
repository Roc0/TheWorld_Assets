# -*- coding: utf-8 -*-
import KBEngine
import random
import SCDefine
import copy
import math
from KBEDebug import *
from interfaces.GameObject import GameObject
import d_entities
import d_spaces
import d_spaces_spawns
import xml.etree.ElementTree as etree 

class Space(KBEngine.Entity, GameObject):
	"""
	An entity that can control the real space on cellapp
	Note: It is an entity, not a real space. The real space exists in the cellapp's memory, and is associated with it and controls the space through this entity.
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		self.createCellEntityInNewSpace(None)
		
		self.spaceUTypeB = self.cellData["spaceUType"]
		
		self.spaceResName = d_spaces.datas.get(self.spaceUTypeB)['resPath']
		
		# The total number of entities created on this map
		self.tmpCreateEntityDatas = copy.deepcopy(d_spaces_spawns.datas.get(self.spaceUTypeB, []))
		
		self.avatars = {}
		self.createSpawnPointDatas()
		
	def createSpawnPointDatas(self):
		"""
		"""
		res = r"scripts\data\spawnpoints\%s_spawnpoints.xml" % (self.spaceResName.replace("\\", "/").split("/")[-1])
		if(len(self.spaceResName) == 0 or not KBEngine.hasRes(res)):
			return
			
		res = KBEngine.getResFullPath(res)
			
		tree = etree.parse(res) 
		root = tree.getroot()
		
		DEBUG_MSG("Space::createSpawnPointDatas: %s" % (res))
		
		for child in root:
			positionNode = child[0][0]
			directionNode = child[0][1]
			scaleNode = child[0][2]
			
			scale = int(((float(scaleNode[0].text) + float(scaleNode[1].text) + float(scaleNode[2].text)) / 3.0) * 10)
			position = (float(positionNode[0].text), float(positionNode[1].text), float(positionNode[2].text))
			direction = [float(directionNode[0].text) / 360 * (math.pi * 2), float(directionNode[1].text) / 360 * (math.pi * 2), float(directionNode[2].text) / 360 * (math.pi * 2)]
			
			if direction[0] - math.pi > 0.0:
				direction[0] -= math.pi * 2
			if direction[1] - math.pi > 0.0:
				direction[1] -= math.pi * 2
			if direction[2] - math.pi > 0.0:
				direction[2] -= math.pi * 2
				
			self.tmpCreateEntityDatas.append([int(child.attrib['name']), \
			position, \
			direction, \
			scale, \
			])
		
	def spawnOnTimer(self, tid):
		"""
		Born monster
		"""
		if len(self.tmpCreateEntityDatas) <= 0:
			self.delTimer(tid)
			return
			
		datas = self.tmpCreateEntityDatas.pop(0)
		
		if datas is None:
			ERROR_MSG("Space::onTimer: spawn %i is error!" % datas[0])

		KBEngine.createEntityAnywhere("SpawnPoint", 
									{"spawnEntityNO"	: datas[0], 	\
									"position"			: datas[1], 	\
									"direction"			: datas[2],		\
									"modelScale"		: datas[3],		\
									"createToCell"		: self.cell})
				
	def loginToSpace(self, avatarEntityCall, context):
		"""
		defined method.
		A player requested to log in to this space
		"""
		avatarEntityCall.createCell(self.cell)
		self.onEnter(avatarEntityCall)
		
	def logoutSpace(self, entityID):
		"""
		defined method.
		A player requested to log out of this space
		"""
		self.onLeave(entityID)
		
	def teleportSpace(self, entityCall, position, direction, context):
		"""
		defined method.
		Request to enter a space
		"""
		entityCall.cell.onTeleportSpaceCB(self.cell, self.spaceUTypeB, position, direction)

	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_SPACE_SPAWN_TICK == userArg:
			self.spawnOnTimer(tid)
		
		GameObject.onTimer(self, tid, userArg)
		
	def onEnter(self, entityCall):
		"""
		defined method.
		Enter the scene
		"""
		self.avatars[entityCall.id] = entityCall
		
		if self.cell is not None:
			self.cell.onEnter(entityCall)
		
	def onLeave(self, entityID):
		"""
		defined method.
		Leave the scene
		"""
		if entityID in self.avatars:
			del self.avatars[entityID]
		
		if self.cell is not None:
			self.cell.onLeave(entityID)

	def onLoseCell(self):
		"""
		KBEngine method.
		Part of the entity's cell is missing
		"""
		KBEngine.globalData["Spaces"].onSpaceLoseCell(self.spaceUTypeB, self.spaceKey)
		GameObject.onLoseCell(self)
		
	def onGetCell(self):
		"""
		KBEngine method.
		Part of the entity's cell was successfully created
		"""
		DEBUG_MSG("Space::onGetCell: %i" % self.id)
		self.addTimer(0.1, 0.1, SCDefine.TIMER_TYPE_SPACE_SPAWN_TICK)
		KBEngine.globalData["Spaces"].onSpaceGetCell(self.spaceUTypeB, self, self.spaceKey)
		GameObject.onGetCell(self)
		

