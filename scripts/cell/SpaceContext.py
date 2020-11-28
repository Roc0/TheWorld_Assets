# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import d_spaces

class SpaceContext(dict):
	"""
	Generate space context
	"""
	def __init__(self, entity):
		pass
	
	@staticmethod
	def create(entity):
		return {}


class SpaceDuplicateContext(SpaceContext):
	"""
	The context in which the space copy is generated
	To enter the copy, you need to hold the key (spaceKey)
	"""
	def __init__(self, entity):
		SpaceContext.__init__(self, entity)

	@staticmethod
	def create(entity):
		return {"spaceKey" : entity.dbid}
		
def createContext(entity, spaceUType):
	"""
	"""
	spaceData = d_spaces.datas.get(spaceUType)
	
	return {
		"Space" : SpaceContext,
		"SpaceDuplicate" : SpaceDuplicateContext,
	}[spaceData["entityType"]].create(entity)