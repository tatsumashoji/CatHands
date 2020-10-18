#!/usr/bin/env python
# -*- coding: utf-8 -*-


#========================================
#  Libraries
#========================================
import pandas as pd
from sklearn.manifold import TSNE, MDS
from sklearn.decomposition import PCA
import umap
from scipy.sparse.csgraph import connected_components # pip install umap-learn
# Libraries (Bokeh)
import bokeh
from bokeh.events import ButtonClick
from bokeh.models import CustomJS, HoverTool, ColumnDataSource, Div
from bokeh.models.widgets import Button, Select, RadioGroup, TextInput, TableColumn, DataTable
from bokeh.layouts import Column, row
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)

# Widget : FNAME
WN_FNAME = "FNAME"
WID_FNAME = "FNAME"
# Widget : METHOD
WN_METHOD = "METHOD"
WID_METHOD = "METHOD"
WPROP_METHOD = {}
WPROP_METHOD["labels"] = ["PCA", "tSNE", "MDS", "UMAP"]
WPROP_METHOD["active"] = 0
# Widget : EXECUTE
WN_EXECUTE = "EXECUTE"
WID_EXECUTE = "EXECUTE"
WPROP_EXECUTE = {}
WPROP_EXECUTE["width"] = 200
WPROP_EXECUTE["label"] = "Execute"
WPROP_EXECUTE["button_type"] = "success"
# Widget : FIGURE
WN_FIGURE = "FIGURE"
WID_FIGURE = "FIGURE"
WPROP_FIGURE = {}
WPROP_FIGURE["tools"] = "pan,box_zoom, lasso_select ,box_select, poly_select, tap, wheel_zoom, reset, save, zoom_in"
WPROP_FIGURE["plot_width"] = 800
WPROP_FIGURE["plot_height"] = 640
WPROP_FIGURE["title"] = "Subgrouping Result"
# Widget : COLOR_SELECT
WN_COLOR_SELECT = "COLOR_SELECT"
WID_COLOR_SELECT = "COLOR_SELECT"
WPROP_COLOR_SELECT = {}
WPROP_COLOR_SELECT["title"] = "Color:"
WPROP_COLOR_SELECT["value"] = "0"
WPROP_COLOR_SELECT["options"] = []
# Widget : DATA_TABLE
WN_DATA_TABLE = "DATA_TABLE"
WID_DATA_TABLE = "DATA_TABLE"
WPROP_DATA_TABLE = {}
WPROP_DATA_TABLE["width"] = 400
WPROP_DATA_TABLE["height"] = 400
WPROP_DATA_TABLE["columns"] = []
WPROP_DATA_TABLE["fit_columns"] = False
# Widget : DECOMP_PANEL
WN_DECOMP_PANEL = "DECOMP_PANEL"
WID_DECOMP_PANEL = "DECOMP_PANEL"
WPROP_DECOMP_PANEL = {}
WPROP_DECOMP_PANEL["title"] = "Decomposition"


#========================================
# MESSAGES
#========================================
MESSAGES = {
    "init_start" : ">> Status : Decomposition : __init__ : Loading header...",
    "init_error" : ">> Status : Decomposition : __init__ : ERROR.",
    "callback_colorSelect_start" : ">> Status : Decomposition : callback_colorSelect : Change color.",
    "callback_colorSelect_error" : ">> Status : Decomposition : callback_colorSelect : ERROR.",
    "callback_execute_init" : ">> Status : Decomposition : callback_execute : Execute decomposition",
    "callback_execute_error" : ">> Status : Decomposition : callback_execute : ERROR."
}


class Decomposition():
    def __init__(self, uploader):
        try:
            ### Checkpoint ###
            print(MESSAGES["init_start"])
            ### Checkpoint ###
            
            # df
            self.dtypes = uploader.df.dtypes.tolist()
            self.df_whole = uploader.df.df
            
            number_col = [i for i in range(len(self.dtypes)) if self.dtypes[i]=="number"]

            # nan, TRUE/FALSE -> string
            for i in range(len(self.df_whole.columns)):
                if not i in number_col:
                    self.df_whole.iloc[:,i] = self.df_whole.iloc[:,i].map(str)
                
            # used in decomposition
            self.df = uploader.df.df.iloc[:,number_col]
            
            
            # filename
            fname = Div( 
            	name=WN_FNAME,
            	id=WID_FNAME,
            	text = "Choose AI"
            )
            
            # analysis_method
            self.method = RadioGroup(
            	name=WN_METHOD,
            	id=WID_METHOD,
            	labels = WPROP_METHOD["labels"],
            	active = WPROP_METHOD["active"]
            )
            
            # execute_button
            execute = Button(
            	name = WN_EXECUTE,
            	id=WID_EXECUTE,
            	width=WPROP_EXECUTE["width"],
            	label = WPROP_EXECUTE["label"],
            	button_type = WPROP_EXECUTE["button_type"]
            )
            execute.on_event(ButtonClick, self.callback_execute)
            
            # graph
            self.graph = figure(
            	name = WN_FIGURE,
            	id = WID_FIGURE,
            	tools = WPROP_FIGURE["tools"],
            	title = WPROP_FIGURE["title"],
            	plot_width = WPROP_FIGURE["plot_width"],
            	plot_height = WPROP_FIGURE["plot_height"]
            )
            self.source = ColumnDataSource(data=dict(length=[], width=[]))
            self.source.data = {"0": [], "1": []}
            self.graph.circle(x="0", y="1", source=self.source)
            
            # color_select
            self.color_select = Select(
            	name=WN_COLOR_SELECT,
            	id=WID_COLOR_SELECT,
            	title = WPROP_COLOR_SELECT["title"],
            	value = WPROP_COLOR_SELECT["value"],
            	options = WPROP_COLOR_SELECT["options"]
            )
            self.color_select.on_change("value", self.callback_colorSelect)
            
            # data_table
            self.data_table = DataTable(
            	name=WN_DATA_TABLE,
            	id=WID_DATA_TABLE,
            	width=WPROP_DATA_TABLE["width"],
            	height=WPROP_DATA_TABLE["height"],
            	source=self.source,
            	columns = WPROP_DATA_TABLE["columns"],
            	fit_columns = WPROP_DATA_TABLE["fit_columns"]
            )
            
            # right area
            operation_area = Column(
            	fname,
            	self.method,
            	execute,
            	self.color_select,
            	self.data_table
            )
            self.bokeh = Panel(
            	name=WN_DECOMP_PANEL,
            	id=WID_DECOMP_PANEL,
            	child = row(self.graph, operation_area),
            	title=WPROP_DECOMP_PANEL["title"]
            )
            
        except:
        	### Checkpoint ###
        	print(MESSAGES["init_error"])
        	### Checkpoint ###
        	
            

    def callback_colorSelect(self, attr, old, new):
        try:
            ### Checkpoint ###
            print(MESSAGES["callback_colorSelect_start"])
            ### Checkpoint ###

            ## modified
            dtype = ""
            for i in range(len(self.dtypes)):
                if self.df_whole.columns[i] == new:
                    dtype = self.dtypes[i]
                    break
            
            if not dtype == "number":
                color_num = len(self.df_whole[new].unique().tolist())
                if color_num <= 256:
                    mapper = factor_cmap(
                        field_name = new,
                        palette = bokeh.palettes.viridis(len(self.df_whole[new].map(str).unique().tolist())),
                        factors = self.df_whole[new].map(str).unique().tolist()
                    )    
                else:
                    mapper = factor_cmap(
                        field_name = new,
                        palette = bokeh.palettes.viridis(1)*color_num,
                        factors = self.df_whole[new].unique().tolist()
                    )    
            else:
                mapper = linear_cmap(
                    field_name = new,
                    palette = bokeh.palettes.Viridis256,
                    low=min(self.df_whole[new].values),
                    high=max(self.df_whole[new].values)
                )
                    
            self.graph.circle(x="0", y="1", source=self.source, line_color=mapper, color=mapper)
            

        except:
        	### Checkpoint ###
        	print(MESSAGES["callback_colorSelect_error"])
    	    ### Checkpoint ###


    def callback_execute(self, event):
        try:
            ### Checkpoint ###
        	print(MESSAGES["callback_execute_init"])
        	### Checkpoint ###
        	print("OK10")

        	if self.method.active == 0:
        		pca = PCA(n_components=2)
        		result = pca.fit_transform(self.df)
        	elif self.method.active == 1:
        		tsne_model = TSNE(n_components=2)
        		result = tsne_model.fit_transform(self.df)
        	elif self.method.active == 2:
        		mds = MDS(n_jobs=1)
        		result = mds.fit_transform(self.df)
        	elif self.method.active == 3:
        	    result = umap.UMAP().fit_transform(self.df)
        	print("OK11")
        	    
        	dict = {"0": result[:, 0], "1": result[:, 1]}
        	columns = list()
        	for column in self.df_whole.columns:
        		dict[column] = self.df_whole[column].values
        		columns.append(TableColumn(field=column, title=column, width=100))
        		
        	print("OK12")
        	self.source.data = dict
        	self.data_table.columns = columns
        	target_column = self.df_whole.columns.values[0]
        	
        	## modified
        	if not self.dtypes[0] == "number":
        	    color_num = len(self.df_whole[target_column].unique().tolist())
        	    if color_num <= 256:
        	        mapper = factor_cmap(
        	            field_name = target_column,
        	            palette = bokeh.palettes.viridis(len(self.df_whole[target_column].unique().tolist())),
        	            factors = self.df_whole[target_column].unique().tolist()
        	        )
        	    else:
        	        mapper = factor_cmap(
        	            field_name = target_column,
        	            palette = bokeh.palettes.viridis(1)*color_num,
        	            factors = self.df_whole[target_column].unique().tolist()
        	        )    
        	else:
        	    mapper = linear_cmap(
        	        field_name = target_column,
        		    palette = bokeh.palettes.Viridis256,
        		    low=min(self.df_whole[target_column].values),
        		    high=max(self.df_whole[target_column].values)
        	    )
        	
        	self.graph.circle(x="0", y="1", source=self.source, line_color=mapper, color=mapper)
        	hover = HoverTool(tooltips=[
        		("index", "$index"),
        		(target_column, "@"+target_column),
        	])
        	self.graph.add_tools(hover)
        	self.color_select.options = list(self.df_whole.columns)
        	self.color_select.value = "0"
        	
        except:
        	### Checkpoint ###
        	print(MESSAGES["callback_execute_error"])
        	### Checkpoint ###
        


