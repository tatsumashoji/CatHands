#!/usr/bin/env python
# -*- coding: utf-8 -*-


#========================================
#  Libraries
#========================================
import pandas as pd
# Libraries (Bokeh)
from bokeh.models.widgets import Button, TextInput

#========================================
# Parameters
#========================================
# URL : download.js
URL_DOWNLOAD_JS = "app/static/download.js"
# Widget : DL_BUTTON
WN_DL_BUTTON = "DL_BUTTON"
WID_DL_BUTTON = "DL_BUTTON"
WPROP_DL_BUTTON = {}
WPROP_DL_BUTTON["label"] = "Download"
WPROP_DL_BUTTON["button_type"] = "success"
WPROP_DL_BUTTON["width"] = 100
WPROP_DL_BUTTON["height"] = 50
# Widget : DL_EXEC
WN_DL_EXEC = "DL_EXEC"
WID_DL_EXEC = "DL_EXEC"
WPROP_DL_EXEC = {}
WPROP_DL_EXEC["value"] = "0"
WPROP_DL_EXEC["width"] = 100
WPROP_DL_EXEC["height"] = 50
WPROP_DL_EXEC["visible"] = False


#========================================
# MESSAGES
#========================================
MESSAGES = {
    "Download_init_start" : ">> Status : Download : __init__ :  Loading download button...",
    "Download_init_error" : ">> Status : Download : __init__ :  ERROR : Loading download button failed.",
    "Download_callback_start" : ">> Status : Download : callback :  Start downloading...",
    "Download_callback_error" : ">> Status : Download : callback :  ERROR : Download failed."
}


#========================================
# Download : bokeh_btn, bokeh_exec : callback
#========================================
class Download():
	def __init__(self, df, uploader):
		try:
			### Checkpoint ###
			print(MESSAGES["Download_init_start"])
			### Checkpoint ###
			self.df = df
			self.uploader = uploader
			self.bokeh_btn = Button(
				name = WN_DL_BUTTON,
				id = WID_DL_BUTTON,
				label = WPROP_DL_BUTTON["label"],
				button_type = WPROP_DL_BUTTON["button_type"],
				width = WPROP_DL_BUTTON["width"],
				height = WPROP_DL_BUTTON["height"]
			)
			self.bokeh_btn.on_click(self.callback)
			self.bokeh_exec = TextInput(
				name = WN_DL_EXEC,
				id = WID_DL_EXEC,
				value = WPROP_DL_EXEC["value"],
				width = WPROP_DL_EXEC["width"],
				height = WPROP_DL_EXEC["height"],
				visible = WPROP_DL_EXEC["visible"]
			)
		except:
			### Checkpoint ###
			print(MESSAGES["Download_init_error"])
			### Checkpoint ###
			self.bokeh = []
			self.bokeh_exec = []
			
	def callback(self):
		try:
			### Checkpoint ###
			print(MESSAGES["Download_callback_start"])
			### Checkpoint ###
			self.bokeh_exec.js_on_change(
				'value',
				CustomJS(
					args = dict(
						source = self.df.df.iloc[self.df.subrow_Manual,:].to_csv(),
						fname = self.uploader.filename
					),
					code = open(URL_DOWNLOAD_JS).read()
				)
			)
			self.bokeh_exec.value += '1'
			self.bokeh_exec._property_values.pop('js_property_callbacks')
		except:
			### Checkpoint ###
			print(MESSAGES["Download_callback_error"])
			### Checkpoint ###
			#main()
