#!/usr/bin/env python
# -*- coding: utf-8 -*-


#========================================
#  Libraries
#========================================
# Libraries (Bokeh)
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import Panel
from bokeh.models.widgets import RadioButtonGroup, Toggle
# Modules
from scripts.Graphs import Graphs
from scripts.Decomposition import Decomposition


#========================================
# Parameters
#========================================
# Widget : PAGE_BUTTON
WN_PAGE_BUTTON = "PAGE_BUTTON"
WID_PAGE_BUTTON = "PAGE_BUTTON"
WPROP_PAGE_BUTTON = {}
WPROP_PAGE_BUTTON["width"] = 300
WPROP_PAGE_BUTTON["height"] = 50
# Num of columns per a page
PAGE_MAX_COL = 10
# Widget : LINK_BUTTON
WN_LINK_BUTTON = "LINK_BUTTON"
WID_LINK_BUTTON = "LINK_BUTTON"
WPROP_LINK_BUTTON = {}
WPROP_LINK_BUTTON["width"] = 100
WPROP_LINK_BUTTON["height"] = 50
WPROP_LINK_BUTTON["labels"] = "Sync"
WPROP_LINK_BUTTON["active"] = True
WPROP_LINK_BUTTON["button_type"] = "success"
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


#========================================
# MESSAGES
#========================================
MESSAGES = {
    "init_start" : ">> Status : PageStatus : __init__ : PageLength Calculation...",
    "init_checkpoint1" : ">> Status : PageStatus : __init__ : PageButton Generation...",
    "init_error" : ">> Status : PageStatus : __init__ : ERROR : PageButton omitted.",
    "callback_start" : ">> Status : PageStatus : callback : Next page calculation...",
    "callback_error" : ">> Status : PageStatus : callback : Lost current status. Move to 1st page.",
    "change_page_start" : ">> Status : PageStatus : change_page : Graph drawing...",
    "change_page_error" : ">> Status : PageStatus : change_page : ERROR : Unknown error during graph drawing.",
    "link_init_start" : ">> Status : LinkStatus : __init__ : Generating LinkStatus button...",
    "link_init_error" : ">> Status : LinkStatus : __init__ : Generating LinkStatus button failed.",
    "link_callback_start" : ">> Status : LinkStatus : callback : LinkStatus has changed. CurrentLinkStatus : %s"
}


#========================================
# PageButton : current_page, bokeh : callback, change_page
#========================================
class PageStatus():
    def __init__(self, Df, uploader):
        try:
            ### Checkpoint ###
            print(MESSAGES["init_start"])
            ### Checkpoint ###
            self.Df = Df
            self.uploader = uploader
            self.current_page = 0
            L = (len(Df.subcol)-1) // PAGE_MAX_COL + 1 # L : Total # of pages
            if L <= PAGE_MAX_COL - 1:
                labels = [str(p+1) for p in range(L)] # pageNumList
                active = 0 # activeNum
                self.current_page = 1 # curPage
            else:
                if int(self.current_page) <= 5:
                    labels = [str(i) for i in [1,2,3,4,5,6,7]] + [">",str(L)]
                    active = int(self.current_page)-1
                elif int(self.current_page) >= L-4:
                    labels = ["1","<"] + [str(L-i) for i in [6,5,4,3,2,1,0]]
                    active = 8-(L-int(self.current_page))
                else:
                    labels = ["1","<"] + [str(int(self.current_page)-i) for i in [2,1,0,-1,-2]] + [">",str(L)]
                    active = 4
            ### Checkpoint ###
            print(MESSAGES["init_checkpoint1"])
            ### Checkpoint ###
            self.bokeh = RadioButtonGroup(
                labels=labels,
                active=active,
                name=WN_PAGE_BUTTON,
                id=WID_PAGE_BUTTON,
                width=WPROP_PAGE_BUTTON["width"],
                height=WPROP_PAGE_BUTTON["height"]
            )
            self.bokeh.on_change('active', self.callback)
        except:
            ### Checkpoint ###
            print(MESSAGES["init_error"])
            ### Checkpoint ###
            self.current_page = 0
            self.bokeh = []

    def callback(self, attr, old, new):
        try:
            print(MESSAGES["callback_start"])
            label = self.bokeh.labels[self.bokeh.active]
            if label==">":
                self.current_page += 1
            elif label=="<":
                self.current_page -= 1
            else:
                self.current_page = int(label)
            self.change_page(self.uploader)
        except:
            print(MESSAGES["callback_error"])
            self.current_page = 0
            
    def change_page(self, uploader):
        try:
            print(MESSAGES["change_page_start"])
            #current_state = curdoc()
            link_status = LinkStatus()
            graphs = Graphs(self.Df, self, link_status)
            select = [self.bokeh].extend(graphs.bokeh)
            select_panel = Panel(
                name=WN_SELECT_PANEL,
                id=WID_SELECT_PANEL,
                child=layout([[self.bokeh, link_status.bokeh]] + graphs.bokeh),
                title=WPROP_SELECT_PANEL["title"]
            )
            decomp = Decomposition(uploader)
            decomp_panel = decomp.bokeh
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
        except:
            print(MESSAGES["change_page_error"])
            #main()
            

#========================================
# LinkButton : current_page, bokeh : callback, change_page
#========================================
class LinkStatus():
    def __init__(self):
        try:
            ### Checkpoint ###
            print(MESSAGES["link_init_start"])
            ### Checkpoint ###
            self.link_status = 1
            self.bokeh = Toggle(
                name = WN_LINK_BUTTON,
                id = WID_LINK_BUTTON,
                width = WPROP_LINK_BUTTON["width"],
                height = WPROP_LINK_BUTTON["height"],
                label = WPROP_LINK_BUTTON["labels"],
                active = WPROP_LINK_BUTTON["active"],
                button_type = WPROP_LINK_BUTTON["button_type"]
            )
            self.bokeh.on_click(self.callback)
            
        except:
            ### Checkpoint ###
            print(MESSAGES["link_init_error"])
            ### Checkpoint ###
            self.link_status = 1
            self.bokeh = []

    def callback(self, handler):
        try:
            ### Checkpoint ###
            print(MESSAGES["link_callback_start"] % (handler))
            ### Checkpoint ###
            self.link_status = 1 if handler else 0
        except:
            pass