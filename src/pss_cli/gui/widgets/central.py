import PyQt5.QtWidgets as QtWidgets

from pss_cli.gui.widgets import SQLView, SettingsTree


class CentralWindow(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        self._sql_view = SQLView(self)
        self._settings_tree = SettingsTree()
        self.addTab(self._sql_view, "SQL View")
        self.addTab(self._settings_tree, "Settings")

        self.show()
