from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot

from pss_cli.core.logging import logger
from pss_cli.gui.dialogs.simple_dialog import SimpleDialog
from pss_cli.core.database import db
from pss_cli.core.controllers import ControllerFactory


class DeleteCase(SimpleDialog):
    """Delete a case from the database"""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        controller_factory = ControllerFactory()
        self.controller = controller_factory.create_controller("case")
        super().__init__(parent)

    def init_ui(self):
        self.setWindowTitle("Delete case from the database")

        objects = db.select_table("case")

        if not objects:
            logger.error("No cases found in the database")
            return

        self.cases_dict = {case.name: case for case in objects}

        self.case = QtWidgets.QComboBox()
        self.case.addItems([str(name) for name in self.cases_dict.keys()])
        self.add_widget(self.case, "Case", required=True)

    @pyqtSlot()
    def accept(self):
        self.controller.delete(self.case.currentText())
        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()
