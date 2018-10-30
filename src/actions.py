#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 19:15:35 2018

@author: mn
"""

from PyQt5.QtWidgets import QAction

from icons import Icon


class Action(QAction):
    """Base class for all actions in pyspread

    Note: Parameter order has changed comparing with QAction

    """

    def __init__(self, parent, label, *connects,
                 icon=None, shortcut=None, statustip=None, checkable=False):
        if icon is None:
            super().__init__(label, parent, checkable=checkable)
        else:
            super().__init__(icon, label, parent, checkable=checkable)

        if shortcut is not None:
            self.setShortcut(shortcut)

        if statustip is not None:
            self.setStatusTip(statustip)

        for connect in connects:
            self.triggered.connect(connect)


class MainWindowActions(dict):
    """Holds all QActions for pyspread"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self._add_file_actions()
        self._add_edit_actions()
        self._add_view_actions()
        self._add_format_actions()
        self._add_macro_actions()
        self._add_help_actions()

    def _add_file_actions(self):
        """Adds actions for File menu"""

        self["new"] = Action(self.parent, "&New", self.parent.close,
                             icon=Icon("new"),
                             shortcut='Ctrl+n',
                             statustip='Create a new, empty spreadsheet')

        self["open"] = Action(self.parent, "&Open", self.parent.close,
                              icon=Icon("open"),
                              statustip='Open spreadsheet from file')

        self["save"] = Action(self.parent, "&Save", self.parent.close,
                              icon=Icon("save"),
                              shortcut='Ctrl+s',
                              statustip='Save spreadsheet')

        self["save_as"] = Action(self.parent, "Save &As", self.parent.close,
                                 icon=Icon("save_as"),
                                 shortcut='Shift+Ctrl+s',
                                 statustip='Save spreadsheet to a new file')

        self["import"] = Action(self.parent, "&Import", self.parent.close,
                                icon=Icon("import"),
                                statustip='Import a file and paste it into '
                                          'the current grid')

        self["export"] = Action(self.parent, "&Export", self.parent.close,
                                icon=Icon("export"),
                                statustip="Export selection to a file")

        self["approve"] = Action(self.parent, "&Approve file",
                                 self.parent.close,
                                 icon=Icon("approve"),
                                 statustip='Approve, unfreeze and sign the '
                                           'current file')

        self["clear_globals"] = Action(self.parent, "&Clear globals",
                                       self.parent.close,
                                       icon=Icon("clear_globals"),
                                       statustip='Deletes global variables '
                                                 'from memory and reloads '
                                                 'base modules')

        self["page_setup"] = Action(self.parent, "Page setup",
                                    self.parent.close,
                                    icon=Icon("page_setup"),
                                    statustip='Setup printer page')

        self["print_preview"] = Action(self.parent, "Print preview",
                                       self.parent.close,
                                       icon=Icon("print_preview"),
                                       statustip='Print preview')

        self["print"] = Action(self.parent, "Print", self.parent.close,
                               icon=Icon("print"),
                               shortcut='Ctrl+p',
                               statustip='Print current spreadsheet')

        self["preferences"] = Action(self.parent, "Preferences...",
                                     self.parent.close,
                                     icon=Icon("preferences"),
                                     statustip='Pyspread setup parameters')

        self["new_gpg_key"] = Action(self.parent, "Switch GPG key...",
                                     self.parent.close,
                                     icon=Icon("new_gpg_key"),
                                     statustip='Create or choose a GPG key '
                                               'pair for signing and '
                                               'verifying pyspread files')

        self["quit"] = Action(self.parent, "&Quit", self.parent.close,
                              icon=Icon("quit"),
                              shortcut='Ctrl+Q',
                              statustip='Exit pyspread')

    def _add_edit_actions(self):
        """Adds actions for Edit menu"""

        self["undo"] = Action(self.parent, "&Undo", self.parent.close,
                              icon=Icon("undo"),
                              shortcut='Ctrl+z',
                              statustip='Undo last step')

        self["redo"] = Action(self.parent, "&Redo", self.parent.close,
                              icon=Icon("redo"),
                              shortcut='Shift+Ctrl+z',
                              statustip='Redo last undone step')

        self["cut"] = Action(self.parent, "Cut", self.parent.close,
                             icon=Icon("cut"),
                             shortcut='Ctrl+x',
                             statustip='Cut cell to the clipboard')

        self["copy"] = Action(self.parent, "&Copy", self.parent.close,
                              icon=Icon("copy"),
                              shortcut='Ctrl+c',
                              statustip='Copy the input strings of the cells '
                                        'to the clipboard')

        self["copy_results"] = Action(self.parent, "Copy results",
                                      self.parent.close,
                                      icon=Icon("copy_results"),
                                      shortcut='Shift+Ctrl+c',
                                      statustip='Copy the result strings of '
                                                'the cells to the clipboard')

        self["paste"] = Action(self.parent, "&Paste", self.parent.close,
                               icon=Icon("paste"),
                               shortcut='Ctrl+v',
                               statustip='Paste cells from the clipboard')

        self["paste_as"] = Action(self.parent, "Paste as...",
                                  self.parent.close,
                                  icon=Icon("paste_as"),
                                  shortcut='Shift+Ctrl+v',
                                  statustip='Transform clipboard and paste '
                                            'results')

        self["select_all"] = Action(self.parent, "&Select all",
                                    self.parent.close,
                                    icon=Icon("select_all"),
                                    shortcut='Ctrl+a',
                                    statustip='Select all cells')

        self["find"] = Action(self.parent, "&Find", self.parent.close,
                              icon=Icon("find"),
                              shortcut='Ctrl+f',
                              statustip='Find cell by content')

        self["replace"] = Action(self.parent, "&Replace...", self.parent.close,
                                 icon=Icon("replace"),
                                 shortcut='Shift+Ctrl+f',
                                 statustip='Replace sub-strings in cells')

        self["quote"] = Action(self.parent, "&Quote", self.parent.close,
                               icon=Icon("quote"),
                               shortcut='Ctrl+Return',
                               statustip="Convert cells' code to strings by "
                                         "addding quotes")

        self["sort_ascending"] = Action(self.parent, "Sort ascending",
                                        self.parent.close,
                                        icon=Icon("sort_ascending"),
                                        statustip='Sort selected columns (or '
                                                  'all if none selected) in '
                                                  'ascending order')

        self["sort_decending"] = Action(self.parent, "Sort descending",
                                        self.parent.close,
                                        icon=Icon("sort_descending"),
                                        statustip='Sort selected columns (or '
                                                  'all if none selected) in '
                                                  'descending order')

        self["insert_rows"] = Action(self.parent, "Insert rows",
                                     self.parent.close,
                                     icon=Icon("insert_row"),
                                     statustip='Insert max(1, no. selected '
                                               'rows) rows at cursor')

        self["insert_columns"] = Action(self.parent, "Insert columns",
                                        self.parent.close,
                                        icon=Icon("insert_column"),
                                        statustip='Insert max(1, no. selected '
                                                  'columns) columns at cursor')

        self["insert_table"] = Action(self.parent, "Insert table",
                                      self.parent.close,
                                      icon=Icon("insert_table"),
                                      statustip='Insert table before current '
                                                'table')

        self["delete_rows"] = Action(self.parent, "Delete rows",
                                     self.parent.close,
                                     icon=Icon("delete_row"),
                                     statustip='Delete max(1, no. selected '
                                               'rows) rows at cursor')

        self["delete_columns"] = Action(self.parent, "Delete columns",
                                        self.parent.close,
                                        icon=Icon("delete_column"),
                                        statustip='Delete max(1, no. selected '
                                                  'columns) columns at cursor')

        self["delete_table"] = Action(self.parent, "Delete table",
                                      self.parent.close,
                                      icon=Icon("delete_table"),
                                      statustip='Delete current table')

        self["resize_grid"] = Action(self.parent, "Resize grid",
                                     self.parent.close,
                                     icon=Icon("resize_grid"),
                                     statustip='Resizes the current grid')

    def _add_view_actions(self):
        """Adds actions for View menu"""

        self["fullscreen"] = Action(self.parent, "Fullscreen",
                                    self.parent.close,
                                    icon=Icon("fullscreen"),
                                    shortcut='F11',
                                    statustip='Show grid in fullscreen mode '
                                              '(press <F11> to leave)')

        self["toggle_main_toolbar"] = Action(self.parent, "Main toolbar",
                                             self.parent.close,
                                             checkable=True,
                                             statustip='Show/hide the main '
                                                       'toolbar')

        self["toggle_macro_toolbar"] = Action(self.parent, "Macro toolbar",
                                              self.parent.close,
                                              checkable=True,
                                              statustip='Show/hide the macro '
                                                        'toolbar')

        self["toggle_widget_toolbar"] = Action(self.parent, "Widget toolbar",
                                               self.parent.close,
                                               checkable=True,
                                               statustip='Show/hide the '
                                                         'widget toolbar')

        self["toggle_format_toolbar"] = Action(self.parent, "Format toolbar",
                                               self.parent.close,
                                               checkable=True,
                                               statustip='Show/hide the '
                                                         'format toolbar')

        self["toggle_find_toolbar"] = Action(self.parent, "Find toolbar",
                                             self.parent.close,
                                             checkable=True,
                                             statustip='Show/hide the find '
                                                       'toolbar')

        self["toggle_entryline"] = Action(self.parent, "Entry line",
                                          self.parent.close,
                                          checkable=True,
                                          statustip='Show/hide the entry line')

        self["toggle_tablelist"] = Action(self.parent, "Table list",
                                          self.parent.close,
                                          checkable=True,
                                          statustip='Show/hide the table list')

        self["toggle_macropanel"] = Action(self.parent, "Macro panel",
                                           self.parent.close,
                                           checkable=True,
                                           statustip='Show/hide the macro '
                                                     'panel')

        self["goto_cell"] = Action(self.parent, "Go to cell",
                                   self.parent.close,
                                   icon=Icon("goto_cell"),
                                   shortcut='Ctrl+g',
                                   statustip='Select a cell and put it into '
                                             'view')

        self["check_spelling"] = Action(self.parent, "Check spelling",
                                        self.parent.nothing,
                                        icon=Icon("check_spelling"),
                                        checkable=True,
                                        statustip='Turn spell checker on/off')

        self["zoom_in"] = Action(self.parent, "Zoom in", self.parent.close,
                                 icon=Icon("zoom_in"),
                                 shortcut='Ctrl++',
                                 statustip='Zoom in the grid')

        self["zoom_out"] = Action(self.parent, "Zoom out", self.parent.close,
                                  icon=Icon("zoom_out"),
                                  shortcut='Ctrl+-',
                                  statustip='Zoom out the grid')

        self["zoom_1"] = Action(self.parent, "Original size",
                                self.parent.close,
                                icon=Icon("zoom_1"),
                                shortcut='Ctrl+0',
                                statustip='Show grid on standard zoom level')

        self["zoom_fit"] = Action(self.parent, "Zoom to fit",
                                  self.parent.close,
                                  icon=Icon("zoom_fit"),
                                  shortcut='F6',
                                  statustip='Zooms the grid so that it fits '
                                            'into the window')

        self["refresh_cells"] = Action(self.parent, "Refresh selected cells",
                                       self.parent.close,
                                       icon=Icon("refresh"),
                                       shortcut='F5',
                                       statustip='Refresh selected cells even '
                                                 'when frozen')

        self["toggle_periodic_updates"] = \
            Action(self.parent, "Toggle periodic updates", self.parent.nothing,
                   icon=Icon("toggle_periodic_updates"),
                   checkable=True,
                   statustip='Toggles periodic updates for frozen cells')

        self["show_frozen"] = Action(self.parent, "Show frozen",
                                     self.parent.nothing,
                                     icon=Icon("show_frozen"),
                                     checkable=True,
                                     statustip='Indicates frozen cells with a '
                                               'background crosshatch')

    def _add_format_actions(self):
        """Adds actions for Format menu"""

        self["copy_format"] = Action(self.parent, "&Copy format",
                                     self.parent.close,
                                     icon=Icon("copy_format"),
                                     shortcut='Alt+Ctrl+c',
                                     statustip='Copy format of selection to '
                                               'the clipboard')

        self["paste_format"] = Action(self.parent, "&Paste format",
                                      self.parent.close,
                                      icon=Icon("paste_format"),
                                      shortcut='Alt+Ctrl+v',
                                      statustip='Apply format from the '
                                                'clipboard to the selected '
                                                'cells')

        self["font"] = Action(self.parent, "&Font...", self.parent.close,
                              icon=Icon("font_dialog"),
                              shortcut='Ctrl+n',
                              statustip='Lauch font dialog')

        self["bold"] = Action(self.parent, "&Bold", self.parent.close,
                              icon=Icon("bold"),
                              shortcut='Ctrl+b',
                              statustip='Toggle bold font weight for the '
                                        'selected cells')

        self["italics"] = Action(self.parent, "&Italics", self.parent.close,
                                 icon=Icon("italics"),
                                 shortcut='Ctrl+i',
                                 statustip='Toggle italics font style for the '
                                           'selected cells')

        self["underline"] = Action(self.parent, "&Underline",
                                   self.parent.close,
                                   icon=Icon("underline"),
                                   shortcut='Ctrl+u',
                                   statustip='Toggle underline for the '
                                             'selected cells')

        self["strikethrough"] = Action(self.parent, "&Strikethrough",
                                       self.parent.close,
                                       icon=Icon("strikethrough"),
                                       statustip='Toggle strikethrough for '
                                                 'the selected cells')

        self["markup"] = Action(self.parent, "Markup", self.parent.close,
                                icon=Icon("markup"),
                                statustip='Show cell results as markup '
                                          '(allows partly formatted output)')

        self["text_color"] = Action(self.parent, "Text color...",
                                    self.parent.close,
                                    icon=Icon("text_color"),
                                    statustip='Lauch text color dialog')

        self["background_color"] = Action(self.parent, "Background color...",
                                          self.parent.close,
                                          icon=Icon("background_color"),
                                          statustip='Lauch background color '
                                                    'dialog')

        self["justify_left"] = Action(self.parent, "Left", self.parent.close,
                                      icon=Icon("justify_left"),
                                      statustip='Display cell result text '
                                                'left justified')

        self["justify_center"] = Action(self.parent, "Center",
                                        self.parent.close,
                                        icon=Icon("justify_center"),
                                        statustip='Display cell result text '
                                                  'centered')

        self["justify_right"] = Action(self.parent, "Right", self.parent.close,
                                       icon=Icon("justify_right"),
                                       statustip='Display cell result text '
                                                 'right justified')

        self["align_top"] = Action(self.parent, "Top", self.parent.close,
                                   icon=Icon("align_top"),
                                   statustip='Align cell result at the top of '
                                             'the cell')

        self["align_center"] = Action(self.parent, "Center", self.parent.close,
                                      icon=Icon("align_center"),
                                      statustip='Center cell result within '
                                                'the cell')

        self["align_bottom"] = Action(self.parent, "Bottom", self.parent.close,
                                      icon=Icon("align_bottom"),
                                      statustip='Align cell result at the '
                                                'bottom of the cell')

        self["rotate_0"] = Action(self.parent, "0°", self.parent.close,
                                  icon=Icon("rotate_0"),
                                  statustip='Set text rotation to 0°')

        self["rotate_90"] = Action(self.parent, "90°", self.parent.close,
                                   icon=Icon("rotate_90"),
                                   statustip='Set text rotation to 90°')

        self["rotate_180"] = Action(self.parent, "180°", self.parent.close,
                                    icon=Icon("rotate_180"),
                                    statustip='Set text rotation to 180°')

        self["rotate_270"] = Action(self.parent, "270°", self.parent.close,
                                    icon=Icon("rotate_270"),
                                    statustip='Set text rotation to 270°')

        self["freeze_cell"] = Action(self.parent, "Freeze cell",
                                     self.parent.close,
                                     icon=Icon("freeze"),
                                     statustip='Freeze the selected cell so '
                                               'that is is only updated when '
                                               '<F5> is pressed')

        self["lock_cell"] = Action(self.parent, "Lock cell", self.parent.close,
                                   icon=Icon("lock"),
                                   statustip='Lock cell so that its code '
                                             'cannot be changed')

        self["merge_cells"] = Action(self.parent, "Merge cells",
                                     self.parent.close,
                                     icon=Icon("merge_cells"),
                                     statustip='Merge/unmerge selected cells')

    def _add_macro_actions(self):
        """Adds actions for Macro menu"""

        self["load_macros"] = Action(self.parent, "Load macros",
                                     self.parent.close,
                                     icon=Icon("load_macros"),
                                     statustip='Load macros from an external '
                                               'Python file')

        self["save_macros"] = Action(self.parent, "Save macros",
                                     self.parent.close,
                                     icon=Icon("save_macros"),
                                     statustip='Save macros to an external '
                                               'Python file')

        self["insert_image"] = Action(self.parent, "Insert image...",
                                      self.parent.close,
                                      icon=Icon("insert_image"),
                                      statustip='Load an image from a file '
                                                'into a cell')

        self["link_image"] = Action(self.parent, "Link image...",
                                    self.parent.close,
                                    icon=Icon("link_image"),
                                    statustip='Link an image file from a cell')

        self["insert_chart"] = Action(self.parent, "Insert chart...",
                                      self.parent.close,
                                      icon=Icon("insert_chart"),
                                      statustip='Create a matplotlib chart '
                                                'and insert code so that it '
                                                'is displayed')

    def _add_help_actions(self):
        """Adds actions for Help menu"""

        self["first_steps"] = Action(self.parent, "First steps...",
                                     self.parent.close,
                                     icon=Icon("help"),
                                     shortcut='F1',
                                     statustip='Display the first steps '
                                               'document that provides a '
                                               'basic overview of pyspread')

        self["tutorial"] = Action(self.parent, "Tutorial...",
                                  self.parent.close,
                                  icon=Icon("tutorial"),
                                  statustip='Display a pyspread tutorial')

        self["faq"] = Action(self.parent, "FAQ...", self.parent.close,
                             icon=Icon("faq"),
                             statustip='Display frequently asked questions')

        self["dependencies"] = Action(self.parent, "Dependencies...",
                                      self.parent.close,
                                      icon=Icon("dependencies"),
                                      statustip='Overview of installed '
                                                'dependencies')

        self["about"] = Action(self.parent, "About pyspread...",
                               self.parent.close,
                               icon=Icon("pyspread"),
                               statustip='About pyspread')