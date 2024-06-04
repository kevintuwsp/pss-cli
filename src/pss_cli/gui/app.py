import os
from typing import Optional
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import qdarktheme

from pss_cli.gui.widgets import (
    MenuBar,
    StatusBar,
    Sidebar,
    OutputWindow,
    CentralWindow,
    ContextActionsWidget,
)
from pss_cli.gui.settings import settings


basedir = os.path.abspath(os.path.dirname(__file__))
main_icon = os.path.join(
    basedir, "assets/icons8-database-administrator-48.png")


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSS Application")
        self.setWindowIcon(QtGui.QIcon(main_icon))
        # self.setMinimumSize(1600, 1000)

        saved_geometry = settings.value("gui/geometry")
        if saved_geometry:
            self.setGeometry(saved_geometry)

        theme = settings.value("gui/theme")
        if theme:
            try:
                qdarktheme.setup_theme(theme)
            except ValueError:
                qdarktheme.setup_theme("dark")
                settings.setValue("gui/theme", "dark")

        self._menu_bar = MenuBar()
        self._status_bar = StatusBar()
        self._central_window = CentralWindow()
        self._sidebar = Sidebar()
        self._output_window = OutputWindow()
        self._context_actions = ContextActionsWidget()

        self.setMenuBar(self._menu_bar)
        self.setStatusBar(self._status_bar)

        self.setCentralWidget(self._central_window)
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self._sidebar)
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, self._output_window
        )
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._context_actions
        )
        self.show()

        self._sidebar.list_view.clicked.connect(
            self._central_window._sql_view.set_table_view_from_index
        )

    def resizeEvent(self, a0: Optional[QtGui.QResizeEvent] = None) -> None:
        """Saves the geometry of the window when it is closed."""
        settings.setValue("gui/geometry", self.geometry())
        a0.accept()  # type: ignore

    def moveEvent(self, a0: Optional[QtGui.QMoveEvent] = None) -> None:
        """Saves the geometry of the window when it is closed."""
        settings.setValue("gui/geometry", self.geometry())
        a0.accept()  # type: ignore
