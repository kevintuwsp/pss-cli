from typing import Optional
from PyQt5.QtCore import pyqtSlot
import PyQt5.QtWidgets as QtWidgets


class InfoWidget(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self._info_widgets = []
        self._layout = QtWidgets.QGridLayout()
        self.setLayout(self._layout)

    def add_widget(self, widget: QtWidgets.QWidget, label: Optional[str] = None):
        """Add a widget to the layout"""

        if label is not None:
            label_widget = QtWidgets.QLabel(label)
            self._layout.addWidget(label_widget, self._layout.rowCount(), 0)
            self._layout.addWidget(widget, self._layout.rowCount() - 1, 1)
        else:
            self._layout.addWidget(widget, self._layout.rowCount(), 0, 1, 2)

    def set_widget(
        self,
        label_name: str,
        widget: QtWidgets.QWidget,
        required: bool = False,
    ):
        """Set the widget to be displayed"""

        self._widget = widget
        self._layout.addWidget(widget, 1, 0, 1, 2)

    def add_info_widget(self, widget: QtWidgets.QWidget):
        """Add an info widget to the layout"""

        self._info_widgets.append(widget)
        self._layout.addWidget(widget, 2, 0, 1, 2)

    @pyqtSlot()
    def update_info(self):
        """Update the info widgets"""
        pass

    def get_value(self):
        """Get the value from the primary widget"""
        pass
