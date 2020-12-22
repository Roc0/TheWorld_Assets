# -*- coding: utf-8 -*-
import KBEngine
import KBExtra
import json
from KBEDebug import *

class GameObject:
	def __init__(self):
		pass
		
	def getScriptName(self):
		return self.__class__.__name__
		
	def onEnterWorld(self):
		"""
		KBEngine method.
		This entity has entered the world
		"""
		pass
		
	def onLeaveWorld(self):
		"""
		KBEngine method.
		This entity is about to leave the world
		"""
		pass
		
	def set_name(self, oldValue):
		"""
		Property method.
		The server sets the name attribute
		"""
		DEBUG_MSG("%s::set_name: %i changed:%s->%s" % (self.getScriptName(), self.id, oldValue, self.name))
		
		# Inform the presentation layer to change name
		KBEngine.fireEvent("set_name", json.dumps((self.id, self.name)))
		KBEngine.fireEvent("set_class_name", json.dumps((self.id, self.getScriptName())))

	def set_modelID(self, oldValue):
		"""
		Property method.
		The server has set the modelNumber attribute
		"""
		DEBUG_MSG("%s::set_modelID: %i changed:%s->%s" % (self.getScriptName(), self.id, oldValue, self.modelID))
		
		# Inform the presentation layer to change performance
		KBEngine.fireEvent("set_modelID", json.dumps((self.id, self.modelID)))
		
	def set_modelScale(self, oldValue):
		"""
		Property method.
		The server has set the modelNumber attribute
		"""
		DEBUG_MSG("%s::set_modelScale: %i changed:%s->%s" % (self.getScriptName(), self.id, oldValue, self.modelScale))
		
		KBEngine.fireEvent("set_modelScale", json.dumps((self.id, self.modelScale)))
