# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *

"""
The loginapp process mainly handles KBEngine server login and account creation.
The script currently supports several functions:
1: Check account registration
2: Login check
3: Custom socket callback, refer to Poller implementation in interface
"""


def onLoginAppReady():
	"""
	KBEngine method.
	loginapp is ready
	"""
	INFO_MSG('onLoginAppReady: bootstrapGroupIndex=%s, bootstrapGlobalIndex=%s' % \
	 (os.getenv("KBE_BOOTIDX_GROUP"), os.getenv("KBE_BOOTIDX_GLOBAL")))

	#KBEngine.addTimer(0.01, 1.0, onTick)

def onTick(timerID):
	"""
	"""
	INFO_MSG('onTick()')

def onLoginAppShutDown():
	"""
	KBEngine method.
	The callback function before this loginapp is closed
	"""
	INFO_MSG('onLoginAppShutDown()')

def onRequestLogin(loginName, password, clientType, datas):
	"""
	KBEngine method.
	Callback when the account requests login
	Here you can also queue the login and store the queued information in datas
	"""
	INFO_MSG('onRequestLogin() loginName=%s, clientType=%s' % (loginName, clientType))

	errorno = KBEngine.SERVER_SUCCESS
	
	if len(loginName) > 64:
		errorno = KBEngine.SERVER_ERR_NAME

	if len(password) > 64:
		errorno = KBEngine.SERVER_ERR_PASSWORD

	return (errorno, loginName, password, clientType, datas)

def onLoginCallbackFromDB(loginName, accountName, errorno, datas):
	"""
	KBEngine method.
	Db verification callback after account request login
	loginName: The login name is the name entered by the client when logging in.
	accountName: The account name is the name queried by dbmgr.
	errorno: KBEngine.SERVER_ERR_*
	This mechanism is used to log into the server with one account multiple name system or multiple third-party account systems.
	The client will also return the account name when getting the baseapp address. The client should log in using this account name when logging into baseapp
	"""
	INFO_MSG('onLoginCallbackFromDB() loginName=%s, accountName=%s, errorno=%s' % (loginName, accountName, errorno))
	
def onRequestCreateAccount(accountName, password, datas):
	"""
	KBEngine method.
	Callback when requesting account creation
	"""
	INFO_MSG('onRequestCreateAccount() %s' % (accountName))

	errorno = KBEngine.SERVER_SUCCESS
	
	if len(accountName) > 64:
		errorno = KBEngine.SERVER_ERR_NAME

	if len(password) > 64:
		errorno = KBEngine.SERVER_ERR_PASSWORD
		
	return (errorno, accountName, password, datas)

def onCreateAccountCallbackFromDB(accountName, errorno, datas):
	"""
	KBEngine method.
	Db verification callback after account registration request
	errorno: KBEngine.SERVER_ERR_*
	"""
	INFO_MSG('onCreateAccountCallbackFromDB() accountName=%s, errorno=%s' % (accountName, errorno))
