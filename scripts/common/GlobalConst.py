# -*- coding: utf-8 -*-

"""
"""
GC_OK								= 0x000

# Skill related
GC_SKILL_MP_NOT_ENGOUH				= 0x001		# Insufficient mana
GC_SKILL_ENTITY_DEAD				= 0x002		# Entity is dead

# Maps corresponding to different demos
g_demoMaps = {
	b'kbengine_ue4_demo' : 7,
	b'kbengine_cocos2d_js_demo' : 6,
	b'kbengine_unity3d_demo' : 3,
	b'kbengine_ogre_demo' : 2,
	b'' : 1,
}