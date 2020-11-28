# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import dialogmgr
import skills

def onInit(isReload):
	"""
	KBEngine method.
	This interface is called when all scripts are initialized after the engine is started
	"""
	DEBUG_MSG('onInit::isReload:%s' % isReload)
	dialogmgr.onInit()
	skills.onInit()
	
def onGlobalData(key, value):
	"""
	KBEngine method.
	globalData changes 
	"""
	DEBUG_MSG('onGlobalData: %s' % key)
	
def onGlobalDataDel(key):
	"""
	KBEngine method.
	globalData delete 
	"""
	DEBUG_MSG('onDelGlobalData: %s' % key)

def onCellAppData(key, value):
	"""
	KBEngine method.
	cellAppData changes 
	"""
	DEBUG_MSG('onCellAppData: %s' % key)
	
def onCellAppDataDel(key):
	"""
	KBEngine method.
	cellAppData delete 
	"""
	DEBUG_MSG('onCellAppDataDel: %s' % key)
	
def onSpaceData( spaceID, key, value ):
	"""
	KBEngine method.
	spaceData changes
	@spaceID:  The data is set in the space of this spaceID.  
	@key:  Set key.  
	@value:  The set value, or None if the value is deleted.  
	"""
	DEBUG_MSG('onSpaceData: spaceID=%s, key=%s, value=%s.' % (spaceID, key, value))
	
def onSpaceGeometryLoaded(spaceID, mapping):
	"""
	KBEngine method.
	space A certain part or all chunks and other data are loaded
	The specific part needs to be determined by the scope of the cell
	"""
	DEBUG_MSG('onSpaceGeometryLoaded: spaceID=%s, mapping=%s.' % (spaceID, mapping))
	
def onAllSpaceGeometryLoaded(spaceID, isBootstrap, mapping):
	"""
	KBEngine method.
	Part of or all data such as chunk is loaded
	The specific part needs to be determined by the scope of the cell
	"""
	DEBUG_MSG('onAllSpaceGeometryLoaded: spaceID=%s, isBootstrap=%i, mapping=%s.' % (spaceID, isBootstrap, mapping))
	

