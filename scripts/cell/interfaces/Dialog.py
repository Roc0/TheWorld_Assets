# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 
import dialogmgr

class Dialog:
	"""
	Dialogue module with NPC, client drives dialogue protocol by calling dialog
	"""
	def __init__(self):
		pass

	#--------------------------------------------------------------------------------------------
	#                              defined
	#--------------------------------------------------------------------------------------------
	def dialog(self, srcEntityID, targetID, dialogID):
		"""
		exposed.
		Cast a skill on a target entity
		"""
		if srcEntityID != self.id:
			return
			
		if not KBEngine.entities.has_key(targetID):
			DEBUG_MSG("Dialog::dialog: %i not found targetID:%i" % (self.id, dialogID))
			return
			
		dialogmgr.onGossip(dialogID, self, KBEngine.entities[targetID])


