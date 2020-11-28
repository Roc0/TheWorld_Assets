# -*- coding: utf-8 -*-
import KBEngine
import random
import time
import d_spaces
import GlobalConst
from AVATAR_INFOS import TAvatarInfos
from AVATAR_INFOS import TAvatarInfosList
from AVATAR_DATA import TAvatarData
from KBEDebug import *
import d_avatar_inittab

class Account(KBEngine.Proxy):
	"""
	Account entity
	After the client logs in to the server, the server will automatically create this entity and interact with the client through this entity
	"""
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		self.activeAvatar = None
		self.relogin = time.time()
	
	def reqAvatarList(self):
		"""
		exposed.
		The client requests to query the role list
		"""
		DEBUG_MSG("Account[%i].reqAvatarList: size=%i." % (self.id, len(self.characters)))
		self.client.onReqAvatarList(self.characters)
				
	def reqCreateAvatar(self, roleType, name):
		"""
		exposed.
		The client requests to create a role
		"""
		avatarinfo = TAvatarInfos()
		avatarinfo.extend([0, "", 0, 0, TAvatarData().createFromDict({"param1" : 0, "param2" :b''})])
			
		"""
		if name in all_avatar_names:
			retcode = 2
			self.client.onCreateAvatarResult(retcode, avatarinfo)
			return
		"""
		
		if len(self.characters) >= 3:
			DEBUG_MSG("Account[%i].reqCreateAvatar:%s. character=%s.\n" % (self.id, name, self.characters))
			self.client.onCreateAvatarResult(3, avatarinfo)
			return
		
		""" Give birth point based on front-end category
		Reference: http://www.kbengine.org/docs/programming/clientsdkprogramming.html, client types
		UNKNOWN_CLIENT_COMPONENT_TYPE	= 0,
		CLIENT_TYPE_MOBILE				= 1,	// Mobile phone
		CLIENT_TYPE_WIN					= 2,	// pc, generally exe client
		CLIENT_TYPE_LINUX				= 3		// Linux Application program
		CLIENT_TYPE_MAC					= 4		// Mac Application program
		CLIENT_TYPE_BROWSER				= 5,	// web application, html5, flash
		CLIENT_TYPE_BOTS				= 6,	// bots
		CLIENT_TYPE_MINI				= 7,	// Mini client
		"""
		spaceUType = GlobalConst.g_demoMaps.get(self.getClientDatas()[0], 1)
		
		# If it is a robot landing, randomly throw it into a scene
		if self.getClientType() == 6:
			while True:
				spaceName = random.choice(list(GlobalConst.g_demoMaps.keys()))
				if len(spaceName) > 0:
					spaceUType = GlobalConst.g_demoMaps[spaceName]
					break

		spaceData = d_spaces.datas.get(spaceUType)
		
		props = {
			"name"				: name,
			"roleType"			: roleType,
			"level"				: 1,
			"spaceUType"		: spaceUType,
			"direction"			: (0, 0, d_avatar_inittab.datas[roleType]["spawnYaw"]),
			"position"			: spaceData.get("spawnPos", (0,0,0)),

			"component1"		: { "bb" : 1231, "state" : 456},
			"component3"		: { "state" : 888 },
			}
			
		avatar = KBEngine.createEntityLocally('Avatar', props)
		if avatar:
			avatar.writeToDB(self._onAvatarSaved)
		
		DEBUG_MSG("Account[%i].reqCreateAvatar:%s. spaceUType=%i, spawnPos=%s.\n" % (self.id, name, avatar.cellData["spaceUType"], spaceData.get("spawnPos", (0,0,0))))
		
	def reqRemoveAvatar(self, name):
		"""
		exposed.
		Client request to delete a role
		"""
		DEBUG_MSG("Account[%i].reqRemoveAvatar: %s" % (self.id, name))
		found = 0
		for key, info in self.characters.items():
			if info[1] == name:
				del self.characters[key]
				found = key
				break
		
		self.client.onRemoveAvatar(found)
		
	def reqRemoveAvatarDBID(self, dbid):
		"""
		exposed.
		Client request to delete a role
		"""
		DEBUG_MSG("Account[%i].reqRemoveAvatar: %s" % (self.id, dbid))
		found = 0
		
		if dbid in self.characters:
			del self.characters[dbid]
			found = dbid

		self.client.onRemoveAvatar(found)

	def selectAvatarGame(self, dbid):
		"""
		exposed.
		The client selects a character to play
		"""
		DEBUG_MSG("Account[%i].selectAvatarGame:%i. self.activeAvatar=%s" % (self.id, dbid, self.activeAvatar))
		# Note: The entity using giveClientTo must be the entity on the current baseapp
		if self.activeAvatar is None:
			if dbid in self.characters:
				self.lastSelCharacter = dbid
				# Because the role needs to be loaded from the database, it is an asynchronous process, and the __onAvatarCreated interface will be called if the loading is successful or fails
				# After the role is created, account will call giveClientTo to switch the client control (which can be understood as the binding of the network connection to an entity) to Avatar,
				# After that, various input and output of the client are proxied through the Avatar on the server, and any proxy entity will call onClientEnabled to obtain control
				# Avatar inherits Teleport, and Teleport.onClientEnabled will create players in specific scenarios
				KBEngine.createEntityFromDBID("Avatar", dbid, self.__onAvatarCreated)
			else:
				ERROR_MSG("Account[%i]::selectAvatarGame: not found dbid(%i)" % (self.id, dbid))
		else:
			self.giveClientTo(self.activeAvatar)
		
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onClientEnabled(self):
		"""
		KBEngine method.
		The entity is officially activated and ready for use. At this time, the entity has established the corresponding entity of the client, and you can create it here.
		cell part.
		"""
		INFO_MSG("Account[%i]::onClientEnabled:entities enable. entityCall:%s, clientType(%i), clientDatas=(%s), hasAvatar=%s, accountName=%s" % \
			(self.id, self.client, self.getClientType(), self.getClientDatas(), self.activeAvatar, self.__ACCOUNT_NAME__))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		When the client login fails, it will call back here
		"""
		INFO_MSG("Account[%i]::onLogOnAttempt: ip=%s, port=%i, selfclient=%s" % (self.id, ip, port, self.client))
		"""
		if self.activeAvatar != None:
			return KBEngine.LOG_ON_REJECT

		if ip == self.lastClientIpAddr and password == self.password:
			return KBEngine.LOG_ON_ACCEPT
		else:
			return KBEngine.LOG_ON_REJECT
		"""
		
		# If an online account is logged in by a client and onLogOnAttempt returns permission
		# Then it will kick off the previous client connection
		# Then self.activeAvatar may not be None at this time, the normal process is to destroy the role and wait for new clients to re-select the role to enter
		if self.activeAvatar:
			if self.activeAvatar.client is not None:
				self.activeAvatar.giveClientTo(self)

			self.relogin = time.time()
			self.activeAvatar.destroySelf()
			self.activeAvatar = None
			
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		The client's corresponding entity has been destroyed
		"""
		if self.activeAvatar:
			self.activeAvatar.accountEntity = None
			self.activeAvatar = None

		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()		
		
	def onDestroy(self):
		"""
		KBEngine method.
		entity destruction
		"""
		DEBUG_MSG("Account::onDestroy: %i." % self.id)
		
		if self.activeAvatar:
			self.activeAvatar.accountEntity = None

			try:
				self.activeAvatar.destroySelf()
			except:
				pass
				
			self.activeAvatar = None
			
	def __onAvatarCreated(self, baseRef, dbid, wasActive):
		"""
		Called when the selected character enters the game
		"""
		if wasActive:
			ERROR_MSG("Account::__onAvatarCreated:(%i): this character is in world now!" % (self.id))
			return
		if baseRef is None:
			ERROR_MSG("Account::__onAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
			return
			
		avatar = KBEngine.entities.get(baseRef.id)
		if avatar is None:
			ERROR_MSG("Account::__onAvatarCreated:(%i): when character was created, it died as well!" % (self.id))
			return
		
		if self.isDestroyed:
			ERROR_MSG("Account::__onAvatarCreated:(%i): i dead, will the destroy of Avatar!" % (self.id))
			avatar.destroy()
			return
			
		info = self.characters[dbid]
		avatar.cellData["modelID"] = d_avatar_inittab.datas[info[2]]["modelID"]
		avatar.cellData["modelScale"] = d_avatar_inittab.datas[info[2]]["modelScale"]
		avatar.cellData["moveSpeed"] = d_avatar_inittab.datas[info[2]]["moveSpeed"]
		avatar.accountEntity = self
		self.activeAvatar = avatar
		self.giveClientTo(avatar)
		
	def _onAvatarSaved(self, success, avatar):
		"""
		New role write database callback
		"""
		INFO_MSG('Account::_onAvatarSaved:(%i) create avatar state: %i, %s, %i' % (self.id, success, avatar.cellData["name"], avatar.databaseID))
		
		# If the account has been destroyed at this time, the role can no longer be recorded, then we clear the role
		if self.isDestroyed:
			if avatar:
				avatar.destroy(True)
				
			return
			
		avatarinfo = TAvatarInfos()
		avatarinfo.extend([0, "", 0, 0, TAvatarData().createFromDict({"param1" : 0, "param2" :b''})])

		if success:
			info = TAvatarInfos()
			info.extend([avatar.databaseID, avatar.cellData["name"], avatar.roleType, 1, TAvatarData().createFromDict({"param1" : 1, "param2" :b'1'})])
			self.characters[avatar.databaseID] = info
			avatarinfo[0] = avatar.databaseID
			avatarinfo[1] = avatar.cellData["name"]
			avatarinfo[2] = avatar.roleType
			avatarinfo[3] = 1
			self.writeToDB()
		else:
			avatarinfo[1] = "Creation failed"

		avatar.destroy()
		
		if self.client:
			self.client.onCreateAvatarResult(0, avatarinfo)
