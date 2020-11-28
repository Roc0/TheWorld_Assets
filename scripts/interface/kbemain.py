# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *
from Poller import Poller

"""
The interfaces process mainly handles the access of the KBEngine server and the third-party platform.
(Note: because interfaces is a single-threaded server, if you need to use Python's http server library, it is recommended to use asynchronous (for example: Tornado), otherwise it will block the main thread. External HTTP requests can use KBEngine.urlopen asynchronous requests.)
Currently supports several functions:
1: Register an account
	When the client requests to register an account, the request will be forwarded by loginapp to dbmgr. If dbmgr is connected to interfaces, dbmgr will forward the request here (KBEngine.onRequestCreateAccount)
	At this time, after receiving this request, the script can communicate with the third-party platform in various ways. You can use the http library of python or use the socket directly. After interacting with the third-party platform, you should
	The result of the interaction is returned to the baseapp layer of the engine, and information can be pushed to the baseapp layer through KBEngine.createAccountResponse.
	
2：Account login
	When the client requests to log in to the account, the request will be forwarded by loginapp to dbmgr. If dbmgr is connected to interfaces, dbmgr will forward the request here (KBEngine.onRequestAccountLogin)
	At this time, after receiving this request, the script can communicate with the third-party platform in various ways. You can use the http library of python or use the socket directly. After interacting with the third-party platform, you should
	The result of the interaction is returned to the baseapp layer of the engine, and information can be pushed to the baseapp layer through KBEngine.accountLoginResponse.
	
3：Recharge billing
	After requesting charging entity.charge () on baseapp, the request will be forwarded by loginapp to dbmgr. If dbmgr is connected to interfaces, dbmgr will forward the request here (KBEngine.onRequestCharge)
	At this time, after receiving this request, the script can communicate with the third-party platform in various ways. You can use the http library of python or use the socket directly. After interacting with the third-party platform, you should
	The result of the interaction is returned to the baseapp layer of the engine. Through KBEngine.chargeResponse, the information can be pushed to the callback given when the entity.charge in the baseapp layer is sent to the onLoseChargeCB interface.
	The Some platforms require the client to request billing directly with the platform. The platform uses a callback server to complete the request. See "Platform Callback".
	
4: Platform callback
	To complete this function, a socket should be created in the script layer,
	And connect the socket to KBEngine (this can prevent the main thread card from blocking), and then listen to the specified port.
	Use KBE's KBEngine.registerReadFileDescriptor () and KBEngine.registerWriteFileDescriptor () to check the API documentation and Poller.py.
"""

g_poller = Poller()

def onInterfaceAppReady():
	"""
	KBEngine method.
	interfaces are ready
	"""
	INFO_MSG('onInterfaceAppReady: bootstrapGroupIndex=%s, bootstrapGlobalIndex=%s' % \
	 (os.getenv("KBE_BOOTIDX_GROUP"), os.getenv("KBE_BOOTIDX_GLOBAL")))

	#KBEngine.addTimer(0.01, 1.0, onTick)
	g_poller.start("localhost", 30040)

def onTick(timerID):
	"""
	"""
	INFO_MSG('onTick()')

	# 测试数据库查询
	KBEngine.executeRawDatabaseCommand("select * from kbe_accountinfos limit 3;", onSqlCallback)
	KBEngine.urlopen("https://www.baidu.com", onHttpCallback)

def onInterfaceAppShutDown():
	"""
	KBEngine method.
	The callback function before the interfaces are closed
	"""
	INFO_MSG('onInterfaceAppShutDown()')
	g_poller.stop()

def onRequestCreateAccount(registerName, password, datas):
	"""
	KBEngine method.
	Request to create an account callback
	@param registerName: Name submitted when requested by the client
	@type  registerName: string
	
	@param password: password
	@type  password: string
	
	@param datas: The data attached to the client request can be forwarded to a third-party platform
	@type  datas: bytes
	"""
	INFO_MSG('onRequestCreateAccount: registerName=%s' % (registerName))
	
	commitName = registerName
	
	# The default account name is the name at the time of submission
	realAccountName = commitName 
	
	# Here, the request can be submitted to a third-party platform through means such as http, and the data returned by the platform can also be placed into datas
	# datas will be called back to the client
	# If you use http access, because the interfaces are single-threaded, synchronous http access is easy to jam the main thread, it is recommended to use
	# KBEngine.urlopen("https://www.baidu.com",onHttpCallback)Asynchronous access. You can also interact with the platform by combining asynchronous sockets (refer to Poller.py).
	
	KBEngine.createAccountResponse(commitName, realAccountName, datas, KBEngine.SERVER_SUCCESS)
	
def onRequestAccountLogin(loginName, password, datas):
	"""
	KBEngine method.
	Request login account callback
	@param loginName: Name submitted when requested by the client
	@type  loginName: string
	
	@param password: password
	@type  password: string
	
	@param datas: The data attached to the client request can be forwarded to a third-party platform
	@type  datas: bytes
	"""
	INFO_MSG('onRequestAccountLogin: registerName=%s' % (loginName))
	
	commitName = loginName
	
	# The default account name is the name at the time of submission
	realAccountName = commitName 
	
	# Here, the request can be submitted to a third-party platform through means such as http, and the data returned by the platform can also be placed into datas
	# datas will be called back to the client
	# If you use http access, because the interfaces are single-threaded, synchronous http access is easy to jam the main thread, it is recommended to use
	# KBEngine.urlopen ("https://www.baidu.com", onHttpCallback) asynchronous access. You can also interact with the platform by combining asynchronous sockets (refer to Poller.py).
	
	# If the return code is KBEngine.SERVER_ERR_LOCAL_PROCESSING, it means that the login is successful, but dbmgr needs to check the account password, and KBEngine.SERVER_SUCCESS does not need to check the password.
	KBEngine.accountLoginResponse(commitName, realAccountName, datas, KBEngine.SERVER_ERR_LOCAL_PROCESSING)
	
def onRequestCharge(ordersID, entityDBID, datas):
	"""
	KBEngine method.
	Request billing callback
	@param ordersID: Order ID
	@type  ordersID: uint64
	
	@param entityDBID: DBID of the entity submitting the order
	@type  entityDBID: uint64
	
	@param datas: The data attached to the client request can be forwarded to a third-party platform
	@type  datas: bytes
	"""
	INFO_MSG('onRequestCharge: entityDBID=%s, entityDBID=%s' % (ordersID, entityDBID))
	
	# Here you can submit the request to a third-party platform through http and other means, and the data returned by the platform can also be placed into datas
	# datas will be called back to the order callback of baseapp, please refer to the API manual charge for details
	# If you use http access, because the interfaces are single-threaded, synchronous http access is easy to jam the main thread, it is recommended to use
	# KBEngine.urlopen ("https://www.baidu.com", onHttpCallback) asynchronous access. You can also interact with the platform by combining asynchronous sockets (refer to Poller.py).
	
	KBEngine.chargeResponse(ordersID, datas, KBEngine.SERVER_SUCCESS)


def onSqlCallback(result, rows, insertid, error):
	DEBUG_MSG('onSqlCallback: result=%s, rows=%s, insertid=%s, error=%s' % (str(result), str(rows), str(insertid), str(error)))

def onHttpCallback(httpcode, data, headers, success, url):
	DEBUG_MSG('onHttpCallback: httpcode=%i, data=%s, headers=%s, success=%s, url=%s' % (httpcode, data, headers, str(success), url))
