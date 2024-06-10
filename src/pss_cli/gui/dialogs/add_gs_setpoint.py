from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot

from pss_cli.core.logging import logger
from pss_cli.gui.dialogs.simple_dialog import SimpleDialog
from pss_cli.core.controllers import GeneratingSystemSetpointController


# TODO: Incomplete, finish off
class AddGeneratingSystemSetpoint(SimpleDialog):
    """Add a generating system to the database"""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        self.controller = GeneratingSystemSetpointController()
        super().__init__(parent)

    def init_ui(self):
        self.setWindowTitle("Add Generating system setpoints to the database")

        scenarios = self.controller.get_scenarios()
        generating_systems = self.controller.get_generating_systems()

        if not scenarios or not generating_systems:
            logger.error("No scenarios or generating systems found in the database")
            return

        self.scenario_name_edit = QtWidgets.QComboBox()
        self.generating_system_name_edit = QtWidgets.QComboBox()
        self.generating_system_name_edit.addItems(
            [str(gs.name) for gs in generating_systems]
        )  # type: ignore
        self.scenario_name_edit.addItems([str(scenario.name) for scenario in scenarios])  # type: ignore

        self.p_setpoint_edit = QtWidgets.QDoubleSpinBox()
        self.q_setpoint_edit = QtWidgets.QDoubleSpinBox()

        self.add_widget(self.scenario_name_edit, "Scenario Name", required=True)
        self.add_widget(
            self.generating_system_name_edit, "Generating System Name", required=True
        )
        self.add_widget(self.p_setpoint_edit, "P Setpoint", required=True)

    @pyqtSlot()
    def accept(self):
        scenario_name = self.scenario_name_edit.currentText()
        generating_system_name = self.generating_system_name_edit.currentText()
        self.controller.add(
            scenario_name=scenario_name,
            gs_name=generating_system_name,
            p_setpoint=self.p_setpoint_edit.value(),
            q_setpoint=self.q_setpoint_edit.value(),
        )
        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()
