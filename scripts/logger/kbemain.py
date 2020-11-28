# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *

"""
The logger process mainly handles the log saving work of the KBEngine server.
"""


def onLoggerAppReady():
	"""
	KBEngine method.
	logger is ready
	"""
	INFO_MSG('onLoggerAppReady: bootstrapGroupIndex=%s, bootstrapGlobalIndex=%s' % \
	 (os.getenv("KBE_BOOTIDX_GROUP"), os.getenv("KBE_BOOTIDX_GLOBAL")))

def onLoggerAppShutDown():
	"""
	KBEngine method.
	Callback function before this logger is closed
	"""
	INFO_MSG('onLoggerAppShutDown()')

def onReadyForShutDown():
	"""
	KBEngine method.
	The process asks the script layer: I'm going to shut down. Is the script ready?
	If it returns True, the process will enter the shutdown process, and other values ​​will cause the process to ask again after a period of time.
	The user can clean up the data of the script layer when receiving the message, so that the work results of the script layer will not be lost due to shutdown.
	"""
	INFO_MSG('onReadyForShutDown()')
	return True

def onLogWrote(logData):
	"""
	KBEngine method.
	logger writes a callback after a log,
	Users in need can write logs to other places (such as databases)
	If it returns False, the log will not be written to the disk file.
	If a string is returned, the log will be replaced with the content returned.
	@param logData: bytes
	"""
	return True

