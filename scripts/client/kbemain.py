# -*- coding: utf-8 -*-
import KBEngine
import kbesystem
import json
from KBEDebug import *

def onInit(isReload):
	"""
	KBEngine method.
	This interface is called when all scripts are initialized after the engine is started
	@param isReload: Whether it was triggered after being rewritten to load the script
	@type isReload: bool
	"""
	DEBUG_MSG('onInit::isReload = %s' % isReload)
	
def onFinish():
	"""
	KBEngine method.
	When the client is about to shut down, the engine calls this interface
	You can do some game resource cleaning work here
	"""
	pass

def onTargetChanged(entityID):
	"""
	KBEngine method.
	The client selected a target
	"""
	# DEBUG_MSG('onTargetChanged:: entityID = %i' % entityID)
	kbesystem.targetMgr.setTargetID(entityID)
	
def kbengine_onEvent(eventID, args):
	"""
	KBEngine method.
	Events emitted by the app
	@param args: Self-agreement
	"""
	DEBUG_MSG('kbengine_onEvent:: eventID = %s, args=%s' % (str(eventID), str(args)))
	
	if eventID == "reset":
		kbesystem.eventMgr.fire("reset", 0)
	elif eventID == "relive":
		if KBEngine.player() != None:
			KBEngine.player().relive()