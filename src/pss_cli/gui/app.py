import os
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

from pss_cli.gui.widgets import (
    MenuBar,
    StatusBar,
    SQLView,
    Sidebar,
)

basedir = os.path.abspath(os.path.dirname(__file__))
main_icon = os.path.join(
    basedir, "assets/icons8-database-administrator-48.png")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSS Application")
        self.setWindowIcon(QtGui.QIcon(main_icon))
        self.setMinimumSize(800, 600)

        self._menu_bar = MenuBar()
        self._status_bar = StatusBar()
        self._sql_view = SQLView()
        self._sidebar = Sidebar()

        self.setMenuBar(self._menu_bar)
        self.setStatusBar(self._status_bar)
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._sidebar)
        self.setCentralWidget(self._sql_view)
        self.show()

        self._sidebar.list_view.clicked.connect(
            self._sql_view.set_table_view_from_index
        )
