# -*- coding: utf-8 -*-
import KBEngine
import GlobalConst
import d_spaces
import d_avatar_inittab
from KBEDebug import * 

class Teleport:
	def __init__(self):
		# If the login is a copy, the login is placed on the main scene anyway
		# Because the copy needs to be opened with the key, all copies are created using the entity SpaceDuplicate
		# Therefore, we only need to simply determine whether the script type of the scene in the configuration corresponding to the current spaceUType contains "Duplicate"
		# You can tell whether it is in a copy
		spacedatas = d_spaces.datas[self.cellData["spaceUType"]]
		avatar_inittab = d_avatar_inittab.datas[self.roleType]

		if "Duplicate" in spacedatas["entityType"]:
			self.cellData["spaceUType"] = avatar_inittab["spaceUType"]
			self.cellData["direction"] = (0, 0, avatar_inittab["spawnYaw"])
			self.cellData["position"] = avatar_inittab["spawnPos"]

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onClientEnabled(self):
		"""
		KBEngine method.
		The entity is officially activated for use. At this time, the entity has established the corresponding entity of the client, and you can create it here.
		cell part.
		"""
		if self.cell is not None:
			return 

		# Prevent the use of the same number to log in to different demos, which can't find the matching map, so that resources cannot be loaded and the game cannot be entered
		# Check here, if you find something wrong, force synchronization to the matching map
		# Ignore robot inspection
		if hasattr(self, "cellData") and self.getClientType() != 6:
			# If the character jumps to other scenes belonging to a certain demo, then it is not forced to return to the main scene of birth
			if self.cellData["spaceUType"] in GlobalConst.g_demoMaps.values():
				spaceUType = GlobalConst.g_demoMaps.get(self.getClientDatas()[0], 1)

				if self.cellData["spaceUType"] != spaceUType:
					spacedatas = d_spaces.datas[spaceUType]
					self.spaceUTypeB = spaceUType
					self.cellData["spaceUType"] = spaceUType
					self.cellData["position"] = spacedatas.get("spawnPos", (0,0,0))
		
		KBEngine.globalData["Spaces"].loginToSpace(self, self.spaceUTypeB, {})



