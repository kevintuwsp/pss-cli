import sys
from PyQt5.QtCore import QModelIndex
import PyQt5.QtSql as QtSql
import PyQt5.QtWidgets as QtWidgets


class SQLView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL Table models")
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()
        self.qdb = self.init_db()
        self.model = QtSql.QSqlTableModel()

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

    def set_table_view(self, table_name: str) -> None:
        """Adds a table view to the layout."""
        self.set_table_model(table_name)
        view = QtWidgets.QTableView()
        view.setModel(self.model)
        self.clear_layout()
        self.layout().addWidget(view)

    def set_table_view_from_index(self, index: QModelIndex) -> None:
        """Sets the table view from the index."""
        table_name = index.data()
        self.set_table_view(table_name)
