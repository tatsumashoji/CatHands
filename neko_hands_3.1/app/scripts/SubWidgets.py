#!/usr/bin/env python
# -*- coding: utf-8 -*-

#========================================
#  Libraries
#========================================
import sys, os, io, time, base64
import numpy as np
import pandas as pd
import math
# Libraries (Bokeh)
from bokeh.io import curdoc
from bokeh.transform import cumsum
from bokeh.plotting import figure
from bokeh.layouts import layout, column, row
from bokeh.models import ColumnDataSource, CustomJS, DataTable, RangeTool, TableColumn, NumberFormatter, StringFormatter, HoverTool, Div, Panel, Tabs
from bokeh.models.widgets import Slider, Select, FileInput, RangeSlider, Button, DataTable, TableColumn, NumberFormatter, RadioButtonGroup, CheckboxGroup, Toggle, TextInput

from bokeh.models.markers import InvertedTriangle


#========================================
#  Color Definition
#========================================
Spectral1 = ["#5e4fa2"]
Spectral2 = ["#5e4fa2", "#3288bd"]
Spectral3 = ["#5e4fa2", "#3288bd", "#66c2a5"]
Spectral4 = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4"]
Spectral5 = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598"]
Spectral6 = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#fee08b"]
Spectral7 = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#fee08b", "#fdae61"]
Spectral8 = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#fee08b", "#fdae61", "#f46d43"]
Spectral9 = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#fee08b", "#fdae61", "#f46d43", "#d53e4f"]
Spectral10 = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#fee08b", "#fdae61", "#f46d43", "#d53e4f", "#9e0142"]
Spectral11 = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#fee08b", "#fdae61", "#f46d43", "#d53e4f", "#9e0142", "#ffffbf"]
color_def = [Spectral1, Spectral2, Spectral3, Spectral4, Spectral5, Spectral6, Spectral7 ,Spectral8 ,Spectral9, Spectral10, Spectral11]
category_color = ["#67c2a5", "#f46d43", "#75899d"]

DONUT_MAX_LEN = 11

#========================================
#  SubWidgets
#========================================
class Widgets():
    def __init__(self):
        self.widgets = {}
        
    def add_widget(self, widget, df, sr, key, graphs):
        instance = widget(df, sr, key, graphs)
        self.widgets[instance.name] = instance

# Title : name, bokeh : adjust
class Title():
    def __init__(self, df, sr, key, graphs):
        self.name = "Title"
        self.bokeh = Div(text='''
                <header class="post-header">
                    <h1 class="post-title">%s</h1>
                    <p class="post-meta">
                        <span class="post-category post-category-design">%s</span>
                    </p>
                </header>
        ''' % (sr.name, df.dtypes[key]), width=1000)

    def adjust(self):
        pass

# Checkbox : name, df, sr, sr_sub, bokeh : callback, adjust
class Checkbox():
    def __init__(self, df, sr, key, graphs):
        self.name = "Checkbox"
        self.df = df
        self.sr = sr
        self.key = key
        self.graphs = graphs
        self.sr_sub = sr[df.subrow_Manual]
        unique = [str(x) for x in sr.unique().tolist()]
        unique_sub = [str(x) for x in self.sr_sub.unique().tolist()]
        self.bokeh = CheckboxGroup(labels=[str(i) for i in unique], width=150)
        self.bokeh.active = [i for i in range(len(self.bokeh.labels)) if self.bokeh.labels[i] in unique_sub]
        self.bokeh.on_change('active', self.callback)

    def callback(self, attr, old, new):
        if not self in self.df.updateStatus:
            self.df.updateStatus.append(self)
            vals = [self.bokeh.labels[i] for i in self.bokeh.active]
            self.df.subrow_Manual = self.sr[self.sr.map(lambda x : str(x) in vals)].index.tolist()
            self.graphs.diffuse(self.key)

    def adjust(self):
        self.df.updateStatus.append(self)
        unique_sub = self.sr[self.df.subrow_Manual].unique().tolist()
        self.bokeh.active = [i for i in range(len(self.bokeh.labels)) if self.bokeh.labels[i] in unique_sub]
        
# Checkbox_NaN : name, df, sr, sr_sub, bokeh : callback, adjust
class Checkbox_NaN():
    def __init__(self, df, sr, key, graphs):
        self.name = "Checkbox_NaN"
        self.df = df
        self.sr = sr
        self.key = key
        self.graphs = graphs
        self.sr_sub = sr[df.subrow_Manual]
        n_NaN = self.sr_sub.isnull().sum()
        self.bokeh = CheckboxGroup(labels=["NaN","Numbers"], width=150)
        self.bokeh.active = [1] if n_NaN == 0 else [0] if n_NaN == len(self.sr_sub) else [] if len(self.sr_sub) == 0 else [0,1]
        self.bokeh.on_change('active', self.callback)

    def callback(self, attr, old, new):
        if not self in self.df.updateStatus:
            self.df.updateStatus.append(self)
            vals = [self.bokeh.labels[i] for i in self.bokeh.active]
            if "NaN" in vals and "Numbers" in vals:
                self.df.subrow_Manual = self.sr.index.tolist()
            elif "NaN" in vals:
                self.df.subrow_Manual = self.sr[(self.sr.isnull())].index.tolist()
            elif "Numbers" in vals:
                self.df.subrow_Manual = self.sr_sub[(~self.sr.isnull())].index.tolist()
            else:
                self.df.subrow_Manual = pd.Series([]).index.tolist()
            self.graphs.diffuse(self.key)

    def adjust(self):
        self.df.updateStatus.append(self)
        n_total = len(self.df.subrow_Manual)
        n_NaN = n_total.isnull().sum()
        self.bokeh.active = [] if n_total == 0 else [1] if n_NaN == 0 else [0] if n_NaN == n_total else [0,1]

# Donut : name, df, sr, sr_sub, bokeh, source : adjust
class Donut():
    def __init__(self, df, sr, key, graphs):
        self.name = "Donut"
        self.df = df
        self.sr = sr
        self.sr_sub = sr[df.subrow_Manual]
        self.bokeh = figure(plot_height=300, plot_width=500, toolbar_location=None, outline_line_color=None, x_range=[-1,2], tooltips = [('','@value'),('','@percentage')])
        factors = dict(self.sr_sub.value_counts())
        length = len(factors)
        donut_dict = {}
        if length > DONUT_MAX_LEN:
            self.bokeh.visible = False
            donut_dict["keys"] = []
            donut_dict["value"] = []
            donut_dict["angle"] = []
            donut_dict["color"] = []
            donut_dict["percentage"] = []
        else:
            donut_dict["keys"] = [str(i) for i in list(factors.keys())]
            donut_dict["value"] = list(factors.values())
            donut_dict["angle"] = [i/sum(factors.values()) * 2*math.pi for i in donut_dict["value"]]
            donut_dict["color"] = color_def[length-1]
            donut_dict["percentage"] = ["( "+str(round(100.0*v/sum(donut_dict["value"]),3))+" %)" for v in donut_dict["value"]]
        self.source = ColumnDataSource(data=donut_dict)
        self.bokeh.annular_wedge(
            x=0, y=1, inner_radius=0.35, outer_radius=0.8,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='keys', source=self.source
        )
        self.bokeh.axis.axis_label=None
        self.bokeh.axis.visible=False
        self.bokeh.grid.grid_line_color = None
        self.bokeh.legend.label_text_font_size = "1em"
        self.bokeh.legend.border_line_color = None
        #self.bokeh.legend.location = (320,270 - 23.7*length)
        self.bokeh.min_border_left = 0
        
    def adjust(self):
        if len(self.df.subrow_Manual) == 0:
            self.bokeh.visible = False
            return None
        else:
            self.bokeh.visible = True
        self.df.updateStatus.append(self)
        factors = dict(self.sr[self.df.subrow_Manual].value_counts())
        length = len(factors)
        if length > DONUT_MAX_LEN:
            self.bokeh.visible = False
            return None
        else:
            self.bokeh.visible = True
        donut_dict = {}
        donut_dict["keys"] = [str(i) for i in list(factors.keys())]
        donut_dict["value"] = list(factors.values())
        donut_dict['angle'] = [i/sum(factors.values()) * 2*math.pi for i in donut_dict['value']]
        donut_dict['color'] = color_def[length-1]
        donut_dict['percentage'] = ['( '+str(round(100.0*v/sum(donut_dict['value']),3))+' %)' for v in donut_dict['value']]
        self.source.data = donut_dict

# Donut_NaN : name, df, sr, sr_sub, bokeh, source : adjust
class Donut_NaN():
    def __init__(self, df, sr, key, graphs):
        self.name = "Donut_NaN"
        self.df = df
        self.sr = sr
        self.sr_sub = sr[df.subrow_Manual]
        self.bokeh = figure(plot_height=300, plot_width=500, toolbar_location=None, outline_line_color=None, x_range=[-1,2], tooltips = [('','@value'),('','@percentage')])
        n_NaN = self.sr_sub.isnull().sum()
        factors = {"NaN":n_NaN, "Numbers":len(df.subrow_Manual) - n_NaN}
        length = len(factors)
        donut_dict = {}
        donut_dict["keys"] = list(factors.keys())
        donut_dict["value"] = list(factors.values())
        donut_dict['angle'] = [i/sum(factors.values()) * 2*math.pi for i in donut_dict['value']]
        donut_dict['color'] = color_def[length-1]
        donut_dict['percentage'] = ['( '+str(round(100.0*v/sum(donut_dict['value']),3))+' %)' for v in donut_dict['value']]
        self.bokeh.annular_wedge(
            x=0, y=1, inner_radius=0.35, outer_radius=0.8,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='keys', source=ColumnDataSource(data=donut_dict)
        )
        self.bokeh.axis.axis_label=None
        self.bokeh.axis.visible=False
        self.bokeh.grid.grid_line_color = None
        self.bokeh.legend.label_text_font_size = "1em"
        self.bokeh.legend.border_line_color = None
        self.bokeh.legend.location = (320,270 - 23.7*length)
        self.bokeh.min_border_left = 0

    def adjust(self):
        if len(self.df.subrow_Manual) == 0:
            self.bokeh.visible = False
            return None
        else:
            self.bokeh.visible = True
        self.df.updateStatus.append(self)
        factors = dict(self.sr[self.df.subrow_Manual].value_counts())
        n_NaN = self.sr[self.df.subrow_Manual].isnull().sum()
        factors = {"NaN":n_NaN, "Numbers":len(self.df.subrow_Manual) - n_NaN}
        length = len(factors)
        donut_dict = {}
        donut_dict["keys"] = list(factors.keys())
        donut_dict["value"] = list(factors.values())
        donut_dict['angle'] = [i/sum(factors.values()) * 2*math.pi for i in donut_dict['value']]
        donut_dict['color'] = color_def[length-1]
        donut_dict['percentage'] = ['( '+str(round(100.0*v/sum(donut_dict['value']),3))+' %)' for v in donut_dict['value']]
        self.bokeh.renderers[0].data_source.data = donut_dict

# Table : name, df, sr, sr_sub, bokeh : adjust
class Table():
    def __init__(self, df, sr, key, graphs):
        self.name = "Table"
        self.df = df
        self.sr = sr
        self.sr_sub = sr[df.subrow_Manual]
        columns = [TableColumn(field=str(sr.name), title="Value", formatter=StringFormatter(text_align="left"))]
        self.bokeh = DataTable(source=ColumnDataSource(data=pd.DataFrame(self.sr_sub)), columns=columns, height=300, width=250)

    def adjust(self):
        self.df.updateStatus.append(self)
        self.bokeh._property_values["source"].data = pd.DataFrame(self.sr[self.df.subrow_Manual])

# Histogram : name, df, sr, sr_sub, bins, AXISES, SOURCES, bokeh : ADJUSTS
class Histogram():
    def __init__(self, df, sr, key, graphs):
        self.name = "Histogram"
        self.df = df
        self.sr = sr
        self.sr_sub = sr[df.subrow_Manual]
        # parms
        x_min = self.sr_sub.min()
        self.bins = 80
        # x_axis
        self.x_axis_base_label = ["Value"]
        self.x_axis_base_option = ["Value"]
        self.x_axis_base_active = 0
        self.x_axis_label_function = lambda x : x if self.x_axis_scale_active == 0 else "Log( " + str(x) + " + 1 )"
        self.x_axis_scale_option = ["Normal", "Log"]
        self.x_axis_scale_active = 0
        self.x_axis = self.x_axis_label_function(self.x_axis_base_label[self.x_axis_base_active])
        # y_axis
        self.y_axis_base_label = ["Frequency", "Percentage"]
        self.y_axis_base_option = ["Frequency", "Percentage"]
        self.y_axis_base_active = 0
        self.y_axis_label_function = lambda x : x if self.y_axis_scale_active == 0 else "Log( " + str(x) + " + 1 )"
        self.y_axis_scale_option = ["Normal", "Log"]
        self.y_axis_scale_active = 0
        self.y_axis = self.y_axis_label_function(self.y_axis_base_label[self.y_axis_base_active])
        self.cumulative = "Off"
        # Statistics
        stats = dict((self.sr_sub.describe()))
        stats["skewness"] = self.sr_sub.skew()
        stats["kurtosis"] = self.sr_sub.kurtosis()
        stats_table = pd.DataFrame([[key, '{:,.3f}'.format(round(stats[key],3))] for key in stats.keys()], index=stats.keys(), columns=["Statistics","Value"])
        # Histogram
        y, edges = np.histogram(self.sr, bins=self.bins)
        left = edges[:-1]
        right = edges[1:]
        popup_hist = [('{:,.3f}'.format(round(100.0*sum(y[0:(i+1)])/sum(y),3))+"% covered") for i in range(len(left))] 
        self.hist_source = ColumnDataSource(data=dict(left=left, right=right, y=y, pname=popup_hist))
        # Cumulative
        cum = [sum(y[:(i+1)]) for i in range(len(y))] if self.cumulative != "Off" else [0]*len(y)
        x = [(left[i]+right[i])*1.0/2 for i in range(len(left))]
        popup_cum = [('{:,.3f}'.format(round(cum[i],3))+"% covered") for i in range(len(x))]
        self.hist_cum_source = ColumnDataSource(data=dict(x=x, cum=cum, pname=popup_cum))
        # Quantiles
        ymax = max(y)
        x_iqr = [stats["25%"],stats["50%"],stats["75%"]]
        iqr = [ymax, ymax, ymax]
        popup_boxarrow = ["25%","50%","75%"]
        self.hist_qt_source = ColumnDataSource(data=dict(x_iqr=x_iqr, iqr=iqr, pname=popup_boxarrow))
        # Mean
        x_mean = [stats["mean"]]
        mean = [ymax]
        popup_meanarrow = ["Mean"]    
        self.hist_mean_source = ColumnDataSource(data=dict(x_mean=x_mean, mean=mean, pname=popup_meanarrow))
        # StatTable
        self.hist_stat_source = ColumnDataSource(data=stats_table)
        columns = [
            TableColumn(field="Statistics", title="Statistics", formatter=StringFormatter(text_align="center")),
            TableColumn(field="Value", title="Value", formatter=StringFormatter(text_align="right"))
        ]
        # Graph
        self.bokeh = figure(plot_height=350, plot_width=400, tooltips = [("","@pname")])
        self.bokeh.quad(top='y', bottom=0, left='left', right='right', source=self.hist_source, fill_color="navy", line_color="white", alpha=0.5)
        self.bokeh.line(x='x', y='cum', source=self.hist_cum_source, line_color=Spectral11[6], line_width=3, alpha=0.7)
        self.bokeh.add_glyph(self.hist_qt_source, InvertedTriangle(x="x_iqr", y="iqr", size=10, line_color="#de2d26", line_width=2, fill_color=None))
        self.bokeh.add_glyph(self.hist_mean_source, InvertedTriangle(x="x_mean", y="mean", size=10, line_color="green", line_width=2, fill_color=None))
        # Axis
        self.bokeh.xaxis.axis_label = self.x_axis
        self.bokeh.yaxis.axis_label = self.y_axis
        # Stat Table
        self.hist_stat_table = DataTable(source=self.hist_stat_source, columns=columns, height=300, width=250)

    def adjust(self):
        self.df.updateStatus.append(self)
        if len(self.df.subrow_Manual) == 0:
            self.bokeh.visible = False
            return None
        else:
            self.bokeh.visible = True
        self.sr_sub = self.sr[self.df.subrow_Manual]
        x_min = self.sr_sub.min()
        stats = dict((self.sr_sub.describe()))
        stats["skewness"] = self.sr_sub.skew()
        stats["kurtosis"] = self.sr_sub.kurtosis()
        stats_table = pd.DataFrame([[key, '{:,.3f}'.format(round(stats[key],3))] for key in stats.keys()], index=stats.keys(), columns=["Statistics","Value"])
        # Histogram
        self.x_axis = self.x_axis_label_function(self.x_axis_base_label[self.x_axis_base_active])
        self.y_axis = self.y_axis_label_function(self.y_axis_base_label[self.y_axis_base_active])
        if self.x_axis_scale_active != 0:
            if x_min <= 0:
                sr_sub = self.sr_sub[0<self.sr_sub]
                x_min = sr.min()
                bins = np.logspace(math.log10(x_min), math.log10(sr_sub.max()), self.bins)
                y, edges = np.histogram(sr_sub, bins=bins)
                left = [math.log10(i) for i in edges[:-1]]
                right = [math.log10(i) for i in edges[1:]]
            else:
                bins = np.logspace(math.log10(x_min), math.log10(self.sr_sub.max()), self.bins)
                y, edges = np.histogram(self.sr_sub, bins=bins)
                left = [math.log10(i) for i in edges[:-1]]
                right = [math.log10(i) for i in edges[1:]]
        else:
            y, edges = np.histogram(self.sr_sub, bins=self.bins)
            left = edges[:-1]
            right = edges[1:]
        if self.y_axis_scale_active != 0:
            y = [math.log10(i+1) for i in y]
        if self.y_axis_base_active != 0:
            ysum = sum(y)
            y =  [1.0*i / ysum for i in y]
        cum = [sum(y[:(i+1)]) for i in range(len(y))] if self.cumulative != "Off" else [0]*len(y)
        x = [(left[i]+right[i])*1.0/2 for i in range(len(left))]
        popup_hist = [('{:,.3f}'.format(round(100.0*sum(y[0:(i+1)])/sum(y),3))+"% covered") for i in range(len(left))] 
        popup_cum = [('{:,.3f}'.format(round(cum[i],3))+"% covered") for i in range(len(x))]
        # Quantiles
        ymax = max(y)
        x_iqr = [stats["25%"], stats["50%"], stats["75%"]]
        iqr = [ymax, ymax, ymax]
        popup_boxarrow = ["25%", "50%", "75%"]
        # Mean
        x_mean = [stats["mean"]]
        mean = [ymax]    
        popup_meanarrow = ["Mean"]    
        # StatTable
        row_name = list(stats.keys())
        row_value = ['{:,.3f}'.format(round(stats[key],3)) for key in stats.keys()]
        # adjust
        self.hist_source.data = dict(left=left, right=right, y=y, pname=popup_hist)
        self.hist_cum_source.data = dict(x=x, cum=cum, pname=popup_cum)
        self.hist_qt_source.data = dict(x_iqr=x_iqr, iqr=iqr, pname=popup_boxarrow)
        self.hist_mean_source.data = dict(x_mean=x_mean, mean=mean, pname=popup_meanarrow)
        self.hist_stat_source.data = dict(Statistics=row_name, Value=row_value)
            
    def adjust_xaxis(self, val):
        self.x_axis_scale_active = 0 if val == "Normal" else 1
        self.adjust_interface()

    def adjust_bin(self, val):
        self.bins = val
        self.adjust_interface()
			    
    def adjust_yaxis(self, val):
        self.y_axis_scale_active = 0 if val == "Normal" else 1
        self.adjust_interface()

    def adjust_yunit(self, val):
        self.y_axis_base_active = 0 if val == "Frequency" else 1
        self.adjust_interface()

    def adjust_cum(self, val):
        self.cumulative = val
        self.adjust_interface()

    def adjust_interface(self):
        if len(self.df.subrow_Manual) == 0:
            self.visible = False
            return None
        else:
            self.bokeh.visible = True
        x_min = self.sr_sub.min()
        stats = dict((self.sr_sub.describe()))
        stats["skewness"] = self.sr_sub.skew()
        stats["kurtosis"] = self.sr_sub.kurtosis()
        stats_table = pd.DataFrame([[key, '{:,.3f}'.format(round(stats[key],3))] for key in stats.keys()], index=stats.keys(), columns=["Statistics","Value"])
        # Histogram
        self.x_axis = self.x_axis_label_function(self.x_axis_base_label[self.x_axis_base_active])
        self.y_axis = self.y_axis_label_function(self.y_axis_base_label[self.y_axis_base_active])
        if self.x_axis_scale_active != 0:
            if x_min <= 0:
                sr_sub = self.sr_sub[0<self.sr_sub]
                x_min = sr.min()
                bins = np.logspace(math.log10(x_min), math.log10(sr_sub.max()), self.bins)
                y, edges = np.histogram(sr_sub, bins=bins)
                left = [math.log10(i) for i in edges[:-1]]
                right = [math.log10(i) for i in edges[1:]]
            else:
                bins = np.logspace(math.log10(x_min), math.log10(self.sr_sub.max()), self.bins)
                y, edges = np.histogram(self.sr_sub, bins=bins)
                left = [math.log10(i) for i in edges[:-1]]
                right = [math.log10(i) for i in edges[1:]]
            if self.y_axis_scale_active != 0:
                y = [math.log10(i+1) for i in y]
            if self.y_axis_base_active != 0:
                ysum = sum(y)
                y =  [1.0*i / ysum for i in y]
            # Quantiles
            ymax = max(y)
            x_iqr = [math.log10(stats["25%"]), math.log10(stats["50%"]), math.log10(stats["75%"])]
            iqr = [ymax, ymax, ymax]
            popup_boxarrow = ["25%", "50%", "75%"]
            # Mean
            x_mean = [math.log10(stats["mean"])]
            mean = [ymax]    
            popup_meanarrow = ["Mean"]    
        else:
            y, edges = np.histogram(self.sr_sub, bins=self.bins)
            left = edges[:-1]
            right = edges[1:]
            if self.y_axis_scale_active != 0:
                y = [math.log10(i+1) for i in y]
            if self.y_axis_base_active != 0:
                ysum = sum(y)
                y =  [1.0*i / ysum for i in y]
            # Quantiles
            ymax = max(y)
            x_iqr = [stats["25%"], stats["50%"], stats["75%"]]
            iqr = [ymax, ymax, ymax]
            popup_boxarrow = ["25%", "50%", "75%"]
            # Mean
            x_mean = [stats["mean"]]
            mean = [ymax]    
            popup_meanarrow = ["Mean"]    
        cum = [sum(y[:(i+1)]) for i in range(len(y))] if self.cumulative != "Off" else [0]*len(y)
        x = [(left[i]+right[i])*1.0/2 for i in range(len(left))]
        popup_hist = [('{:,.3f}'.format(round(100.0*sum(y[0:(i+1)])/sum(y),3))+"% covered") for i in range(len(left))] 
        popup_cum = [('{:,.3f}'.format(round(cum[i],3))+"% covered") for i in range(len(x))]
        # StatTable
        row_name = list(stats.keys())
        row_value = ['{:,.3f}'.format(round(stats[key],3)) for key in stats.keys()]
        # adjust
        self.hist_source.data = dict(left=left, right=right, y=y, pname=popup_hist)
        self.hist_cum_source.data = dict(x=x, cum=cum, pname=popup_cum)
        self.hist_qt_source.data = dict(x_iqr=x_iqr, iqr=iqr, pname=popup_boxarrow)
        self.hist_mean_source.data = dict(x_mean=x_mean, mean=mean, pname=popup_meanarrow)
        self.bokeh.xaxis.axis_label = self.x_axis
        self.bokeh.yaxis.axis_label = self.y_axis
        self.hist_stat_source.data = dict(Statistics = row_name, Value = row_value)

# Inputs : name, df, sr, key, widget, bokeh : CALLBACKS, adjust
class Inputs():
    def __init__(self, df, sr, key, graphs):
        self.name = "Inputs"
        self.df = df
        self.sr = sr
        self.key = key
        self.graphs = graphs
        sr_sub = sr[df.subrow_Manual]
        sr_min = math.floor(sr.min())
        sr_max = math.ceil(sr.max())
        if sr_min == sr_max: # con't be same
            sr_max += 1
        sr_steps = min((sr_max-sr_min)/100, 1)
        self.widget = {
            "x_min" : Slider(title="x min", value=sr_sub.min(), start=sr_min, end=sr_max, step=sr_steps),
            "x_max" : Slider(title="x max", value=sr_sub.max(), start=sr_min, end=sr_max, step=sr_steps),
            "x_axis" : Select(title="x axis scale", options=["Normal", "Log"], value="Normal"),
            "bins" : Slider(title="Number of Bins", value=80, start=10, end=300, step=10),
            "y_axis" : Select(title="y axis scale", options=["Normal", "Log"], value="Normal"),
            "y_unit" : Select(title="y axis unit", options=["Frequency", "Percentage"], value="Frequency"),
            "cumulative" : Select(title="Cumulative", options=["Off", "On"], value="Off"),
        }
        # Callbacks
        self.widget["x_min"].on_change('value', self.callback)
        self.widget["x_max"].on_change('value', self.callback)
        self.widget["x_axis"].on_change('value', self.callback_xaxis)
        self.widget["bins"].on_change('value', self.callback_bin)
        self.widget["y_axis"].on_change('value', self.callback_yaxis)
        self.widget["y_unit"].on_change('value', self.callback_yunit)
        self.widget["cumulative"].on_change('value', self.callback_cum)
        # Packaging
        self.bokeh = column([self.widget["x_min"], self.widget["x_max"] , self.widget["x_axis"] , self.widget["bins"] , self.widget["y_axis"] , self.widget["y_unit"] , self.widget["cumulative"]], width=200, height=300)
        
    def adjust(self):
        self.df.updateStatus.append(self)
        if len(self.df.subrow_Manual) == 0:
            sr_min = self.sr.min()
            self.widget["x_min"].value = sr_min
            self.widget["x_max"].value = sr_min
        else:
            sr_sub = self.sr[self.df.subrow_Manual]
            self.widget["x_min"].value = sr_sub.min()
            self.widget["x_max"].value = sr_sub.max()
        
    def callback(self, attr, old, new):
        if not self in self.df.updateStatus:
            self.df.updateStatus.append(self)
            self.df.subrow_Manual = self.sr[(self.widget["x_min"].value <= self.sr) & (self.sr <= self.widget["x_max"].value)].index.tolist()
            self.graphs.diffuse(self.key)

    def callback_xaxis(self, attr, old, new):
        val = self.widget["x_axis"].value
        self.graphs.graphs[self.key].widgets["Histogram"].adjust_xaxis(val)

    def callback_bin(self, attr, old, new):
        val = self.widget["bins"].value
        self.graphs.graphs[self.key].widgets["Histogram"].adjust_bin(val)
			    
    def callback_yaxis(self, attr, old, new):
        val = self.widget["y_axis"].value
        self.graphs.graphs[self.key].widgets["Histogram"].adjust_yaxis(val)

    def callback_yunit(self, attr, old, new):
        val = self.widget["y_unit"].value
        self.graphs.graphs[self.key].widgets["Histogram"].adjust_yunit(val)

    def callback_cum(self, attr, old, new):
        val = self.widget["cumulative"].value
        self.graphs.graphs[self.key].widgets["Histogram"].adjust_cum(val)
