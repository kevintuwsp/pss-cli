from abc import ABC, ABCMeta, abstractmethod
from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot

from pss_cli.gui.widgets.checkable_combobox import CheckableComboBox


class SimpleDialogMeta(ABCMeta, type(QtWidgets.QDialog)):
    pass


class SimpleDialogWidget(ABC, metaclass=SimpleDialogMeta):
    pass


class SimpleDialog(QtWidgets.QDialog, SimpleDialogWidget):
    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
        minimum_width: int = 400,
    ):
        super().__init__(parent)
        self._current_row = 0
        self._required = []
        self._grid_layout_indexes = []
        self._layout = QtWidgets.QGridLayout()
        self.setMinimumWidth(minimum_width)
        self.setLayout(self._layout)
        self.init_ui()
        self.add_required_label()
        self.add_buttons()

    def add_widget(
        self,
        widget: QtWidgets.QWidget,
        label_name: Optional[str] = None,
        required: bool = False,
        row_offset: int = 0,
    ):
        if required:
            self._required.append(widget)
            label_name = f"{label_name}*"

        if label_name:
            label = QtWidgets.QLabel(label_name)
            self._layout.addWidget(label, self._current_row + row_offset, 0, 1, 1)
            self._layout.addWidget(widget, self._current_row + row_offset, 1, 1, 1)
            self._grid_layout_indexes.insert(
                self._current_row, (self._current_row + row_offset, 0, 1, 1)
            )
        else:
            self._layout.addWidget(widget, self._current_row + row_offset, 0, 1, 2)
            self._grid_layout_indexes.insert(
                self._current_row, (self._current_row + row_offset, 0, 1, 2)
            )
        self._current_row += 1

    def shift_widgets(self, row: int, row_offset: int):
        """Shift widgets from the given row down by the given offset."""

        for i in range(row, len(self._grid_layout_indexes)):
            widget = self._layout.itemAtPosition(*self._grid_layout_indexes[i][:2])
            if widget:
                self._layout.addWidget(
                    widget.widget(),
                    self._grid_layout_indexes[i][0] + row_offset,
                    self._grid_layout_indexes[i][1],
                    self._grid_layout_indexes[i][2],
                    self._grid_layout_indexes[i][3],
                )

    def clear_required_label(self):
        """Clear the required fields and buttons from the dialog."""

        self.required_label.deleteLater()

    def clear_accept_cancel_buttons(self):
        """Clear the accept and cancel buttons from the dialog."""

        self.button_box.deleteLater()

    def add_required_label(self):
        self.required_label = QtWidgets.QLabel(
            "Required fields are marked with <span style='color: red;'>*</span>"
        )
        self.add_widget(self.required_label)

    def add_buttons(self):
        self.buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.button_box = QtWidgets.QDialogButtonBox(self.buttons)
        self.button_box.accepted.connect(self._accept)
        self.button_box.rejected.connect(self.cancel)
        self.add_widget(self.button_box)

    def _accept(self):
        if self.get_unvalidated():
            for widget in self.get_validated():
                self.color_normal()
            for widget in self.get_unvalidated():
                self.color_required(widget)
            return
        self.accept()

    def color_required(self, widget: QtWidgets.QWidget):
        widget.setStyleSheet("border: 1px solid red;")

    def color_normal(self):
        for widget in self._required:
            widget.setStyleSheet("")

    def get_validated(self):
        return [widget for widget in self._required if self.get_widget_value(widget)]

    def get_unvalidated(self):
        return [
            widget for widget in self._required if not self.get_widget_value(widget)
        ]

    def get_widget_value(self, widget: QtWidgets.QWidget):
        if isinstance(widget, QtWidgets.QLineEdit):
            return widget.text()
        elif isinstance(widget, QtWidgets.QComboBox):
            return widget.currentText()
        elif isinstance(widget, QtWidgets.QCheckBox):
            return widget.isChecked()
        elif isinstance(widget, QtWidgets.QRadioButton):
            return widget.isChecked()
        elif isinstance(widget, QtWidgets.QSpinBox):
            return widget.value()
        elif isinstance(widget, QtWidgets.QDoubleSpinBox):
            return widget.value()
        elif isinstance(widget, QtWidgets.QTextEdit):
            return widget.toPlainText()
        elif isinstance(widget, QtWidgets.QPlainTextEdit):
            return widget.toPlainText()
        elif isinstance(widget, QtWidgets.QDateEdit):
            return widget.date().toPyDate()
        elif isinstance(widget, QtWidgets.QTimeEdit):
            return widget.time().toPyTime()
        elif isinstance(widget, QtWidgets.QDateTimeEdit):
            return widget.dateTime().toPyDateTime()
        elif isinstance(widget, CheckableComboBox):
            return widget.currentData()
        else:
            raise NotImplementedError

    @abstractmethod
    def init_ui(self):
        raise NotImplementedError

    @abstractmethod
    @pyqtSlot()
    def accept(self):
        raise NotImplementedError

    @abstractmethod
    @pyqtSlot()
    def cancel(self):
        raise NotImplementedError
