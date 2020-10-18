#!/usr/bin/env python
# -*- coding: utf-8 -*-


#========================================
#  Libraries
#========================================
# Libraries (Bokeh)
from bokeh.models.widgets import Butto
import sqlite3, os

#========================================
# Parameters
#========================================
# Widget : DL_BUTTON
WN_RESET = "RESET"
WID_RESET = "RESET"
WPROP_RESET = {}
WPROP_RESET["label"] = "Reset"
WPROP_RESET["button_type"] = "warning"
WPROP_RESET["width"] = 100
WPROP_RESET["height"] = 50


#========================================
# MESSAGES
#========================================
MESSAGES = {
    "Reset_init_start" : ">> Status : Reset : __init__ :  Loading reset button...",
    "Reset_init_error" : ">> Status : Reset : __init__ :  ERROR : Loading reset button failed.",
    "Reset_callback_start" : ">> Status : Reset : callback :  Start reseting.",
    "Reset_callback_error" : ">> Status : Reset : callback :  ERROR : Reseting failed."
}


#========================================
# Reset : bokeh : callback
#========================================
class Save():
	def __init__(self, df):
		try:
			### Checkpoint ###
			print(MESSAGES["Reset_init_start"])
			### Checkpoint ###
			self.df = df
			self.bokeh = Button(
				name = WN_RESET,
				id = WID_RESET,
				label = WPROP_RESET["label"],
				button_type = WPROP_RESET["button_type"],
				width = WPROP_RESET["width"],
				height = WPROP_RESET["height"]
			)
			self.bokeh.on_click(self.callback)
		except:
			### Checkpoint ###
			print(MESSAGES["Reset_init_error"])
			### Checkpoint ###
			self.bokeh = []
			
	def callback(self):
		try:
			conn = sqlite3.connect("csv.sqlite")
			c = conn.cursor()
			file_name="test.csv"
			self.df.df.to_sql(file_name, conn, if_exists='append', index=None)
			conn.close()
			### Checkpoint ###
			print(MESSAGES["Reset_callback_start"])
			### Checkpoint ###
		except:
			### Checkpoint ###
			print(MESSAGES["Reset_callback_error"])
			### Checkpoint ###
			#main()
