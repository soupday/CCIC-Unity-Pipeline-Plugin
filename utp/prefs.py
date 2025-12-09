# Copyright (C) 2025 Victor Soupday
# This file is part of CC/iC-Unity-Pipeline-Plugin <https://github.com/soupday/CCiC-Unity-Pipeline-Plugin>
#
# CC/iC-Unity-Pipeline-Plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CC/iC-Unity-Pipeline-Plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CC/iC-Unity-Pipeline-Plugin.  If not, see <https://www.gnu.org/licenses/>.

import os
import RLPy
import json
import os
import gzip
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import os, json
from . import vars, utils, cc, qt, options


PREFERENCES: 'Preferences' = None

def get_preferences():
    global PREFERENCES
    if not PREFERENCES:
        PREFERENCES = Preferences()
    return PREFERENCES


class Preferences(QObject):
    window: RLPy.RIDockWidget = None

    def __init__(self):
        QObject.__init__(self)
        self.create_window()

    def show(self):
        self.window.Show()

    def hide(self):
        self.window.Hide()

    def is_shown(self):
        return self.window.IsVisible()

    def create_window(self):
        OPTS = options.get_opts()

        W = 500
        H = 400
        self.window, layout = qt.window(f"Unity Pipeline Plug-in Preferences",
                                        width=W, height=H, fixed=True,
                                        show_hide=self.on_show_hide)
        self.window.SetFeatures(RLPy.EDockWidgetFeatures_Closable)

        qt.spacing(layout, 10)

        # title
        grid = qt.grid(layout)
        qt.label(grid, f"DataLink Settings:", style=qt.STYLE_RL_BOLD, row=0, col=0)
        qt.label(grid, f"Version {vars.VERSION}  ", style=qt.STYLE_VERSION, row=0, col=1, align=Qt.AlignVCenter | Qt.AlignRight)
        qt.button(grid, "Detect", func=self.detect_settings, height=26, width=64, row=0, col=2)

        # DataLink folder
        qt.label(grid, "Local DataLink Folder", row=1, col=0)
        qt.DTextBox(self, grid, OPTS, "DATALINK_FOLDER", row=1, col=1, update=self.write_options)
        qt.button(grid, "Find", func=self.browse_datalink_folder, height=26, width=64, row=1, col=2)

        qt.spacing(layout, 10)

        col = qt.column(layout)
        qt.DCheckBox(self, col, "Auto-start Link Server", OPTS, "AUTO_START_SERVICE", update=self.write_options)
        qt.DCheckBox(self, col, "Match Client Rate", OPTS, "MATCH_CLIENT_RATE", update=self.write_options)
        #qt.DCheckBox(self, col, "Sequence Frame Sync", OPTS, "DATALINK_FRAME_SYNC", update=self.update_options)

        qt.spacing(layout, 10)
        qt.separator(layout, 1)
        qt.spacing(layout, 4)

        # Export Morph Materials
        grid = qt.grid(layout)
        grid.setColumnStretch(1, 2)

        qt.label(grid, "DataLink Send Settings:", style=qt.STYLE_RL_BOLD,
                 row=0, col=0, col_span=2)

        if cc.is_cc():

            qt.label(grid, "Export Frame Rate:", style=qt.STYLE_NONE, row=1, col=0)
            qt.DComboBox(self, grid, OPTS, "CC_EXPORT_FPS",
                               options=[(0, "Project fps"), (12, "12 fps"), (24, "24 fps (Film)"), (25, "25 fps (PAL)"), (30, "30 fps (NTSC)"), ((60, "60 fps"))],
                               numeric=True, min=1, max=120, suffix="fps",
                               row=1, col=1, update=self.write_options)

            qt.label(grid, "Export With:", style=qt.STYLE_NONE, row=2, col=0)
            qt.DComboBox(self, grid, OPTS, "CC_EXPORT_MODE",
                               options=["No Animation", "Current Pose", "Animation"],
                               row=2, col=1, update=self.write_options)

            qt.label(grid, "Max SubD-Level:", style=qt.STYLE_NONE, row=3, col=0)
            qt.DComboBox(self, grid, OPTS, "CC_EXPORT_MAX_SUB_LEVEL",
                               options=[[-1, "Current"], [0, "SubD 0"], [1, "SubD 1"], [2, "SubD 2"]],
                               row=3, col=1, update=self.write_options)

            qt.DCheckBox(self, grid, "Delete Hidden Faces", OPTS, "CC_DELETE_HIDDEN_FACES",
                               row=7, col=0, col_span=2, update=self.write_options)
            qt.DCheckBox(self, grid, "Bake Textures", OPTS, "CC_BAKE_TEXTURES",
                               row=8, col=0, col_span=2, update=self.write_options)

        else:

            qt.label(grid, "Export Frame Rate:", style=qt.STYLE_NONE, row=1, col=0)
            qt.DComboBox(self, grid, OPTS, "IC_EXPORT_FPS",
                               options=[(0, "Project fps"), (12, "12 fps"), (24, "24 fps (Film)"), (25, "25 fps (PAL)"), (30, "30 fps (NTSC)"), ((60, "60 fps (iClone)"))],
                               numeric=True, min=1, max=120, suffix="fps",
                               row=1, col=1, update=self.write_options)

            qt.label(grid, "Export With:", style=qt.STYLE_NONE, row=2, col=0)
            qt.DComboBox(self, grid, OPTS, "IC_EXPORT_MODE",
                               options=["No Animation", "Current Pose", "Animation"],
                               row=2, col=1, update=self.write_options)

            qt.label(grid, "Max SubD-Level:", style=qt.STYLE_NONE, row=3, col=0)
            qt.DComboBox(self, grid, OPTS, "IC_EXPORT_MAX_SUB_LEVEL",
                               options=[[-1, "Current"], [0, "SubD 0"], [1, "SubD 1"], [2, "SubD 2"]],
                               row=3, col=1, update=self.write_options)

            qt.DCheckBox(self, grid, "Delete Hidden Faces", OPTS, "IC_DELETE_HIDDEN_FACES",
                               row=4, col=0, col_span=2, update=self.write_options)
            qt.DCheckBox(self, grid, "Bake Textures", OPTS, "IC_BAKE_TEXTURES",
                               row=5, col=0, col_span=2, update=self.write_options)

        qt.spacing(layout, 10)
        qt.stretch(layout, 1)

    def refresh_ui(self):
        OPTS = options.get_opts()

        textbox_export_path = qt.find_dcontrol(self, OPTS, "DATALINK_FOLDER")
        combo_cc_export_max_sub_level = qt.find_dcontrol(self, OPTS, "CC_EXPORT_MAX_SUB_LEVEL")
        combo_ic_export_max_sub_level = qt.find_dcontrol(self, OPTS, "IC_EXPORT_MAX_SUB_LEVEL")
        combo_cc_export_mode = qt.find_dcontrol(self, OPTS, "CC_EXPORT_MODE")
        combo_ic_export_mode = qt.find_dcontrol(self, OPTS, "IC_EXPORT_MODE")
        if textbox_export_path:
            textbox_export_path.update_value()
        if combo_cc_export_max_sub_level:
            combo_cc_export_max_sub_level.update_value()
        if combo_ic_export_max_sub_level:
            combo_ic_export_max_sub_level.update_value()
        if combo_cc_export_mode:
            combo_cc_export_mode.update_value()
        if combo_ic_export_mode:
            combo_ic_export_mode.update_value()

    def on_show_hide(self, visible):
        if visible:
            qt.toggle_toolbar_action("Unity Pipeline Toolbar", "Unity Pipeline Settings", True)
            self.refresh_ui()
        else:
            qt.toggle_toolbar_action("Unity Pipeline Toolbar", "Unity Pipeline Settings", False)

    def write_options(self):
        OPTS = options.get_opts()
        OPTS.write_state()

    def detect_settings(self):
        OPTS = options.get_opts()

        # if datalink path is invalid, generate a new one
        if not check_datalink_path()[0]:
            OPTS.DATALINK_FOLDER = ""
        detect_paths()
        textbox_export_path = qt.find_dcontrol(self, OPTS, "DATALINK_FOLDER")
        textbox_export_path.update_value()


    def browse_datalink_folder(self):
        OPTS = options.get_opts()

        if OPTS.DATALINK_FOLDER:
            folder_path = qt.browse_folder("Datalink Folder", OPTS.DATALINK_FOLDER)
        else:
            folder_path = qt.browse_folder("Datalink Folder")
        if os.path.exists(folder_path):
            textbox_export_path = qt.find_dcontrol(self, OPTS, "DATALINK_FOLDER")
            textbox_export_path.set_value(folder_path)
            OPTS.write_state()



def detect_paths():
    OPTS = options.get_opts()

    utils.log_info("Reading settings...")
    OPTS.read_state()

    changed = False

    if OPTS.DATALINK_FOLDER:
        if not os.path.exists(OPTS.DATALINK_FOLDER):
            try:
                os.makedirs(OPTS.DATALINK_FOLDER, exist_ok=True)
            except:
                utils.log_warn(f"DataLink folder: {OPTS.DATALINK_FOLDER} invalid! Using default.")
                OPTS.DATALINK_FOLDER = ""

    if not OPTS.DATALINK_FOLDER:
        path = cc.user_files_path("DataLink", create=True)
        OPTS.DATALINK_FOLDER = path
        changed = True

    if changed:
        utils.log_info(f"Writing updated settings...")
        OPTS.write_state()

    utils.log_info(f"Using Datalink Folder: {OPTS.DATALINK_FOLDER}")


def check_datalink_path(report=None, create=False, warn=False):
    OPTS = options.get_opts()

    if not report:
        report = ""

    valid = True
    write = False

    # correct old datalink folder default path (or any CC/iC temp files path)
    if utils.contains_path(OPTS.DATALINK_FOLDER, cc.temp_files_path()):
        OPTS.DATALINK_FOLDER = cc.user_files_path("DataLink", create=True)
        utils.log_info(f"Using corrected default DataLink path: {OPTS.DATALINK_FOLDER}")
        write = True

    # if empty use user documents folder
    if not OPTS.DATALINK_FOLDER:
        OPTS.DATALINK_FOLDER = cc.user_files_path("DataLink", create=True)
        utils.log_info(f"Using default DataLink path: {OPTS.DATALINK_FOLDER}")
        write = True

    if OPTS.DATALINK_FOLDER:
        if os.path.exists(OPTS.DATALINK_FOLDER):
            # if exists but not a folder, reset to user documents
            if not os.path.isdir(OPTS.DATALINK_FOLDER):
                report += "Datalink path is not a folder!\n"
                utils.log_warn(f"DataLink path: {OPTS.DATALINK_FOLDER} is not a folder!")
                OPTS.DATALINK_FOLDER = cc.user_files_path("DataLink", create=True)
                utils.log_info(f"Using default DataLink path: {OPTS.DATALINK_FOLDER}")
                write = True
        elif create:
            try:
                os.makedirs(OPTS.DATALINK_FOLDER, exist_ok=True)
                utils.log_info(f"DataLink path: {OPTS.DATALINK_FOLDER} created!")
            except:
                # the datalink path can't be made, reset to user documents
                utils.log_warn(f"DataLink path: {OPTS.DATALINK_FOLDER} is not valid, unable to create path!")
                OPTS.DATALINK_FOLDER = cc.user_files_path("DataLink", create=True)
                utils.log_info(f"Using default DataLink path: {OPTS.DATALINK_FOLDER}")
                write = True

    if valid and write:
        OPTS.write_state()

    if warn and not valid:
        report += "\n\nPlease check plugin datalink path settings."
        qt.message_box("Path Error", report)

    return valid, report


def check_paths(quiet=False, create=False):
    report = ""
    valid = True

    valid, report = check_datalink_path(report=report, create=create)

    if not quiet and not valid:
        report += "\n\nPlease check plugin path settings."
        qt.message_box("Path Error", report)

    return valid


def export_animation():
    OPTS = options.get_opts()

    if cc.is_cc() and OPTS.CC_EXPORT_MODE == "Animation":
        return True
    if cc.is_iclone() and OPTS.IC_EXPORT_MODE == "Animation":
        return True
    return False