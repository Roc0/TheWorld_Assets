# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from interfaces.GameObject import GameObject

class NPCObject(GameObject):
	"""
	All non-role entity interface classes
	"""
	def __init__(self):
		GameObject.__init__(self)
		
