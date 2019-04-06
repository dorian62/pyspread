#!/usr/bin/env python3
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


def get_enchant_version():
    """Returns version number string of pyenchant iif it is installed

    Othervise returns None

    """

    try:
        import enchant
    except ImportError:
        return

    return enchant.__version__


def get_gpg_version():
    """Returns version string if gpg is insatlled else false"""
    try:
        import gnupg
    except ImportError:
        return

    return gnupg.__version__