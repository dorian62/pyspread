#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Martin Manns
# Distributed under the terms of the GNU General Public License

# --------------------------------------------------------------------
# pyspread is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyspread is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyspread.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

"""
_charts
=======

"""

import matplotlib.pyplot

import wx

# Widgets
# =======


class LineParameterPanel(wx.Panel):
    """Panel that contains widgets with line parameter choices"""

    line_styles = [ \
        ('-', "solid line style"),
        ('--', "dashed line style"),
        ('-.', "dash-dot line style"),
        (',', "dotted line style"),
        ('.', "point marker"),
        (',', "pixel marker"),
        ('o', "circle marker"),
        ('v', "triangle_down marker"),
        ('^', "triangle_up marker"),
        ('<', "triangle_left marker"),
        ('>', "triangle_right marker"),
        ('1', "tri_down marker"),
        ('2', "tri_up marker"),
        ('3', "tri_left marker"),
        ('4', "tri_right marker"),
        ('s', "square marker"),
        ('p', "pentagon marker"),
        ('*', "star marker"),
        ('h', "hexagon1 marker"),
        ('H', "hexagon2 marker"),
        ('+', "plus marker"),
        ('x', "x marker"),
        ('D', "diamond marker"),
        ('d', "thin_diamond marker"),
        ('|', "vline marker"),
        ('_', "hline marker"),
    ],

    line_parameters = [ \
        ("line_style", { \
            "type": "line_style_bitmap_combo",
            "label": "Style",
            "parameters": line_styles,
        }),
        ("color", { \
            "type": "color_choice",
            "label": "Color",
        }),
        ("alpha", { \
            "type": "slider",
            "label": "Alpha",
            "min": 0.0,
            "max": 1.0,
        }),
        ("linewidth", { \
            "type": "line_width_bitmap_combo",
            "label": "Width",
            "values": [0.0, 0.1, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0],
        }),
    ]

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.GridFlexSizer()
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.label_1 = wx.StaticText(self.panel_1, -1, "Line width", style=wx.ALIGN_CENTRE)
        self.combo_box_1 = wx.ComboBox(self.panel_1, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_3 = wx.StaticText(self.panel_1, -1, "Line style", style=wx.ALIGN_CENTRE)
        self.combo_box_2 = wx.ComboBox(self.panel_1, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_2 = wx.StaticText(self.panel_1, -1, "Line color", style=wx.ALIGN_CENTRE)
        self.button_1 = wx.Button(self.panel_1, -1, "button_1")
        self.label_4 = wx.StaticText(self.panel_1, -1, "Alpha", style=wx.ALIGN_CENTRE)
        self.slider_1 = wx.Slider(self.panel_1, -1, 0, 0, 100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        self.combo_box_1.SetMinSize((-1,-1))
        self.combo_box_2.SetMinSize((-1, -1))
        self.panel_1.SetMinSize((-1,-1))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 4, 5, 10)
        grid_sizer_1.Add(self.label_1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        grid_sizer_1.Add(self.combo_box_1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_3, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 2)
        grid_sizer_1.Add(self.combo_box_2, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_4, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 2)
        grid_sizer_1.Add(self.slider_1, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableCol(1)
        grid_sizer_1.AddGrowableCol(3)
        sizer_1.Add(self.panel_1, 1, wx.ALL | wx.EXPAND, 2)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# End of class LineEntryPanel


class LineMarkerPanel(wx.Panel):
    """Panel that contains widgets with marker parameter choices

    Markers represent points in plots e. g. with crosses or dots

    """

    marker_styles = [ \
        (7, "caretdown"),
        (4, "caretleft"),
        (5, "caretright"),
        (6, "caretup"),
        ('o', "circle"),
        ('D', "diamond"),
        ('h', "hexagon1"),
        ('H', "hexagon2"),
        ('_', "hline"),
        ('', "nothing"),
        ('8', "octagon"),
        ('p', "pentagon"),
        (',', "pixel"),
        ('+', "plus"),
        ('.', "point"),
        ('s', "square"),
        ('*', "star"),
        ('d', "thin_diamond"),
        (3, "tickdown"),
        (0, "tickleft"),
        (1, "tickright"),
        (2, "tickup"),
        ('1', "tri_down"),
        ('3', "tri_left"),
        ('4', "tri_right"),
        ('2', "tri_up"),
        ('v', "triangle_down"),
        ('<', "triangle_left"),
        ('>', "triangle_right"),
        ('^', "triangle_up"),
        ('|', "vline"),
        ('x', "x"),
    ],

    marker_parameters = [ \
        ("marker", { \
            "type": "marker_style_bitmap_combo",
            "label": "Style",
            "choices": marker_styles,
        }),
        ("markeredgecolor", { \
            "type": "color_choice",
            "label": "Marker edge color"
        }),
        ("markeredgewidth", { \
            "type": "line_width_bitmap_combo",
            "label": "Edge width",
            "values": [0.0, 0.1, 0.2, 0.5, 1.0, 2.0],
        }),
        ("markerfacecolor", { \
            "type": "color_choice",
            "label": "Marker face color"
        }),
        ("markerfacecoloralt", { \
            "type": "color_choice",
            "label": "Marker face color 2",
        }),
        ("markersize", { \
            "type": "slider",
            "label": "Marker size",
            "min": 0.0,
            "max": 10.0,
        }),
    ]




#xy_plot_parameters = [ \
#    ("line", { \
#        "type": "line",
#        "label": "Line",
#        "parameters": line_parameters,
#    }),
#    ("marker", { \
#        "type": "marker",
#        "label": "Marker",
#        "parameters": marker_parameters,
#    }),
#]

#hist_parameters = [ \
#    ("bins", { \
#        "type": "integer|list",
#        "label": "Number of histogram bins",
#    }),
#    ("color", { \
#        "type": "color_choice",
#        "label": "Line color"
#    }),
#]

#charts = [ \
#    ("xy_plot", { \
#        "command": matplotlib.pyplot.plot,
#        "label": "XY plot",
#        "dim": 2,
#        "multiplot": True,
#        "parameters": xy_plot_parameters,
#    }),
#    ("histogram", { \
#        "command": matplotlib.pyplot.hist,
#        "label": "1D histogram",
#        "dim": 1,
#        "multiplot": False,
#        "parameters": hist_parameters,
#    }),
#]

# Widgets
# =======



# Line style

# Line width

# Line color