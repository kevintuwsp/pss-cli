import PyQt5.QtWidgets as qtw

from pss_cli.gui.widgets.sidebar import Sidebar
from pss_cli.gui.widgets.sqlview import SQLView


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL Table models")
        self.setLayout(qtw.QHBoxLayout())
        # self.label = qtw.QLabel("SQL Table models")
        # self.layout().addWidget(self.label)
        self.show()
        self.sidebar = Sidebar()
        self.layout().addWidget(self.sidebar)

        self.sql_view = SQLView()
        self.sql_view.set_table_view("busdefinition")
        self.layout().addWidget(self.sql_view, 1)
        self.setMinimumSize(800, 600)

        self.sidebar.list_view.clicked.connect(self.sql_view.set_table_view_from_index)


if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    app.exec_()
