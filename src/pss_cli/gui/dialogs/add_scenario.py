from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot

from pss_cli.core.logging import logger
from pss_cli.gui.dialogs.simple_dialog import SimpleDialog
from pss_cli.gui.widgets.checkable_combobox import CheckableComboBox
from pss_cli.core.database import db
from pss_cli.core.controllers import ControllerFactory


class AddScenario(SimpleDialog):
    """Add a scenario to the database"""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        controller_factory = ControllerFactory()
        self.controller = controller_factory.create_controller("scenario")
        super().__init__(parent)

    def init_ui(self):
        self.setWindowTitle("Add a scenario to the database")

        objects = db.select_table("case")

        if not objects:
            logger.error("No cases found in the database")
            return

        self.cases_dict = {case.name: case for case in objects}  # type: ignore

        self.name_edit = QtWidgets.QLineEdit()
        self.description_edit = QtWidgets.QLineEdit()
        self.cases = CheckableComboBox()
        self.cases.addItems([str(name) for name in self.cases_dict.keys()])

        self.add_widget(self.name_edit, "Name", required=True)
        self.add_widget(self.description_edit, "Description", required=True)
        self.add_widget(self.cases, "Case", required=True)

    @pyqtSlot()
    def accept(self):
        case_names = self.cases.currentData()
        cases = [self.cases_dict[case_name] for case_name in case_names]

        self.controller.add(
            name=self.name_edit.text(),
            description=self.description_edit.text(),
            cases=cases,  # type: ignore
        )
        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()
