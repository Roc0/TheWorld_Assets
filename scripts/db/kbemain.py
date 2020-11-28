# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *

"""
"""

def onDBMgrReady():
	"""
	KBEngine method.
	dbmgr is ready
	"""
	INFO_MSG('onDBMgrReady: bootstrapGroupIndex=%s, bootstrapGlobalIndex=%s' % \
	 (os.getenv("KBE_BOOTIDX_GROUP"), os.getenv("KBE_BOOTIDX_GLOBAL")))

	#KBEngine.addTimer(0.01, 1.0, onTick)

def onTick(timerID):
	"""
	"""
	INFO_MSG('onTick()')

	# Test database query
	KBEngine.executeRawDatabaseCommand("select * from kbe_accountinfos limit 3;", onSqlCallback)

def onDBMgrShutDown():
	"""
	KBEngine method.
	Callback function before this dbmgr is closed
	"""
	INFO_MSG('onDBMgrShutDown()')

def onSelectAccountDBInterface(accountName):
	"""
	KBEngine method.
	This callback implementation returns the database interface corresponding to an account. After the interface is selected, the related operations of dbmgr for this account are completed by the corresponding database interface.
	The database interface is defined in kbengine_defs.xml->dbmgr->databaseInterfaces.
	Use this interface to decide which database the account should be stored in based on accountName.
	"""
	return "default"

def onSqlCallback(result, rows, insertid, error):
	DEBUG_MSG('onSqlCallback: result=%s, rows=%s, insertid=%s, error=%s' % (str(result), str(rows), str(insertid), str(error)))
