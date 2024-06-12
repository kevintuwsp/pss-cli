from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot
import sqlalchemy

from pss_cli.core.logging import logger
from pss_cli.gui.dialogs.simple_dialog import SimpleDialog
from pss_cli.core.controllers import ControllerFactory


# TODO: Incomplete, finish off
class AddGeneratingSystemSetpoint(SimpleDialog):
    """Add a generating system to the database"""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        controller_factory = ControllerFactory()
        self.controller = controller_factory.create_controller(
            "generating_system_setpoint"
        )
        super().__init__(parent)

    def init_ui(self):
        self.setWindowTitle("Add Generating system setpoints to the database")

        self.case_name_edit = QtWidgets.QComboBox()
        cases = self.controller.get_cases()
        self.case_name_edit.addItems([str(case.name) for case in cases])

        self.scenario_name_edit = QtWidgets.QComboBox()
        self.generating_system_name_edit = QtWidgets.QComboBox()

        self.p_setpoint_edit = QtWidgets.QDoubleSpinBox()
        self.q_setpoint_edit = QtWidgets.QDoubleSpinBox()
        self.p_setpoint_edit.setDecimals(2)
        self.q_setpoint_edit.setDecimals(2)
        self.p_setpoint_edit.setMinimum(-1000)
        self.p_setpoint_edit.setMaximum(1000)
        self.q_setpoint_edit.setMinimum(-1000)
        self.q_setpoint_edit.setMaximum(1000)

        self.add_widget(self.case_name_edit, "Case Name", required=True)
        self.add_widget(self.scenario_name_edit, "Scenario Name", required=True)
        self.add_widget(
            self.generating_system_name_edit, "Generating System Name", required=True
        )
        self.add_widget(self.p_setpoint_edit, "P Setpoint", required=True)
        self.add_widget(self.q_setpoint_edit, "Q Setpoint", required=True)

        self.case_name_edit.editTextChanged.connect(self.update_info)
        self.update_info()

    def update_info(self):
        """Update the info widgets"""

        case_name = self.case_name_edit.currentText()
        scenarios = self.controller.get_scenarios(case_name)
        self.scenario_name_edit.clear()
        self.scenario_name_edit.addItems([str(scenario.name) for scenario in scenarios])

        case = self.controller.get_case(case_name)
        generating_systems = self.controller.get_generating_systems(case)

        self.generating_system_name_edit.clear()
        self.generating_system_name_edit.addItems(
            [str(gs.name) for gs in generating_systems]
        )

    @pyqtSlot()
    def accept(self):
        case_name = self.case_name_edit.currentText()
        scenario_name = self.scenario_name_edit.currentText()
        generating_system_name = self.generating_system_name_edit.currentText()

        try:
            self.controller.add(
                scenario_name=scenario_name,
                case_name=case_name,
                gs_name=generating_system_name,
                p_setpoint=self.p_setpoint_edit.value(),
                q_setpoint=self.q_setpoint_edit.value(),
            )
        except sqlalchemy.exc.IntegrityError:
            dlg = QtWidgets.QMessageBox()
            dlg.setText("The generating system setpoint already exists in the database")
            dlg.exec_()
            return
        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()
