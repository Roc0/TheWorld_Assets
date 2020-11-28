# -*- coding: utf-8 -*-
import KBEngine
import GlobalConst
from KBEDebug import * 


# Server timer definition
TIMER_TYPE_BUFF_TICK								= 1 # buff's tick
TIMER_TYPE_SPACE_SPAWN_TICK							= 2 # space born monster
TIMER_TYPE_CREATE_SPACES							= 3 # Create space
TIMER_TYPE_DESTROY									= 4 # Delayed destruction of entity
TIMER_TYPE_HEARDBEAT								= 5	# Heartbeat
TIMER_TYPE_FIGTH_WATI_INPUT_TIMEOUT					= 6	# Waiting for user input timeout in battle round
TIMER_TYPE_SPAWN									= 7	# Birth point
TIMER_TYPE_DESTROY									= 8	# entity destruction