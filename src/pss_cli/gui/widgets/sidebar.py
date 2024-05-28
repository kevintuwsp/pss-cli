import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from pss_cli.core.database import db


class Sidebar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL Table models")
        self.setLayout(QtWidgets.QVBoxLayout())
        self.label = QtWidgets.QLabel("SQL Table models")
        self.layout().addWidget(self.label)
        self.show()
        self.list_view = self.get_list_view()
        self.set_widget(self.list_view)
        self.setMinimumSize(200, 600)

    def clear_layout(self) -> None:
        """Clears the layout of the widget."""
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

    def set_widget(self, widget) -> None:
        """Sets the widget to the layout."""
        self.clear_layout()
        self.layout().addWidget(widget)

    def get_list_view(self) -> QtWidgets.QListView:
        """Returns a list view of all the tables in the database."""
        tables = db.get_all_table_names()
        list_view = QtWidgets.QListView()
        list_view.setModel(QtCore.QStringListModel(tables))

        return list_view
