from typing import Optional
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import pyqtSignal

from pss_cli.gui.dialogs.add_case import AddCase
from pss_cli.gui.dialogs.add_scenario import AddScenario
from pss_cli.gui.dialogs.delete_scenario import DeleteScenario
from pss_cli.gui.dialogs.delete_case import DeleteCase
from pss_cli.gui.dialogs.add_gs import AddGeneratingSystem
from pss_cli.gui.dialogs.delete_gs import DeleteGeneratingSystem
from pss_cli.gui.dialogs.add_gs_setpoint import AddGeneratingSystemSetpoint
from pss_cli.gui.settings import settings

error_color = settings.value("gui/error_color")


class SQLActions(QtWidgets.QWidget):
    set_sql_view = pyqtSignal(str)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.parent = parent
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        # self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.add_case_button = QtWidgets.QPushButton("Add Case")
        self.add_case_button.clicked.connect(self.add_case_action)
        self._layout.addWidget(self.add_case_button)

        self.add_scenario_button = QtWidgets.QPushButton("Add Scenario")
        self.add_scenario_button.clicked.connect(self.add_scenario_action)
        self._layout.addWidget(self.add_scenario_button)

        self.add_generating_system_button = QtWidgets.QPushButton(
            "Add Generating System"
        )
        self.add_generating_system_button.clicked.connect(
            self.add_generating_system_action
        )
        self._layout.addWidget(self.add_generating_system_button)

        self.add_generator_setpoint = QtWidgets.QPushButton("Add Generator Setpoint")
        self.add_generator_setpoint.clicked.connect(self.add_generator_setpoint_action)
        self._layout.addWidget(self.add_generator_setpoint)

        self.delete_case_button = QtWidgets.QPushButton("Delete Case")
        self.delete_case_button.clicked.connect(self.delete_case_action)
        self._layout.addWidget(self.delete_case_button)
        self.delete_case_button.setStyleSheet(f"color: {error_color};")

        self.delete_scenario_button = QtWidgets.QPushButton("Delete Scenario")
        self.delete_scenario_button.clicked.connect(self.delete_scenario_action)
        self._layout.addWidget(self.delete_scenario_button)
        self.delete_scenario_button.setStyleSheet(f"color: {error_color};")

        self.delete_generating_system_button = QtWidgets.QPushButton(
            "Delete Generating System"
        )
        self.delete_generating_system_button.clicked.connect(
            self.delete_generating_system
        )
        self._layout.addWidget(self.delete_generating_system_button)
        self.delete_generating_system_button.setStyleSheet(f"color: {error_color};")

    def add_generating_system_action(self):
        self.set_sql_view.emit("generatingsystem")
        dialog = AddGeneratingSystem(self)
        dialog.exec_()
        self.set_sql_view.emit("generatingsystem")

    def add_generator_setpoint_action(self):
        self.set_sql_view.emit("generatorsetpoint")
        dialog = AddGeneratingSystemSetpoint(self)
        dialog.exec_()
        self.set_sql_view.emit("generatorsetpoint")

    def add_scenario_action(self):
        self.set_sql_view.emit("scenario")
        dialog = AddScenario(self)
        dialog.exec_()
        self.set_sql_view.emit("scenario")

    def delete_scenario_action(self):
        self.set_sql_view.emit("scenario")
        dialog = DeleteScenario(self)
        dialog.exec_()
        self.set_sql_view.emit("scenario")

    def add_case_action(self):
        self.set_sql_view.emit("case")
        dialog = AddCase(self)
        dialog.exec_()
        self.set_sql_view.emit("case")

    def delete_case_action(self):
        self.set_sql_view.emit("case")
        dialog = DeleteCase(self)
        dialog.exec_()
        self.set_sql_view.emit("case")

    def delete_generating_system(self):
        self.set_sql_view.emit("generatingsystem")
        dialog = DeleteGeneratingSystem(self)
        dialog.exec_()
        self.set_sql_view.emit("generatingsystem")


class ContextActionsWidget(QtWidgets.QDockWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Context Actions")
        self.sql_actions = SQLActions(self)
        self.setWidget(self.sql_actions)
        self.setMinimumWidth(200)
