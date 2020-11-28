# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

def countPlayers():
	"""
	KBEngine.addWatcher("players", "UINT32", countPlayers)
	The above code adds this function to the monitor, and the function return value can be monitored in real time from tools such as GUIConsole
	"""
	i = 0
	for e in KBEngine.entities.values():
		if e.__class__.__name__ == "Avatar":
			i += 1

	return i
	
def countSpaces():
	"""
	KBEngine.addWatcher("players", "UINT32", countPlayers)
	The above code adds this function to the monitor, and the function return value can be monitored in real time from tools such as GUIConsole
	"""
	i = 0
	for e in KBEngine.entities.values():
		if e.__class__.__name__ == "Spaces":
			i += 1

	return i


def setup():
	KBEngine.addWatcher("players", "UINT32", countPlayers)
	KBEngine.addWatcher("spaces", "UINT32", countSpaces)