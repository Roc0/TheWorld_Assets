# -*- coding: utf-8 -*-
import KBEngine
import json
from KBEDebug import * 
from interfaces.CombatPropertys import CombatPropertys

class Combat(CombatPropertys):
	def __init__(self):
		CombatPropertys.__init__(self)

	def recvDamage(self, attackerID, skillID, damageType, damage):
		"""
		defined.
		"""
		DEBUG_MSG("%s::recvDamage: %i attackerID=%i, skillID=%i, damageType=%i, damage=%i" % \
			(self.getScriptName(), self.id, attackerID, skillID, damageType, damage))
		
		# Inform the presentation layer to change performance
		KBEngine.fireEvent("recvDamage", json.dumps((self.id, attackerID, skillID, damageType, damage, self.HP)))
		

