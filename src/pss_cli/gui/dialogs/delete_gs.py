from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot

from pss_cli.core.logging import logger
from pss_cli.gui.dialogs.simple_dialog import SimpleDialog
from pss_cli.core.database import db
from pss_cli.core.controllers import GeneratingSystemController


class DeleteGeneratingSystem(SimpleDialog):
    """Delete a generating system from the database"""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        self.controller = GeneratingSystemController()
        super().__init__(parent)

    def init_ui(self):
        self.setWindowTitle("Delete generating system from the database")

        gs_objs = db.select_table("generatingsystem")

        if not gs_objs:
            logger.error("No generating systems found in the database")
            return

        gs_names = [gs.name for gs in gs_objs]  # type: ignore

        self.generating_systems = QtWidgets.QComboBox()
        self.generating_systems.addItems(gs_names)
        self.add_widget(self.generating_systems, "Generating Systems", required=True)

    @pyqtSlot()
    def accept(self):
        self.controller.delete(self.generating_systems.currentText())
        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()
