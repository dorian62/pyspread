#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Martin Manns
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
test_xls
========

Unit tests for xls.py

"""


import bz2
import os
import sys

import xlrd
import xlwt

import wx
app = wx.App()

TESTPATH = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-1]) + os.sep
sys.path.insert(0, TESTPATH)
sys.path.insert(0, TESTPATH + (os.sep + os.pardir) * 3)
sys.path.insert(0, TESTPATH + (os.sep + os.pardir) * 2)

from src.interfaces.xls import Xls
from src.lib.selection import Selection
from src.lib.testlib import params, pytest_generate_tests
from src.model.model import CodeArray


class TestXls(object):
    """Unit tests for Xls"""

    def setup_method(self, method):
        """Creates Xls class with code_array and temporary test.xls file"""

        # All data structures are initially empty
        # The test file xls_file has entries in each category

        self.top_window = wx.Frame(None, -1)
        wx.GetApp().SetTopWindow(self.top_window)

        self.code_array = CodeArray((1000, 100, 3))
        self.xls_infile = xlrd.open_workbook(TESTPATH + "xls_test1.xls",
                                             formatting_info=True)
        self.xls_outfile_path = TESTPATH + "xls_test2.xls"
        self.xls_in = Xls(self.code_array, self.xls_infile)

    def write_xls_out(self, xls, workbook, method_name, *args, **kwargs):
        """Helper that writes an xls file"""

        method = getattr(xls, method_name)
        method(*args, **kwargs)
        workbook.save(self.xls_outfile_path)

    def read_xls_out(self):
        """Returns string of xls_out content and removes xls_out"""

        out_workbook = xlrd.open_workbook(self.xls_outfile_path,
                                          formatting_info=True)

        # Clean up the test dir
        os.remove(self.xls_outfile_path)

        return out_workbook

    param_idx2colour = [
        {'idx': 0, 'res': (0, 0, 0)},
        {'idx': 1, 'res': (255, 255, 255)},
        {'idx': 2, 'res': (255, 0, 0)},
        {'idx': 3, 'res': (0, 255, 0)},
    ]

    @params(param_idx2colour)
    def test_idx2colour(self, idx, res):
        """Test idx2colour method"""

        assert self.xls_in.idx2colour(idx).Get() == res

    param_color2idx = [
        {'red': 0, 'green': 0, 'blue': 0, 'res': 0},
        {'red': 255, 'green': 255, 'blue': 255, 'res': 1},
        {'red': 255, 'green': 255, 'blue': 254, 'res': 1},
        {'red': 51, 'green': 52, 'blue': 51, 'res': 63},
    ]

    @params(param_color2idx)
    def test_color2idx(self, red, green, blue, res):
        """Test color2idx method"""

        assert self.xls_in.color2idx(red, green, blue) == res

    param_shape2xls = [
        {'tabs': 1, 'res': 1},
        {'tabs': 2, 'res': 2},
        {'tabs': 100, 'res': 100},
        {'tabs': 100000, 'res': 256},
    ]

    @params(param_shape2xls)
    def test_shape2xls(self, tabs, res):
        """Test _shape2xls method"""

        self.code_array.dict_grid.shape = (99, 99, tabs)
        workbook = xlwt.Workbook()
        xls_out = Xls(self.code_array, workbook)
        self.write_xls_out(xls_out, workbook, "_shape2xls", [])
        workbook = self.read_xls_out()
        assert len(workbook.sheets()) == res

    def test_xls2shape(self):
        """Test _xls2shape method"""

        self.xls_in._xls2shape()
        assert self.code_array.dict_grid.shape == (11, 7, 3)

    param_code2xls = [
        {'code': [((0, 0, 0), "Test"), ], 'key': (0, 0, 0), 'val': "Test"},
        {'code': [((10, 1, 1), "Test"), ], 'key': (10, 1, 1), 'val': "Test"},
        {'code': [((1, 1, 0), "Test"), ], 'key': (0, 0, 0), 'val': ""},
    ]

    @params(param_code2xls)
    def test_code2xls(self, key, val, code):
        """Test _code2xls method"""

        row, col, tab = key

        for __key, __val in code:
            self.code_array[__key] = __val
            self.code_array.shape = (1000, 100, 3)
        wb = xlwt.Workbook()
        xls_out = Xls(self.code_array, wb)
        worksheets = []
        xls_out._shape2xls(worksheets)
        self.write_xls_out(xls_out, wb, "_code2xls", worksheets)
        workbook = self.read_xls_out()

        worksheets = workbook.sheets()
        worksheet = worksheets[tab]
        assert worksheet.cell_value(row, col) == val

    param_xls2code = [
        {'key': (5, 2, 0), 'res': "34.234"},
        {'key': (6, 2, 0), 'res': "2.0"},
        {'key': (3, 4, 0), 'res': "Hi"},
    ]

    @params(param_xls2code)
    def test_xls2code(self, key, res):
        """Test _xls2code method"""

        worksheets = self.xls_in.workbook.sheet_names()

        for tab, worksheet_name in enumerate(worksheets):
            worksheet = self.xls_in.workbook.sheet_by_name(worksheet_name)
            self.xls_in._xls2code(worksheet, tab)

        assert self.xls_in.code_array(key) == res

#    param_attributes2xls = [
#        {'code': "[]\t[]\t[]\t[]\t[(3, 4)]\t0\t'borderwidth_bottom'\t42\n",
#         'selection': Selection([], [], [], [], [(3, 4)]), 'table': 0,
#         'key': (3, 4, 0), 'attr': 'borderwidth_bottom', 'val': 42},
#    ]
#
#    param_get_font = [
#        {'code': "0\t0\t0\tTest\n", 'key': (0, 0, 0), 'val': "Test"},
#        {'code': "10\t0\t0\t" + u"öäüß".encode("utf-8") + "\n",
#         'key': (10, 0, 0), 'val': u"öäüß"},
#        {'code': "2\t0\t0\tTest\n", 'key': (2, 0, 0), 'val': "Test"},
#        {'code': "2\t0\t0\t" + "a" * 100 + '\n', 'key': (2, 0, 0),
#         'val': "a" * 100},
#        {'code': '0\t0\t0\t"Test"\n', 'key': (0, 0, 0), 'val': '"Test"'},
#    ]
#
#    @params(param_get_font)
#    def test_get_font(self, key, val, code):
#        """Test _get_font method"""
#
#        self.code_array[key] = val
#        self.write_xls_out("_code2xls")
#        res = self.read_xls_out()
#
#        assert res == code
#
#    param_get_alignment = [
#        {'code': "0\t0\t0\tTest\n", 'key': (0, 0, 0), 'val': "Test"},
#        {'code': "10\t0\t0\t" + u"öäüß".encode("utf-8") + "\n",
#         'key': (10, 0, 0), 'val': u"öäüß"},
#        {'code': "2\t0\t0\tTest\n", 'key': (2, 0, 0), 'val': "Test"},
#        {'code': "2\t0\t0\t" + "a" * 100 + '\n', 'key': (2, 0, 0),
#         'val': "a" * 100},
#        {'code': '0\t0\t0\t"Test"\n', 'key': (0, 0, 0), 'val': '"Test"'},
#    ]
#
#    @params(param_get_alignment)
#    def test_get_alignment(self, key, val, code):
#        """Test _get_alignment method"""
#
#        self.code_array[key] = val
#        self.write_xls_out("_code2xls")
#        res = self.read_xls_out()
#
#        assert res == code
#
#    param_get_pattern = [
#        {'code': "0\t0\t0\tTest\n", 'key': (0, 0, 0), 'val': "Test"},
#        {'code': "10\t0\t0\t" + u"öäüß".encode("utf-8") + "\n",
#         'key': (10, 0, 0), 'val': u"öäüß"},
#        {'code': "2\t0\t0\tTest\n", 'key': (2, 0, 0), 'val': "Test"},
#        {'code': "2\t0\t0\t" + "a" * 100 + '\n', 'key': (2, 0, 0),
#         'val': "a" * 100},
#        {'code': '0\t0\t0\t"Test"\n', 'key': (0, 0, 0), 'val': '"Test"'},
#    ]
#
#    @params(param_get_pattern)
#    def test_get_pattern(self, key, val, code):
#        """Test _get_pattern method"""
#
#        self.code_array[key] = val
#        self.write_xls_out("_code2xls")
#        res = self.read_xls_out()
#
#        assert res == code
#
#    param_get_borders = [
#        {'code': "0\t0\t0\tTest\n", 'key': (0, 0, 0), 'val': "Test"},
#        {'code': "10\t0\t0\t" + u"öäüß".encode("utf-8") + "\n",
#         'key': (10, 0, 0), 'val': u"öäüß"},
#        {'code': "2\t0\t0\tTest\n", 'key': (2, 0, 0), 'val': "Test"},
#        {'code': "2\t0\t0\t" + "a" * 100 + '\n', 'key': (2, 0, 0),
#         'val': "a" * 100},
#        {'code': '0\t0\t0\t"Test"\n', 'key': (0, 0, 0), 'val': '"Test"'},
#    ]
#
#    @params(param_get_borders)
#    def test_get_borders(self, key, val, code):
#        """Test _get_borders method"""
#
#        self.code_array[key] = val
#        self.write_xls_out("_code2xls")
#        res = self.read_xls_out()
#
#        assert res == code
#
#    param_get_xfstyle = [
#        {'code': "0\t0\t0\tTest\n", 'key': (0, 0, 0), 'val': "Test"},
#        {'code': "10\t0\t0\t" + u"öäüß".encode("utf-8") + "\n",
#         'key': (10, 0, 0), 'val': u"öäüß"},
#        {'code': "2\t0\t0\tTest\n", 'key': (2, 0, 0), 'val': "Test"},
#        {'code': "2\t0\t0\t" + "a" * 100 + '\n', 'key': (2, 0, 0),
#         'val': "a" * 100},
#        {'code': '0\t0\t0\t"Test"\n', 'key': (0, 0, 0), 'val': '"Test"'},
#    ]
#
#    @params(param_get_xfstyle)
#    def test_get_xfstyle(self, key, val, code):
#        """Test _get_xfstyle method"""
#
#        self.code_array[key] = val
#        self.write_xls_out("_code2xls")
#        res = self.read_xls_out()
#
#        assert res == code
#
#    @params(param_attributes2xls)
#    def test_xls2attributes(self, selection, table, key, attr, val, code):
#        """Test _xls2attributes method"""
#
#        self.xls_in._xls2attributes(code)
#
#        attrs = self.code_array.dict_grid.cell_attributes[key]
#        assert attrs[attr] == val
#
#    param_cell_attribute_append = [
#        {'row': 0, 'tab': 0, 'height': 0.1, 'code': "0\t0\t0.1\n"},
#        {'row': 0, 'tab': 0, 'height': 0.0, 'code': "0\t0\t0.0\n"},
#        {'row': 10, 'tab': 0, 'height': 1.0, 'code': "10\t0\t1.0\n"},
#        {'row': 10, 'tab': 10, 'height': 1.0, 'code': "10\t10\t1.0\n"},
#        {'row': 10, 'tab': 10, 'height': 100.0, 'code': "10\t10\t100.0\n"},
#    ]
#
#    @params(param_cell_attribute_append)
#    def test_cell_attribute_append(self, selection, table, key, attr, val,
#                                   code):
#        """Test _cell_attribute_append method"""
#
#        self.code_array.dict_grid.cell_attributes.undoable_append(
#            (selection, table, {attr: val}), mark_unredo=False)
#
#        self.write_xls_out("_attributes2xls")
#        assert self.read_xls_out() == code
#
    param_row_heights2xls = [
        {'row': 0, 'tab': 0, 'height': 0.1, 'points': 1},
        {'row': 0, 'tab': 0, 'height': 0.0, 'points': 0},
        {'row': 10, 'tab': 0, 'height': 1.0, 'points': 14},
        {'row': 10, 'tab': 10, 'height': 1.0, 'points': 14},
        {'row': 10, 'tab': 10, 'height': 100.0, 'points': 1483},
    ]

    @params(param_row_heights2xls)
    def test_row_heights2xls(self, row, tab, height, points):
        """Test _row_heights2xls method"""

        self.code_array.shape = (1000, 100, 30)
        self.code_array.dict_grid.row_heights = {(row, tab): height}

        wb = xlwt.Workbook()
        xls_out = Xls(self.code_array, wb)
        worksheets = []
        xls_out._shape2xls(worksheets)
        self.write_xls_out(xls_out, wb, "_row_heights2xls", worksheets)
        workbook = self.read_xls_out()

        worksheets = workbook.sheets()
        worksheet = worksheets[tab]
        assert worksheet.rowinfo_map[row].height == points

    param_xls2row_heights = [
        {'row': 1, 'tab': 0, 'height': 44.500},
        {'row': 10, 'tab': 0, 'height': 45.511},
    ]

    @params(param_xls2row_heights)
    def test_xls2row_heights(self, row, tab, height):
        """Test _xls2row_heights method"""

        worksheet_names = self.xls_in.workbook.sheet_names()
        worksheet_name = worksheet_names[tab]
        worksheet = self.xls_in.workbook.sheet_by_name(worksheet_name)

        self.xls_in._xls2row_heights(worksheet, tab)
        res = self.code_array.dict_grid.row_heights[(row, tab)]
        assert round(res, 3) == height

    param_col_widths2xls = [
        {'col': 0, 'tab': 0, 'width': 0.1, 'points': 3},
        {'col': 0, 'tab': 0, 'width': 0.0, 'points': 0},
        {'col': 10, 'tab': 0, 'width': 1.0, 'points': 38},
        {'col': 10, 'tab': 10, 'width': 1.0, 'points': 38},
        {'col': 10, 'tab': 10, 'width': 100.0, 'points': 3840},
    ]

    @params(param_col_widths2xls)
    def test_col_widths2xls(self, col, tab, width, points):
        """Test _col_widths2xls method"""

        self.code_array.shape = (1000, 100, 30)
        self.code_array.dict_grid.col_widths = {(col, tab): width}

        wb = xlwt.Workbook()
        xls_out = Xls(self.code_array, wb)
        worksheets = []
        xls_out._shape2xls(worksheets)
        self.write_xls_out(xls_out, wb, "_col_widths2xls", worksheets)
        workbook = self.read_xls_out()

        worksheets = workbook.sheets()
        worksheet = worksheets[tab]
        assert worksheet.colinfo_map[col].width == points

    param_xls2col_widths = [
        {'col': 4, 'tab': 0, 'width': 130.339},
        {'col': 6, 'tab': 0, 'width': 104.661},
    ]

    @params(param_xls2col_widths)
    def test_xls2col_widths(self, col, tab, width):
        """Test _xls2col_widths method"""

        worksheet_names = self.xls_in.workbook.sheet_names()
        worksheet_name = worksheet_names[tab]
        worksheet = self.xls_in.workbook.sheet_by_name(worksheet_name)

        self.xls_in._xls2col_widths(worksheet, tab)
        res = self.code_array.dict_grid.col_widths[(col, tab)]
        assert round(res, 3) == width
#
#    def test_from_code_array(self):
#        """Test from_code_array method"""
#
#        self.xls_infile.seek(0)
#        self.xls_in.to_code_array()
#
#        outfile = bz2.BZ2File(self.xls_outfile_path, "w")
#        xls_out = Xls(self.code_array, outfile)
#        xls_out.from_code_array()
#        outfile.close()
#
#        self.xls_infile.seek(0)
#        in_data = self.xls_infile.read()
#
#        outfile = bz2.BZ2File(self.xls_outfile_path)
#        out_data = outfile.read()
#        outfile.close()
#
#        # Clean up the test dir
#        os.remove(self.xls_outfile_path)
#
#        assert in_data == out_data
#
#    def test_to_code_array(self):
#        """Test to_code_array method"""
#
#        self.xls_in.to_code_array()
#
#        assert self.code_array((0, 0, 0)) == '"Hallo"'