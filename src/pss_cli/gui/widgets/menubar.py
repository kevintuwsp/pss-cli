import PyQt5.QtWidgets as QtWidgets
import qdarktheme

from pss_cli.gui.settings import settings


class MenuBar(QtWidgets.QMenuBar):
    def __init__(self):
        super().__init__()

        self._file_menu = self.addMenu("File")
        self._edit_menu = self.addMenu("Edit")
        self._view_menu = self.addMenu("View")
        self._help_menu = self.addMenu("Help")

        self._set_theme = self._view_menu.addMenu("Set Theme")

        self._create_actions()

    def _create_actions(self):
        self._new_action = QtWidgets.QAction("&New", self)
        self._open_action = QtWidgets.QAction("&Open", self)
        self._save_action = QtWidgets.QAction("&Save", self)
        self._quit_action = QtWidgets.QAction("&Quit", self)

        self._file_menu.addAction(self._new_action)
        self._file_menu.addAction(self._open_action)
        self._file_menu.addAction(self._save_action)
        self._file_menu.addAction(self._quit_action)

        self._new_action.triggered.connect(self._new)
        self._open_action.triggered.connect(self._open)
        self._save_action.triggered.connect(self._save)
        self._quit_action.triggered.connect(self._quit)

        self._new_action.setShortcut("Ctrl+N")
        self._quit_action.setShortcut("Ctrl+Q")
        self._open_action.setShortcut("Ctrl+O")
        self._save_action.setShortcut("Ctrl+S")

        self._new_action.setStatusTip("Create a new file")

        self._dark_theme = QtWidgets.QAction("Dark Theme", self)
        self._light_theme = QtWidgets.QAction("Light Theme", self)

        self._set_theme.addAction(self._dark_theme)
        self._set_theme.addAction(self._light_theme)

        self._dark_theme.triggered.connect(self._set_dark_theme)
        self._light_theme.triggered.connect(self._set_light_theme)

    def _set_light_theme(self):
        qdarktheme.setup_theme("light")
        settings.setValue("gui/theme", "light")

    def _set_dark_theme(self):
        qdarktheme.setup_theme("dark")
        settings.setValue("gui/theme", "dark")

    def _new(self):
        print("Creating a new file")

    def _open(self):
        print("Opening a file")

    def _save(self):
        print("Saving a file")

    def _quit(self):
        print("Quitting the application")
        QtWidgets.QApplication.quit()
