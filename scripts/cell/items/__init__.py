# -*- coding: utf-8 -*-
#
"""
"""
import KBEngine
import copy
import scdefine
import scutils
import skills
import ScriptMaps
from KBEDebug import *
from Item import Item
from Equip import Equip
from Weapon import Weapon
from d_items import datas as d_items

def onInit():
	pass

def checkItemNo(itemNO):
	return itemNO in d_items

def noAlias2ItemNo(aid):
	return g_noAlias2ItemNo.get(aid, 0)

def itemNo2NoAlias(sid):
	return g_itemNo2NoAlias.get(sid, 0)

def getItemData(itemNO):
	"""
	Obtain the configuration data of the item
	"""
	return d_items.get(itemNO, {})

def getItemClass(itemNO):
	"""
	Obtain the configuration data of the item
	"""
	return d_items[itemNO]["script"]

def createItem(itemNO, amount = 1, owner = None):
	"""
	Create item
	"""
	INFO_MSG("%i created. amount=%i" % (itemNO, amount))

	stackMax = getItemData(itemNO).get("overlayMax", 1)
	itemList = []
	while amount > 0:
		itemAmount = (amount < stackMax) and amount or stackMax
		item = getItemClass(itemNO)(itemNO, scutils.newUID(), itemAmount)
		item.onCreate(owner)
		itemList.append(item)
		amount -= itemAmount

	return itemList

def createItemByItem(item, amount, owner = None):
	"""
	Create a new item based on a known item
	"""
	newItem = copy.deepcopy(item)
	newItem.setUUID(scutils.newUID())
	newItem.setAmount(amount)
	INFO_MSG("new item created. new item uuid=%i, src item uuid=%i" % (newItem.getUUID(), item.getUUID()))
	return newItem