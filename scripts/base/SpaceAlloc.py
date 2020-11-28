# -*- coding: utf-8 -*-
import KBEngine
import Functor
from KBEDebug import *
import d_entities
import d_spaces
import copy

CONST_WAIT_CREATE = -1

class SpaceAlloc:
	"""
	Normal scene allocator
	"""
	def __init__(self, utype):
		self._spaces = {}
		self._utype = utype
		self._pendingLogonEntities = {}
		self._pendingEnterEntityMBs = {}
		
	def init(self):
		"""
		virtual method.
		"""
		self.createSpace(0, {})
	
	def getSpaces(self):
		return self._spaces
		
	def createSpace(self, spaceKey, context):
		"""
		"""
		if spaceKey <= 0:
			spaceKey = KBEngine.genUUID64()
			
		context = copy.copy(context)
		spaceData = d_spaces.datas.get(self._utype)
		KBEngine.createEntityAnywhere(spaceData["entityType"], \
											{"spaceUType" : self._utype,	\
											"spaceKey" : spaceKey,	\
											"context" : context,	\
											}, \
											Functor.Functor(self.onSpaceCreatedCB, spaceKey))
											
	def onSpaceCreatedCB(self, spaceKey, space):
		"""
		Callback after a space is created
		"""
		DEBUG_MSG("Spaces::onSpaceCreatedCB: space %i. entityID=%i" % (self._utype, space.id))

	def onSpaceLoseCell(self, spaceKey):
		"""
		The cell of space is created
		"""
		del self._spaces[spaceKey]
		
	def onSpaceGetCell(self, spaceEntityCall, spaceKey):
		"""
		The cell of space is created
		"""
		DEBUG_MSG("Spaces::onSpaceGetCell: space %i. entityID=%i, spaceKey=%i" % (self._utype, spaceEntityCall.id, spaceKey))
		self._spaces[spaceKey] = spaceEntityCall

		pendingLogonEntities = self._pendingLogonEntities.pop(spaceKey, [])
		pendingEnterEntityMBs = self._pendingEnterEntityMBs.pop(spaceKey, [])
		
		for e, context in pendingLogonEntities:
			self.loginToSpace(e, context)
		
		for mb, pos, dir, context in pendingEnterEntityMBs:
			self.teleportSpace(mb, pos, dir, context)
		
	def alloc(self, context):
		"""
		virtual method.
		Allocate a space
		"""
		if self._spaces == {}:
			return None
		
		return list(self._spaces.values())[0]
		
	def loginToSpace(self, avatarEntity, context):
		"""
		virtual method.
		A player requests to log in to a space
		"""
		spaceKey = context.get("spaceKey", 0)
		space = self.alloc({"spaceKey" : spaceKey})
		if space is None:
			ERROR_MSG("Spaces::loginToSpace: not found space %i. login to space is failed! spaces=%s" % (self._utype, str(self._spaces)))
			return
		
		if space == CONST_WAIT_CREATE:
			if spaceKey not in self._pendingLogonEntities:
				self._pendingLogonEntities[spaceKey] = [(avatarEntity, context)]
			else:
				self._pendingLogonEntities[spaceKey].append((avatarEntity, context))
				
			DEBUG_MSG("Spaces::loginToSpace: avatarEntity=%s add pending." % avatarEntity.id)
			return
		
		DEBUG_MSG("Spaces::loginToSpace: avatarEntity=%s" % avatarEntity.id)
		space.loginToSpace(avatarEntity, context)

	def teleportSpace(self, entityCall, position, direction, context):
		"""
		virtual method.
		Request to enter a space
		"""
		space = self.alloc(context)
		if space is None:
			ERROR_MSG("Spaces::teleportSpace: not found space %i. login to space is failed!" % self._utype)
			return
		
		if space == CONST_WAIT_CREATE:
			spaceKey = context.get("spaceKey", 0)
			if spaceKey not in self._pendingEnterEntityMBs:
				self._pendingEnterEntityMBs[spaceKey] = [(entityCall, position, direction, context)]
			else:
				self._pendingEnterEntityMBs[spaceKey].append((entityCall, position, direction, context))

			DEBUG_MSG("Spaces::teleportSpace: avatarEntity=%s add pending." % entityCall.id)
			return
			
		DEBUG_MSG("Spaces::teleportSpace: entityCall=%s" % entityCall)
		space.teleportSpace(entityCall, position, direction, context)
		
class SpaceAllocDuplicate(SpaceAlloc):
	"""
	Replica allocator
	"""
	def __init__(self, utype):
		SpaceAlloc.__init__(self, utype)

	def init(self):
		"""
		virtual method.
		"""
		pass # The copy does not need to be initialized to create one
		
	def alloc(self, context):
		"""
		virtual method.
		Allocate a space
		For replicas, creating a replica uses the player’s dbid as the space key,
		Anyone who wants to enter this copy needs to know this key.
		"""
		spaceKey = context.get("spaceKey", 0)
		space = self._spaces.get(spaceKey)
		
		assert spaceKey != 0
		
		if space is None:
			self.createSpace(spaceKey, context)
			return CONST_WAIT_CREATE
		
		return space
