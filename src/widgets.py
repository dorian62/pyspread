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


from PyQt5.QtCore import pyqtSignal, QSize, QStateMachine, QState
from PyQt5.QtWidgets import QToolButton, QColorDialog, QFontComboBox, QComboBox
from PyQt5.QtGui import QPalette, QColor, QFont, QIntValidator, QIcon

from icons import Icon

from config import config


class MultiStateBitmapButton(QToolButton):
    """QPushbutton that cycles through arbitrary states

    The states are defined by an iterable of QIcons

    Parameters
    ----------

    * actions: List of QIcons
    \tThe list of icons to be cycled through

    """

    def __init__(self, actions):
        super().__init__()

        self.actions = actions
        self.statemachine = QStateMachine(self)

        states = []
        for action in actions:
            state = QState()
            state.action = action
            state.assignProperty(self, 'icon', QIcon(Icon(action)))
            states.append(state)
            self.statemachine.addState(state)

        # Connect states to a cycle
        for state1, state2 in zip(states[:-1], states[1:]):
            state1.addTransition(self.pressed, state2)
        states[-1].addTransition(self.pressed, states[0])

        self.statemachine.setInitialState(states[0])
        self.statemachine.start()

        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        """Button clicked event handler. Chechs corresponding menu item"""

        state = next(iter(self.statemachine.configuration()), None)

        for action in self.actions:
            enabled = action == state.action
            if enabled:
                self.main_window.actions[action].trigger()
            else:
                self.main_window.actions[action].setChecked(False)


class RotationButton(MultiStateBitmapButton):
    """Rotation button for the format toolbar"""

    actions = ("rotate_0", "rotate_90", "rotate_180", "rotate_270")

    def __init__(self, main_window):
        self.main_window = main_window

        super().__init__(self.actions)
        self.setStatusTip("Text rotation")
        self.setToolTip("Text rotation")


class JustificationButton(MultiStateBitmapButton):
    """Justification button for the format toolbar"""

    actions = ("justify_left", "justify_center", "justify_right")

    def __init__(self, main_window):
        self.main_window = main_window

        super().__init__(self.actions)
        self.setStatusTip("Text justification")
        self.setToolTip("Text justification")


class AlignmentButton(MultiStateBitmapButton):
    """Alignment button for the format toolbar"""

    actions = ("align_top", "align_center", "align_bottom")

    def __init__(self, main_window):
        self.main_window = main_window

        super().__init__(self.actions)
        self.setStatusTip("Text alignment")
        self.setToolTip("Text alignment")


class ColorButton(QToolButton):
    """Color button widget

    Parameters
    ----------

    * qcolor: QColor
    \tColor that is initially set
    * icon: QIcon, defaults to None
    \tButton foreground image
    * max_size: QSize, defaults to QSize(28, 28)
    \tMaximum Size of the button

    """

    colorChanged = pyqtSignal()
    title = "Select color"

    def __init__(self, color, icon=None, max_size=QSize(28, 28)):
        super().__init__()

        if icon is not None:
            self.setIcon(icon)

        self.color = color

        self.pressed.connect(self.on_pressed)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        """Color setter that adjusts internal state and button background.

        Parameters
        ----------
        * color: QColor
        \tNew color attribute to be set
        """

        if hasattr(self, "_color") and self._color == color:
            return

        self._color = color

        palette = self.palette()
        palette.setColor(QPalette.Button, color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.update()

    def set_max_size(self, size):
        """Set the maximum size of the widget

        size: Qsize
        \tMaximum size of the widget

        """

        self.setMaximumWidth(size.width())
        self.setMaximumHeight(size.height())

    def on_pressed(self):
        """Button pressed event handler

        Shows color dialog and sets the chosen color.

        """

        dlg = QColorDialog(self)
        dlg.setCurrentColor(self.color)
        dlg.setWindowTitle(self.title)

        if dlg.exec_():
            self.color = dlg.currentColor()
            self.colorChanged.emit()


class TextColorButton(ColorButton):
    """Color button with text icon"""

    def __init__(self, color):
        icon = Icon("text_color")
        super().__init__(color, icon=icon)

        self.title = "Select text color"
        self.setStatusTip("Text color")
        self.setToolTip("Text color")


class LineColorButton(ColorButton):
    """Color button with text icon"""

    def __init__(self, color):
        icon = Icon("line_color")
        super().__init__(color, icon=icon)

        self.title = "Select cell border line color"
        self.setStatusTip("Cell border line color")
        self.setToolTip("Cell border line color")


class BackgroundColorButton(ColorButton):
    """Color button with text icon"""

    def __init__(self, color):
        icon = Icon("background_color")
        super().__init__(color, icon=icon)

        self.title = "Select cell background color"
        self.setStatusTip("Cell background color")
        self.setToolTip("Cell background color")


class FontChoiceCombo(QFontComboBox):
    """Font choice combo box"""

    fontChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMaximumWidth(150)

        # Set default font
        self.setFont(QFont(config["font"]))

        self.currentFontChanged.connect(self.on_font)

    @property
    def font(self):
        return self.currentFont().family()

    @font.setter
    def font(self, font):
        """Sets font without emitting currentTextChanged"""

        self.currentFontChanged.disconnect(self.on_font)
        self.setCurrentFont(QFont(font))
        self.currentFontChanged.connect(self.on_font)

    def on_font(self, font):
        """Font choice event handler"""

        self.fontChanged.emit()


class FontSizeCombo(QComboBox):
    """Font choice combo box"""

    fontSizeChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setEditable(True)

        for size in config["font_default_sizes"]:
            self.addItem(str(size))

        idx = self.findText(str(config["font_default_size"]))
        if idx >= 0:
            self.setCurrentIndex(idx)

        validator = QIntValidator(1, 128, self)
        self.setValidator(validator)

        self.currentTextChanged.connect(self.on_text)

    @property
    def size(self):
        return int(self.currentText())

    @size.setter
    def size(self, size):
        """Sets size without emitting currentTextChanged"""

        self.currentTextChanged.disconnect(self.on_text)
        self.setCurrentText(str(size))
        self.currentTextChanged.connect(self.on_text)

    def on_text(self, size):
        """Font size choice event handler"""

        try:
            value = int(self.currentText())
        except ValueError:
            value = 1
            self.setCurrentText("1")

        if value < 1:
            self.setCurrentText("1")
        if value > 128:
            self.setCurrentText("128")

        self.fontSizeChanged.emit()


class Widgets:
    def __init__(self, main_window):

        self.main_window = main_window

        main_window.gui_update.connect(self.on_gui_update)

        # Format toolbar widgets

        self.font_combo = FontChoiceCombo()

        self.font_size_combo = FontSizeCombo()

        text_color = QColor(*config["text_color"])
        self.text_color_button = TextColorButton(text_color)

        background_color = QColor(*config["background_color"])
        self.background_color_button = BackgroundColorButton(background_color)

        line_color = QColor(*config["grid_color"])
        self.line_color_button = LineColorButton(line_color)

        self.rotate_button = RotationButton(main_window)
        self.justify_button = JustificationButton(main_window)
        self.align_button = AlignmentButton(main_window)

    def on_gui_update(self, attributes):
        """GUI update event handler.

        Emmitted on cell change. Attributes contains current cell_attributes.

        """

        self.text_color_button.color = QColor(*attributes["textcolor"])
        self.background_color_button.color = QColor(*attributes["bgcolor"])
        self.font_combo.font = attributes["textfont"]
        self.font_size_combo.size = attributes["pointsize"]

        is_bold = attributes["fontweight"] == QFont.Bold
        self.main_window.actions["bold"].setChecked(is_bold)

        is_italic = attributes["fontstyle"] == QFont.StyleItalic
        self.main_window.actions["italics"].setChecked(is_italic)

        underline_action = self.main_window.actions["underline"]
        underline_action.setChecked(attributes["underline"])

        strikethrough_action = self.main_window.actions["strikethrough"]
        strikethrough_action.setChecked(attributes["strikethrough"])
