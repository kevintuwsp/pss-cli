from re import M
from typing import Optional
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore

from pss_cli.core.logging import logger


class ContextActions(QtWidgets.QWidget):
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

        self.add_generator_setpoint = QtWidgets.QPushButton(
            "Add Generator Setpoint")
        self.add_generator_setpoint.clicked.connect(
            self.add_generator_setpoint_action)
        self._layout.addWidget(self.add_generator_setpoint)

    def add_generating_system_action(self):
        logger.info("Add generating system")

    def add_generator_setpoint_action(self):
        logger.info("Add generator setpoint")

    def add_scenario_action(self):
        logger.info("Add scenario")

    def add_case_action(self):
        logger.info("Add action")


class ContextActionsWidget(QtWidgets.QDockWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Context Actions")
        self.widget = ContextActions(self)
        self.setWidget(self.widget)
        self.setMinimumWidth(200)
