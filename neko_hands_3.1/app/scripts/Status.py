#!/usr/bin/env python
# -*- coding: utf-8 -*-


#========================================
#  Libraries
#========================================
# Libraries (Bokeh)
from bokeh.models import Panel, Div, Tabs


#========================================
# Parameters
#========================================
# Widget : ACCOUNT_NAME
WN_ACCOUNT_NAME = "ACCOUNT_NAME"
WID_ACCOUNT_NAME = "ACCOUNT_NAME"
WPROP_ACCOUNT_NAME = {}
WPROP_ACCOUNT_NAME["text"] = "Name : %s"
WPROP_ACCOUNT_NAME["width"] = 200
# Widget : ACCOUNT_PLAN
WN_ACCOUNT_PLAN = "ACCOUNT_PLAN"
WID_ACCOUNT_PLAN = "ACCOUNT_PLAN"
WPROP_ACCOUNT_PLAN = {}
WPROP_ACCOUNT_PLAN["text"] = "Plan : %s (<a href='%s'>Change</a>)"
WPROP_ACCOUNT_PLAN["width"] = 200
# Widget : TABS
WN_TABS = "tabs"
WID_TABS = "tabs"


#========================================
# MESSAGES
#========================================
MESSAGES = {
    "Status_init_start" : ">> Status : Status : __init__ : Loading account information...",
    "Status_init_error" : ">> Status : Status : __init__ : ERROR : Loading account information failed."
}


#========================================
# Status : bokeh_name, bokeh_plan
#========================================
class Status():
	def __init__(self):
		try:
			### Checkpoint ###
			print(MESSAGES["Status_init_start"])
			### Checkpoint ###
			self.bokeh_name = Div(
				name=WN_ACCOUNT_NAME,
				id=WID_ACCOUNT_NAME,
				text=WPROP_ACCOUNT_NAME["text"] % ("Guest"),
				width=WPROP_ACCOUNT_NAME["width"]
			)
			self.bokeh_plan = Div(
				name=WN_ACCOUNT_PLAN,
				id=WID_ACCOUNT_PLAN,
				text=WPROP_ACCOUNT_PLAN["text"] % ("Standard", "_blank"),
				width=WPROP_ACCOUNT_PLAN["width"]
			)
		except:
			### Checkpoint ###
			print(MESSAGES["Status_init_error"])
			### Checkpoint ###
			self.bokeh_name = []
			self.bokeh_plan = []
			

#========================================
# Page : panels, tabs, pther_comps : add_panel(), define_tab(), add_other_comps()
#========================================
class Page():
	def __init__(self):
		self.panels = {}
		self.tabs = Tabs(
			name=WN_TABS,
			id=WID_TABS,
			tabs = list(self.panels.values()),
			active=0
		)
		self.other_comps = []
		
	def add_panel(self, panel, name):
		self.panels[name] = panel
		
	def define_tab(self):
		self.tabs.tabs = list(self.panels.values())
		
	def add_other_comps(self, comp):
		self.other_comps.append(comp)