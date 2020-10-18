#!/usr/bin/env python
# -*- coding: utf-8 -*-


#========================================
#  Libraries
#========================================
import io
import pandas as pd
from bokeh.models import Panel, Div


#========================================
# Parameters
#========================================
# dtype definition
DTYPE_LIST = ["factor_nan", "number", "factor", "general"]
# threshold used for donut
DONUT_MAX_LEN = 11
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
    "DataFrame_init_start" : ">> Status : DataFrame : __init__ :  Initializes DataFrame-related properties...",
    "DataFrame_init_error" : ">> Status : DataFrame : __init__ :  ERROR : Initialization failed.",
    "DataFrame_reload_df_start" : ">> Status : DataFrame : reload_df :  Uptakes FileInputs' contents into DataFrame...",
    "DataFrame_reload_df_error" : ">> Status : DataFrame : reload_df :  ERROR : Uptaking failed."
}


#========================================
# DataFrame : df, dtypes, subcol, subrow_Decomposition, subrow_Manual, updateStatus : reload_df, get_dtypes
#========================================
class DataFrame():
	def __init__(self):
		try:
			### Checkpoint ###
			print(MESSAGES["DataFrame_init_start"])
			### Checkpoint ###
			self.df = pd.DataFrame([])
			self.dtypes = []
			self.subcol = []
			self.subrow_Decomposition = []
			self.subrow_Manual = []
			self.updateStatus = []
			self.bokeh_filename = Div(
				name = WN_FILENAME,
				id = WID_FILENAME,
				text = WPROP_FILENAME["text"] % (WPROP_FILENAME["default_text"]),
				width = WPROP_FILENAME["width"]
			)
			self.bokeh_columns = Div(
				name = WN_COLUMNS,
				id = WID_COLUMNS,
				text = WPROP_COLUMNS["text"] % (WPROP_COLUMNS["default_text"]),
				width = WPROP_COLUMNS["width"]
			)
			self.bokeh_records = Div(
				name = WN_RECORDS,
				id = WID_RECORDS,
				text = WPROP_RECORDS["text"] % (WPROP_RECORDS["default_text"]),
				width = WPROP_RECORDS["width"]
			)
			self.bokeh_selected_records = Div(
				name = WN_SELECTED_RECORDS,
				id = WID_SELECTED_RECORDS,
				text = WPROP_SELECTED_RECORDS["text"] % (WPROP_SELECTED_RECORDS["default_text"]),
				width = WPROP_SELECTED_RECORDS["width"]
			)
		except:
			### Checkpoint ###
			print(MESSAGES["DataFrame_init_error"])
			### Checkpoint ###
			
	def reload_df(self, uploader): # set_df
		try:
			### Checkpoint ###
			print(MESSAGES["DataFrame_reload_df_start"])
			### Checkpoint ###
			if uploader.bokeh.filename.endswith(".csv"):
				self.df = pd.read_csv(io.StringIO(uploader.bokeh.value))
			elif uploader.bokeh.filename.endswith(".tsv"):
				self.df = pd.read_table(io.StringIO(uploader.bokeh.value))
			elif uploader.bokeh.filename.endswith(".xlsx"):
				self.df = pd.read_excel(io.StringIO(uploader.bokeh.value))
			self.dtypes = self.df.apply(self.get_dtypes) # dtypes
			self.subcol = [self.df.columns.get_loc(x) for x in self.df.columns] #sub_col
			self.subrow_Decomposition = self.df.index.tolist() # subrow_Dec
			self.subrow_Manual = self.df.index.tolist() # subrow_Dis
			self.updateStatus = []
			self.bokeh_filename.text = WPROP_FILENAME["text"] % (uploader.bokeh.filename)
			self.bokeh_columns.text = WPROP_COLUMNS["text"] % (str(len(self.df.columns)))
			self.bokeh_records.text = WPROP_RECORDS["text"] % (str(len(self.df)))
			self.bokeh_selected_records.text = WPROP_SELECTED_RECORDS["text"] % (str(len(self.subrow_Manual)))
		except:
			### Checkpoint ###
			print(MESSAGES["DataFrame_reload_df_error"])
			### Checkpoint ###
			self.df = pd.DataFrame([]) # df
			self.dtypes = [] # dtypes, dtype_name
			self.subcol = [] #sub_col
			self.subrow_Decomposition = [] # subrow_Dec
			self.subrow_Manual = [] # subrow_Dis
			self.updateStatus = []
			self.bokeh_filename = Div(
				name = WN_FILENAME,
				id = WID_FILENAME,
				text = WPROP_FILENAME["text"] % (WPROP_FILENAME["default_text"]),
				width = WPROP_FILENAME["width"]
			)
			self.bokeh_columns = Div(
				name = WN_COLUMNS,
				id = WID_COLUMNS,
				text = WPROP_COLUMNS["text"] % (WPROP_COLUMNS["default_text"]),
				width = WPROP_COLUMNS["width"]
			)
			self.bokeh_records = Div(
				name = WN_RECORDS,
				id = WID_RECORDS,
				text = WPROP_RECORDS["text"] % (WPROP_RECORDS["default_text"]),
				width = WPROP_RECORDS["width"]
			)
			self.bokeh_selected_records = Div(
				name = WN_SELECTED_RECORDS,
				id = WID_SELECTED_RECORDS,
				text = WPROP_SELECTED_RECORDS["text"] % (WPROP_SELECTED_RECORDS["default_text"]),
				width = WPROP_SELECTED_RECORDS["width"]
			)
    					
	def get_dtypes(self, sr):
		self.DTYPE_LIST = DTYPE_LIST
		try:
			if sr.map(lambda x : "bool" in str(type(x))).all():
				return self.DTYPE_LIST[2]
			return self.DTYPE_LIST[0] if sr.astype(float).isnull().sum() > 0 else self.DTYPE_LIST[1]
		except:
			return self.DTYPE_LIST[2] if len(sr.unique()) <= DONUT_MAX_LEN else self.DTYPE_LIST[3]
        
