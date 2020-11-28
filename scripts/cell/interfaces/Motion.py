# -*- coding: utf-8 -*-
import KBEngine
import math
import Math
import time
import random
from KBEDebug import * 

class Motion:
	"""
	Mobile related packages
	"""
	def __init__(self):
		self.nextMoveTime = int(time.time() + random.randint(5, 15))
	
	def stopMotion(self):
		"""
		Stop moving
		"""
		if self.isMoving:
			#INFO_MSG("%i stop motion." % self.id)
			self.cancelController("Movement")
			self.isMoving = False

	def randomWalk(self, basePos):
		"""
		Randomly move entities
		"""
		if self.isMoving:
			return False
			
		if time.time() < self.nextMoveTime:
			return False
		
		while True:
			# Move radius within 30 meters
			if self.canNavigate():
				destPos = self.getRandomPoints(basePos, 30.0, 1, 0)
				
				if len(destPos) == 0:
					self.nextMoveTime = int(time.time() + random.randint(5, 15))
					return False
				
				destPos = destPos[0]
			else:
				rnd = random.random()
				a = 30.0 * rnd				# Move radius within 30 meters
				b = 360.0 * rnd				# Random angle
				x = a * math.cos( b ) 		# Radius * Positive Yuxuan
				z = a * math.sin( b )
				
				destPos = (basePos.x + x, basePos.y, basePos.z + z)

			if self.position.distTo(destPos) < 2.0:
				continue
				
			self.gotoPosition(destPos)
			self.isMoving = True
			self.nextMoveTime = int(time.time() + random.randint(5, 15))
			break

		return True

	def resetSpeed(self):
		walkSpeed = self.getDatas()["moveSpeed"]
		if walkSpeed != self.moveSpeed:
			self.moveSpeed = walkSpeed
				
	def backSpawnPos(self):
		"""
		virtual method.
		"""
		INFO_MSG("%s::backSpawnPos: %i, pos=%s, speed=%f." % \
			(self.getScriptName(), self.id, self.spawnPos, self.moveSpeed * 0.1))
		
		self.resetSpeed()
		self.gotoPosition(self.spawnPos)
	
	def gotoEntity(self, targetID, dist = 0.0):
		"""
		virtual method.
		移动到entity位置
		"""
		if self.isMoving:
			self.stopMotion()
		
		entity = KBEngine.entities.get(targetID)
		if entity is None:
			DEBUG_MSG("%s::gotoEntity: not found targetID=%i" % (targetID))
			return
			
		if entity.position.distTo(self.position) <= dist:
			return

		self.isMoving = True
		self.moveToEntity(targetID, self.moveSpeed * 0.1, dist, None, True, False)
		
	def gotoPosition(self, position, dist = 0.0):
		"""
		virtual method.
		移动到位置
		"""
		if self.isMoving:
			self.stopMotion()

		if self.position.distTo(position) <= 0.05:
			return

		self.isMoving = True
		speed = self.moveSpeed * 0.1
		
		if self.canNavigate():
			self.navigate(Math.Vector3(position), speed, dist, speed, 512.0, 1, 0, None)
		else:
			if dist > 0.0:
				destPos = Math.Vector3(position) - self.position
				destPos.normalise()
				destPos *= dist
				destPos = position - destPos
			else:
				destPos = Math.Vector3(position)
			
			self.moveToPoint(destPos, speed, 0, None, 1, False)

	def getStopPoint(self, yaw = None, rayLength = 100.0):
		"""
		"""
		if yaw is None:yaw = self.yaw
		yaw = (yaw / 2);
		vv = Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
		vv.normalise()
		vv *= rayLength
		
		lastPos = self.position + vv;
		
		pos = KBEngine.raycast(self.spaceID, self.layer, self.position, vv)
		if pos == None:
			pos = lastPos
			
		return pos
		
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onMove(self, controllerId, userarg):
		"""
		KBEngine method.
		Use any mobile related interface of the engine, this interface will be called when a move of the entity is completed
		"""
		#DEBUG_MSG("%s::onMove: %i controllerId =%i, userarg=%s" % \
		#				(self.getScriptName(), self.id, controllerId, userarg))
		self.isMoving = True
		
	def onMoveFailure(self, controllerId, userarg):
		"""
		KBEngine method.
		Use any mobile related interface of the engine, this interface will be called when a move of the entity is completed
		"""
		DEBUG_MSG("%s::onMoveFailure: %i controllerId =%i, userarg=%s" % \
						(self.getScriptName(), self.id, controllerId, userarg))
		
		self.isMoving = False
		
	def onMoveOver(self, controllerId, userarg):
		"""
		KBEngine method.
		Any mobile related interface using the engine will call this interface at the end of the entity movement
		"""	
		self.isMoving = False
