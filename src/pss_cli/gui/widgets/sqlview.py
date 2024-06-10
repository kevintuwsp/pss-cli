import sys
from typing import Optional
from PyQt5.QtCore import QModelIndex
import PyQt5.QtSql as QtSql
import PyQt5.QtWidgets as QtWidgets

editable_tables = [
    "case",
    "scenario",
    "generatingsystem",
    "generator",
    "infgenerator",
    "generatingsystemsetpoint",
]


class SQLView(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QTabWidget] = None):
        super().__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)
        self.setWindowTitle("SQL Table models")
        self.qdb = self.init_db()
        self.model = QtSql.QSqlTableModel()
        # self.model = QtSql.QSqlRelationalTableModel()
        # self.delegate = QtSql.QSqlRelationalDelegate(self)
        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        # self.view.setItemDelegate(self.delegate)
        self._layout.addWidget(self.view)
        self.view.setSortingEnabled(True)
        # self.set_table_model("case")

    def init_db(self) -> QtSql.QSqlDatabase:
        qdb = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        qdb.setDatabaseName("sqlite.db")
        if not qdb.open():
            sys.exit(-1)
        return qdb

    def clear_layout(self) -> None:
        """Clears the layout of the widget."""
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

    def set_table_model(self, table_name: str) -> None:
        """Returns a table model for the given table name."""

        self.model.setTable(table_name)
        self.model.select()
        if table_name not in editable_tables:
            self.view.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        else:
            self.view.setEditTriggers(QtWidgets.QTableView.DoubleClicked)
        self.view.resizeColumnsToContents()

    def set_table_view_from_index(self, index: QModelIndex) -> None:
        """Sets the table view from the index."""
        table_name = index.data()
        self.set_table_model(table_name)
