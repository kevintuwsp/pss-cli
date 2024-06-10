from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot

from pss_cli.core.logging import logger
from pss_cli.gui.dialogs.simple_dialog import SimpleDialog
from pss_cli.gui.widgets.checkable_combobox import CheckableComboBox
from pss_cli.core.database import db
from pss_cli.core.controllers import ControllerFactory


class DeleteScenario(SimpleDialog):
    """Delete a scenario from the database"""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        controller_factory = ControllerFactory()
        self.controller = controller_factory.create_controller("scenario")
        super().__init__(parent)

    def init_ui(self):
        self.setWindowTitle("Delete a scenario from the database")

        objects = db.select_table("scenario")

        if not objects:
            logger.error("No scenarios found in the database")

        self.scenarios_dict = {scenario.name: scenario for scenario in objects}

        self.scenarios = CheckableComboBox()
        self.scenarios.addItems([str(name) for name in self.scenarios_dict.keys()])
        self.add_widget(self.scenarios, "Scenario", required=True)

    @pyqtSlot()
    def accept(self):
        scenario_names = self.scenarios.currentData()

        for scenario_name in scenario_names:
            self.controller.delete(scenario_name)

        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()
