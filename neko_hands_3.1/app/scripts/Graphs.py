#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Debug用コメント、スイッチ、Tryぶん
# Decomposition
# 他のファイルでデバッグ
# リンク切断高速化
# 全体
# このスクリプトなど、変数名
# 変数の外部指定化
# 表の表示
# Authentication
# タスクの切り分け
# ラップサイズデザイン <- 表示ゼロで大きさが狂う
# Libraryの種類
# .tsc, .xlsx
# .propertyの取り方じゃなくて、dataでとる方法に変える
# 0行の例外、0列の時の表示、ヘッダ対応
# カテゴリカラー

#========================================
#  Libraries
#========================================
import numpy as np
# Libraries (Bokeh)
from bokeh.layouts import layout
from bokeh.models import Panel
# Modules
from scripts.SubWidgets import Widgets, Title, Checkbox, Checkbox_NaN, Donut, Donut_NaN, Table, Histogram, Inputs


#========================================
# Parameters
#========================================
# dtype definition
DTYPE_LIST = ["factor_nan", "number", "factor", "general"]
# Num of columns per a page
PAGE_MAX_COL = 10
# graphs definition
DTYPE_VS_WIDGETS_DEFINITION = [
    [Title, Checkbox_NaN, Donut_NaN, Table],
    [Title, Inputs, Histogram, Donut],
    [Title, Checkbox, Donut, Table],
    [Title, Table]
]
DTYPE_VS_WIDGETS_STRUCT_DEFINITION = [
    [["Title"], ["Checkbox_NaN", "Donut_NaN", "Table"]],
    [["Title"], ["Inputs", "Histogram", "Donut"]],
    [["Title"], ["Checkbox", "Donut", "Table"]],
    [["Title"], ["Table"]]
]
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
    "init_start" : ">> Status : Graphs : __init__ :  Calculates target columns...",
    "init_checkpoint1" : ">> Status : Graphs : __init__ : %s columns seleted to display.",
    "init_checkpoint2" : ">> Status : Graphs : __init__ : WidgetsLists '%s' selected for Col #%s ",
    "init_checkpoint3" : ">> Status : Graphs : __init__ : Widget '%s' loaded.",
    "init_error" : ">> Status : Graphs : __init__ :  ERROR : Unknown error during widgets loading.",
    "diffuse_start" : ">> Status : Graphs : diffuse() : Start diffusing.",
    "subwidget" : ">> Status : Graphs : diffuse() : %s has changed."
}

#========================================
# Graphs : bokeh, graphs : diffuse
#========================================
class Graphs():
    def __init__(self, Df, PageStatus, link_status):
        try:
            ### Checkpoint ###
            print(MESSAGES["init_start"])
            ### Checkpoint ###
            self.Df = Df
            self.link_status = link_status
            self.bokeh = [] # graphs in grid
            self.graphs = {} # graphs
            start = PAGE_MAX_COL * (PageStatus.current_page - 1)
            if len(Df.subcol) >= PAGE_MAX_COL * (PageStatus.current_page): # For other than the last page
                end = start + PAGE_MAX_COL
            else:
                end = start + len(Df.subcol) % PAGE_MAX_COL # For the other pages
            ### Checkpoint ###
            print(MESSAGES["init_checkpoint1"] % (str(end-start)))
            ### Checkpoint ###
            for key in range(start, end):
                dtype = Df.dtypes[key]
                sr=Df.df.iloc[:,Df.subcol[key]]
                self.graphs[key] = Widgets()
                for i in range(len(DTYPE_LIST)):
                    if dtype == DTYPE_LIST[i]:
                        ### Checkpoint ###
                        print(MESSAGES["init_checkpoint2"] % (DTYPE_LIST[i], str(key)))
                        ### Checkpoint ###
                        for widget in DTYPE_VS_WIDGETS_DEFINITION[i]:
                            ### Checkpoint ###
                            print(MESSAGES["init_checkpoint3"] % (widget))
                            ### Checkpoint ###
                            if i == 2:
                                sr.replace(np.nan, "NaN", inplace=True)
                            self.graphs[key].add_widget(widget, Df, sr, key, self)
                        self.bokeh.extend([[self.graphs[key].widgets[widget].bokeh for widget in row] for row in DTYPE_VS_WIDGETS_STRUCT_DEFINITION[i]])
        except:
            ### Checkpoint ###
            print(MESSAGES["init_error"])
            ### Checkpoint ###
            self.bokeh = [] # graphs in grid
            self.graphs = {} # graphs
            
    def diffuse(self, key):
        ### Checkpoint ###
        print(MESSAGES["diffuse_start"])
        ### Checkpoint ###
        if self.link_status.link_status == 1:
            for widgets in self.graphs.values():
                for widget in widgets.widgets.values():
                    print(MESSAGES["subwidget"] % (widget))
                    widget.adjust()
        else:
            for widget in self.graphs[key].widgets.values():
                print(MESSAGES["subwidget"] % (widget))
                widget.adjust()
        self.Df.updateStatus = []
        self.Df.bokeh_selected_records.text = WPROP_SELECTED_RECORDS["text"] % (str(len(self.Df.subrow_Manual)))

