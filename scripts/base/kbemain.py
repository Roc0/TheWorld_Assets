# -*- coding: utf-8 -*-
import KBEngine
import Watcher
import d_spaces
from KBEDebug import *

def onBaseAppReady(isBootstrap):
	"""
	KBEngine method.
	baseapp is ready
	@param isBootstrap: Whether it is the first baseapp started
	@type isBootstrap: BOOL
	"""
	INFO_MSG('onBaseAppReady: isBootstrap=%s' % isBootstrap)
	
	# Install the monitor
	Watcher.setup()
	
	if isBootstrap:
		# Create spacemanager
		KBEngine.createEntityLocally( "Spaces", {} )

def onReadyForShutDown():
	"""
	KBEngine method.
	The process asks the script layer: I am going to shut down. Is the script ready?
	If it returns True, the process will enter the shutdown process, and other values ​​will cause the process to ask again after a period of time.
	The user can clean up the data of the script layer when receiving the message, so that the work results of the script layer will not be lost due to shutdown.
	"""
	INFO_MSG('onReadyForShutDown()')
	return True

def onBaseAppShutDown(state):
	"""
	KBEngine method.
	The callback function before the baseapp is closed
	@param state:  	0 : Before disconnecting all clients
					1 : Before writing all entities to the database
					2 : After all entities are written to the database
	@type state: int					 
	"""
	INFO_MSG('onBaseAppShutDown: state=%i' % state)
	
def onReadyForLogin(isBootstrap):
	"""
	KBEngine method.
	If the return value is greater than or equal to 1.0, the initialization is all completed, otherwise it returns the prepared progress value 0.0 ~ 1.0.
	Here, you can ensure that the script layer is fully initialized before logging in.
	@param isBootstrap: Whether it is the first baseapp started
	@type isBootstrap: BOOL
	"""
	if not isBootstrap:
		INFO_MSG('initProgress: completed!')
		return 1.0
		
	spacesEntity = KBEngine.globalData["Spaces"]
	
	tmpDatas = list(d_spaces.datas.keys())
	count = 0
	total = len(tmpDatas)
	
	for utype in tmpDatas:
		spaceAlloc = spacesEntity.getSpaceAllocs()[utype]
		if spaceAlloc.__class__.__name__ != "SpaceAllocDuplicate":
			if len(spaceAlloc.getSpaces()) > 0:
				count += 1
		else:
			count += 1
	
	if count < total:
		v = float(count) / total
		INFO_MSG('initProgress: %f' % v)
		return v;
	
	INFO_MSG('initProgress: completed!')
	return 1.0

def onAutoLoadEntityCreate(entityType, dbid):
	"""
	KBEngine method.
	Automatically loaded entity creation method, the engine allows the script layer to re-implement the entity creation, if the script does not implement this method
	The underlying engine uses createEntityAnywhereFromDBID to create entities
	"""
	INFO_MSG('onAutoLoadEntityCreate: entityType=%s, dbid=%i' % (entityType, dbid))
	KBEngine.createEntityAnywhereFromDBID(entityType, dbid)
	
def onInit(isReload):
	"""
	KBEngine method.
	This interface is called when all scripts are initialized after the engine is started
	@param isReload: Whether it was triggered after being rewritten to load the script
	@type isReload: bool
	"""
	INFO_MSG('onInit::isReload:%s' % isReload)

def onFini():
	"""
	KBEngine method.
	The engine is officially shut down
	"""
	INFO_MSG('onFini()')
	
def onCellAppDeath(addr):
	"""
	KBEngine method.
	Some cellapp died
	"""
	WARNING_MSG('onCellAppDeath: %s' % (str(addr)))
	
def onGlobalData(key, value):
	"""
	KBEngine method.
	globalData has changed
	"""
	DEBUG_MSG('onGlobalData: %s' % key)
	
def onGlobalDataDel(key):
	"""
	KBEngine method.
	globalData has been deleted
	"""
	DEBUG_MSG('onDelGlobalData: %s' % key)

def onBaseAppData(key, value):
	"""
	KBEngine method.
	baseAppData has changed
	"""
	DEBUG_MSG('onBaseAppData: %s' % key)
	
def onBaseAppDataDel(key):
	"""
	KBEngine method.
	baseAppData has been deleted
	"""
	DEBUG_MSG('onBaseAppDataDel: %s' % key)

def onLoseChargeCB(ordersID, dbid, success, datas):
	"""
	KBEngine method.
	An unknown order was processed, it may be due to timeout resulting in billing
	Cleared, and received a callback for third-party recharge processing
	"""
	DEBUG_MSG('onLoseChargeCB: ordersID=%s, dbid=%i, success=%i, datas=%s' % \
							(ordersID, dbid, success, datas))


