import PyQt5.QtWidgets as QtWidgets

from pss_cli.gui.widgets import Sidebar, SQLView


class CentralWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout()

        self.setLayout(self._layout)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._sidebar = Sidebar()
        self._layout.addWidget(self._sidebar)

        self._sql_view = SQLView()
        self._layout.addWidget(self._sql_view, 1)

        self._sidebar.list_view.clicked.connect(
            self._sql_view.set_table_view_from_index
        )

        self.show()
