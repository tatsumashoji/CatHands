#!/usr/bin/env python
# -*- coding: utf-8 -*-


#========================================
#  Libraries
#========================================
from bokeh.models.widgets import Tabs
from bokeh.models import Panel
from bokeh.io import curdoc
from bokeh.layouts import layout
# Modules
from scripts.DataFrame import DataFrame
from scripts.Uploader import UploaderHeader, Uploader, LoadFile, LoadFileHeader
from scripts.Graphs import Graphs
from scripts.PageStatus import PageStatus
from scripts.Download import Download
from scripts.Reset import Reset
from scripts.Status import Status, Page


#========================================
# Parameters
#========================================
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
WN_TABS = "tabs"
WID_TABS = "tabs"


#========================================
# main()
#========================================
page = Page()
# DataFrame
df = DataFrame()
# Uploader
uploader_header = UploaderHeader()
uploader = Uploader(df, page, uploader_header)
loadfile_header = LoadFileHeader()
loadfile = LoadFile(df, uploader)
files_panel = Panel(
    name=WN_FILES_PANEL,
    id=WID_FILES_PANEL,
    child=layout([[uploader_header.bokeh]]+[[uploader.bokeh]]+[[loadfile_header.bokeh]]+loadfile.bokeh_user_file_lists),
    title=WPROP_FILES_PANEL["title"]
)
page.add_panel(files_panel, WN_FILES_PANEL)

select_panel = Panel(
	name=WN_SELECT_PANEL,
	id=WID_SELECT_PANEL,
	child=layout([]),
	title=WPROP_SELECT_PANEL["title"]
)
page.add_panel(select_panel, WN_SELECT_PANEL)

###
decomp_panel = Panel(
	name=WN_DECOMP_PANEL,
	id=WID_DECOMP_PANEL,
	child=layout([]),
	title=WPROP_DECOMP_PANEL["title"]
)
page.add_panel(decomp_panel, WN_DECOMP_PANEL)
###
# Tabs
page.define_tab()
# Others
download = Download(df, uploader)
#reset = Reset()
page.add_other_comps(download.bokeh_btn)
page.add_other_comps(download.bokeh_exec)
#page.add_other_comps(reset.bokeh)
page.add_other_comps(df.bokeh_filename)
page.add_other_comps(df.bokeh_columns)
page.add_other_comps(df.bokeh_records)
page.add_other_comps(df.bokeh_selected_records)
status = Status()
page.add_other_comps(status.bokeh_name)
page.add_other_comps(status.bokeh_plan)


# curdoc
for model in curdoc().roots:
	curdoc().remove_root(model)

curdoc().add_root(page.tabs)
for bokeh in page.other_comps:
	curdoc().add_root(bokeh)

