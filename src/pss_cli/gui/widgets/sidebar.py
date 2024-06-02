from typing import Union
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from pss_cli.core.database import db


class UnEditableQStringListModel(QtCore.QStringListModel):
    def flags(self, index) -> Union[int, QtCore.Qt.ItemFlags]:
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable  # noqa: E501


class Sidebar(QtWidgets.QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL Table models")
        self.setContentsMargins(0, 0, 0, 0)
        self.list_view = self.get_list_view()
        self.setWidget(self.list_view)
        self.setMinimumWidth(self.list_view.sizeHint().width())

    def get_list_view(self) -> QtWidgets.QListView:
        """Returns a list view of all the tables in the database."""
        tables = db.get_all_table_names()
        list_view = QtWidgets.QListView()
        list_view.setModel(UnEditableQStringListModel(tables))

        return list_view
