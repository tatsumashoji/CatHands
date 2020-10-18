#!/usr/bin/env python
# -*- coding: utf-8 -*-


#========================================
#  Libraries
#========================================
import os, glob
import pandas as pd
# Libraries (Bokeh)
from bokeh.io import curdoc
from bokeh.models.widgets import FileInput
from bokeh.models import Panel, Div, Button
from bokeh.layouts import layout
# Modules
from scripts.DataFrame import DataFrame
from scripts.Graphs import Graphs
from scripts.PageStatus import PageStatus, LinkStatus
from scripts.Decomposition import Decomposition
# database
import sqlite3

#========================================
# Parameters
#========================================
# Widget : UPLOADER_HEADER
WN_UPLOADER_HEADER = "UPLOADER_HEADER"
WID_UPLOADER_HEADER = "UPLOADER_HEADER"
WPROP_UPLOADER_HEADER = {}
WPROP_UPLOADER_HEADER["width"] = 1000
WPROP_UPLOADER_HEADER["text"] = '''
                <header class="post-header">
                    <h1 class="post-title">Drag & Drop</h1>
                    <p class="post-meta">
                        <span class="post-category post-category-design">CSV</span>
                        <span class="post-category post-category-design">TSV</span>
                    </p>
                </header>
'''
# Widget : UPLOADER
WN_UPLOADER = "UPLOADER"
WID_UPLOADER = "UPLOADER"
WPROP_UPLOADER = {}
WPROP_UPLOADER["sizing_mode"] = "stretch_both"
WPROP_UPLOADER["height"] = 300
# Widget : FILES_PANEL
WN_FILES_PANEL = "FILES_PANEL"
WID_FILES_PANEL = "FILES_PANEL"
WPROP_FILES_PANEL = {}
WPROP_FILES_PANEL["title"] = "Upload"
# Widget : SELECT_PANEL
WN_SELECT_PANEL = "SELECT_PANEL"
WID_SELECT_PANEL = "SELECT_PANEL"
WPROP_SELECT_PANEL = {}
WPROP_SELECT_PANEL["title"] = "Select"
# Widget : DECOMP_PANEL
WN_DECOMP_PANEL = "DECOMP_PANEL"
WID_DECOMP_PANEL = "DECOMP_PANEL"
WPROP_DECOMP_PANEL = {}
WPROP_DECOMP_PANEL["title"] = "Decomposition"
# Widget : TABS
WID_TABS = "tabs"
# Database
PATH = "app/database/"
DB_SUFFIX = ".sqlite"
# Widget : DECOMP_PANEL
WN_LOADFILE = "LOADFILE"
WID_LOADFILE = "LOADFILE"
WPROP_LOADFILE = {}
WPROP_LOADFILE["width"] = 1000
WPROP_LOADFILE["height"] = 400
WPROP_LOADFILE["columns"] = []
# Widget : LOADFILE_HEADER
WN_LOADFILE_HEADER = "LOADFILE_HEADER"
WID_LOADFILE_HEADER = "LOADFILE_HEADER"
WPROP_LOADFILE_HEADER = {}
WPROP_LOADFILE_HEADER["width"] = 1000
WPROP_LOADFILE_HEADER["text"] = '''
                <header class="post-header">
                    <h1 class="post-title">Load Files</h1>
                </header>
'''
# Widget : FILENAME
WN_FILENAME = "FILENAME"
WID_FILENAME = "FILENAME"
WPROP_FILENAME = {}
WPROP_FILENAME["text"] = "Target : %s"
WPROP_FILENAME["default_text"] = " No Files Selected. "
WPROP_FILENAME["width"] = 200
# Widget : COLUMNS
WN_COLUMNS = "COLUMNS"
WID_COLUMNS = "COLUMNS"
WPROP_COLUMNS = {}
WPROP_COLUMNS["text"] = "Columns : %s"
WPROP_COLUMNS["default_text"] = " --- "
WPROP_COLUMNS["width"] = 200
# Widget : RECORDS
WN_RECORDS = "RECORDS"
WID_RECORDS = "RECORDS"
WPROP_RECORDS = {}
WPROP_RECORDS["text"] = "Records : %s"
WPROP_RECORDS["default_text"] = " --- "
WPROP_RECORDS["width"] = 200
# Widget : SELECTED_RECORDS
WN_SELECTED_RECORDS = "SELECTED_RECORDS"
WID_SELECTED_RECORDS = "SELECTED_RECORDS"
WPROP_SELECTED_RECORDS = {}
WPROP_SELECTED_RECORDS["text"] = "Selected Records : %s"
WPROP_SELECTED_RECORDS["default_text"] = " --- "
WPROP_SELECTED_RECORDS["width"] = 200

#========================================
# MESSAGES
#========================================
MESSAGES = {
    "UploaderHeader_init_start" : ">> Status : UploaderHeader : __init__ ",
    "UploaderHeader_init_error" : ">> Status : UploaderHeader : __init__ : ############## ERROR ##############",
    "Uploader_init_start" : ">> Status : Uploader : __init__ ",
    "Uploader_init_error" : ">> Status : Uploader : __init__ : ############## ERROR ##############",
    "Uploader_callback_start" : ">> Status : Uploader : callback : 1",
    "Uploader_callback_checkpoint1" : ">> Status : Uploader : callback : 2",
    "Uploader_callback_error" : ">> Status : Uploader : callback : ############## ERROR ##############",
    "LoadFileHeader_init_start" : ">> Status : LoadFileHeader : __init__ ",
    "LoadFileHeader_init_error" : ">> Status : LoadFileHeader : __init__ : ############## ERROR ##############",
    "LoadFile_init_start" : ">> Status : LoadFile : __init__ ",
    "LoadFile_init_error" : ">> Status : LoadFile : __init__ : ############## ERROR ##############"
}


#========================================
# UploaderHeader : bokeh
#========================================
class UploaderHeader():
	def __init__(self):
		try:
			### Checkpoint ###
			print(MESSAGES["UploaderHeader_init_start"])
			### Checkpoint ###
			self.bokeh = Div(
				name=WN_UPLOADER_HEADER,
				id=WID_UPLOADER_HEADER,
				text=WPROP_UPLOADER_HEADER["text"],
				width=WPROP_UPLOADER_HEADER["width"]
			)
		except:
			### Checkpoint ###
			print(MESSAGES["UploaderHeader_init_error"])
			### Checkpoint ###
			self.bokeh = []
			
#========================================
# Uploader : bokeh : callback
#========================================
class Uploader():
	def __init__(self, df, page, uploader_header):
		try:
			### Checkpoint ###
			print(MESSAGES["Uploader_init_start"])
			### Checkpoint ###
			self.df = df
			self.page = page
			self.uploader_header = uploader_header
			self.bokeh = FileInput(
				name=WN_UPLOADER,
				id=WID_UPLOADER,
				sizing_mode=WPROP_UPLOADER["sizing_mode"],
				height=WPROP_UPLOADER["height"]
			)
			self.bokeh.on_change('value', self.callback)
		except:
			### Checkpoint ###
			print(MESSAGES["Uploader_init_error"])
			### Checkpoint ###
			self.bokeh = []
	
	def callback(self, attr, old, new, uid="test"):
	    try:
	    	### Checkpoint ###
	    	print(MESSAGES["Uploader_callback_start"])
	    	### Checkpoint ###
	    	
    		self.df.reload_df(self)
    		loadfile_header = LoadFileHeader()
    		loadfile = LoadFile(self.df, self.page)
    		
    		page_status = PageStatus(self.df, self)
    		link_status = LinkStatus()
    		graphs = Graphs(self.df, page_status, link_status)

    		files_panel = Panel(
    			name=WN_FILES_PANEL,
    			id=WID_FILES_PANEL,
    			child=layout([[self.uploader_header.bokeh]]+[[self.bokeh]]+[[loadfile_header.bokeh]]+loadfile.bokeh_user_file_lists),
    			title=WPROP_FILES_PANEL["title"]
    		)
    		select_panel = Panel(
    			name=WN_SELECT_PANEL,
    			id=WID_SELECT_PANEL,
    			child=layout([[page_status.bokeh, link_status.bokeh]] + graphs.bokeh),
    			title=WPROP_SELECT_PANEL["title"]
    		)
    		decomp = Decomposition(self)
    		decomp_panel = decomp.bokeh
    		### Checkpoint ###
    		print(MESSAGES["Uploader_callback_checkpoint1"])
    		### Checkpoint ###
    		for i in range(len(curdoc().roots[0]._property_values[WID_TABS])):
    			if curdoc().roots[0]._property_values[WID_TABS][i].id == WID_FILES_PANEL:
    				curdoc().roots[0]._property_values[WID_TABS].pop(i)
    				curdoc().roots[0]._property_values[WID_TABS].append(files_panel)
    				break		
    		for i in range(len(curdoc().roots[0]._property_values[WID_TABS])):
    			if curdoc().roots[0]._property_values[WID_TABS][i].id == WID_SELECT_PANEL:
    				curdoc().roots[0]._property_values[WID_TABS].pop(i)
    				curdoc().roots[0]._property_values[WID_TABS].append(select_panel)                
    				break			
    		for i in range(len(curdoc().roots[0]._property_values[WID_TABS])):
    			if curdoc().roots[0]._property_values[WID_TABS][i].id == WID_DECOMP_PANEL:
    				curdoc().roots[0]._property_values[WID_TABS].pop(i)
    				curdoc().roots[0]._property_values[WID_TABS].append(decomp_panel)                
    				break			
    		self.page.tabs.active=1
    		
    		# database
    		conn = sqlite3.connect(PATH + uid + ".sqlite")
    		c = conn.cursor()
    		try:
	    		self.df.df.to_sql(self.bokeh.filename, conn, if_exists="fail", index=None)
	    	except:
	    		print("File already exists.")
    		conn.commit()
    		conn.close()
    		
	    except:
    		### Checkpoint ###
    		print(MESSAGES["Uploader_callback_error"])
    		### Checkpoint ###
    		#main()


#========================================
# LoadFileHeader : bokeh
#========================================
class LoadFileHeader():
	def __init__(self):
		try:
			### Checkpoint ###
			print(MESSAGES["LoadFileHeader_init_start"])
			### Checkpoint ###
			self.bokeh = Div(
				name=WN_LOADFILE_HEADER,
				id=WID_LOADFILE_HEADER,
				text=WPROP_LOADFILE_HEADER["text"],
				width=WPROP_LOADFILE_HEADER["width"]
			)
		except:
			### Checkpoint ###
			print(MESSAGES["LoadFileHeader_init_error"])
			### Checkpoint ###
			self.bokeh = []


#========================================
# LoadFile : bokeh
#========================================
class LoadFile():
	def __init__(self, df, uploader, uid="test"):
		try:
			### Checkpoint ###
			print(MESSAGES["LoadFile_init_start"])
			### Checkpoint ###
			self.df = df
			self.uploader = uploader
			self.uid = uid
			try:
				conn = sqlite3.connect(PATH + self.uid + ".sqlite")
				c = conn.cursor()
				self.bokeh_user_file_lists = []
				for a in c.execute("select name from sqlite_master where type='table'"):
					self.bokeh_user_file_lists.append(
						Button(
							id=a[0],
							label=a[0],
							button_type = "success",
							width=500
						)
					)
					self.bokeh_user_file_lists[-1].on_click(self.callback)
			except:
				pass
				
		except:
			### Checkpoint ###
			print(MESSAGES["LoadFile_init_error"])
			### Checkpoint ###
			self.bokeh = []


	def callback(self, event):
		try:
			### Checkpoint ###
			#print(MESSAGES["Fileload_callback_start"])
			### Checkpoint ###
			
			filename = event._model_id

			db_name = PATH + self.uid + ".sqlite"
						
			with sqlite3.connect(db_name) as conn:
				sql = "select * from '" + filename + "'"
				df = pd.read_sql_query(sql, conn)
				
			conn.close()
			
			self.df.df = df
			self.df.dtypes = self.df.df.apply(self.df.get_dtypes) # dtypes
			self.df.subcol = [self.df.df.columns.get_loc(x) for x in self.df.df.columns] #sub_col
			self.df.subrow_Decomposition = self.df.df.index.tolist() # subrow_Dec
			self.df.subrow_Manual = self.df.df.index.tolist() # subrow_Dis
			self.df.updateStatus = []
			self.df.bokeh_filename.text = WPROP_FILENAME["text"] % (filename)
			self.df.bokeh_columns.text = WPROP_COLUMNS["text"] % (str(len(self.df.df.columns)))
			self.df.bokeh_records.text = WPROP_RECORDS["text"] % (str(len(self.df.df)))
			self.df.bokeh_selected_records.text = WPROP_SELECTED_RECORDS["text"] % (str(len(self.df.subrow_Manual)))
			
			loadfile_header = LoadFileHeader()
			page_status = PageStatus(self.df, self.uploader)
			
			link_status = LinkStatus()
			
			graphs = Graphs(self.df, page_status, link_status)
			
			files_panel = Panel(
				name=WN_FILES_PANEL,
				id=WID_FILES_PANEL,
				child=layout([[self.uploader.uploader_header.bokeh]]+[[self.uploader.bokeh]]+[[loadfile_header.bokeh]]+self.bokeh_user_file_lists),
				title=WPROP_FILES_PANEL["title"]
			)
						
			select_panel = Panel(
				name=WN_SELECT_PANEL,
				id=WID_SELECT_PANEL,
				child=layout([[page_status.bokeh, link_status.bokeh]] + graphs.bokeh),
				title=WPROP_SELECT_PANEL["title"]
			)
			

			decomp = Decomposition(self.uploader)
			decomp_panel = decomp.bokeh
			
			### Checkpoint ###
			#print(MESSAGES["Uploader_callback_checkpoint1"])
			### Checkpoint ###
			for i in range(len(curdoc().roots[0]._property_values[WID_TABS])):
				if curdoc().roots[0]._property_values[WID_TABS][i].id == WID_FILES_PANEL:
					curdoc().roots[0]._property_values[WID_TABS].pop(i)
					curdoc().roots[0]._property_values[WID_TABS].append(files_panel)
					break		
			for i in range(len(curdoc().roots[0]._property_values[WID_TABS])):
				if curdoc().roots[0]._property_values[WID_TABS][i].id == WID_SELECT_PANEL:
					curdoc().roots[0]._property_values[WID_TABS].pop(i)
					curdoc().roots[0]._property_values[WID_TABS].append(select_panel)                
					break			
			for i in range(len(curdoc().roots[0]._property_values[WID_TABS])):
				if curdoc().roots[0]._property_values[WID_TABS][i].id == WID_DECOMP_PANEL:
					curdoc().roots[0]._property_values[WID_TABS].pop(i)
					curdoc().roots[0]._property_values[WID_TABS].append(decomp_panel)                
					break			
			self.uploader.page.tabs.active=1

		except:
			pass
			### Checkpoint ###
			#print(MESSAGES["Download_callback_error"])
			### Checkpoint ###
			#main()
