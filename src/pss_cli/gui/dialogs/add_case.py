from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot

from pss_cli.core.logging import logger
from pss_cli.gui.dialogs.simple_dialog import SimpleDialog
from pss_cli.core.controllers import CaseController


class AddCase(SimpleDialog):
    """Add a case to the database"""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        self.controller = CaseController()
        self.root_dir = "."
        super().__init__(parent)

    def init_ui(self):
        self.setWindowTitle("Add Case to the database")

        files = self.controller.get_files(root_dir=self.root_dir, pattern="*.sav")

        if not files:
            logger.error(
                f"No files with match-pattern '*.sav' found within '"
                f"{self.root_dir}' and subdirectories."
            )
            return

        self.name_edit = QtWidgets.QLineEdit()
        self.description_edit = QtWidgets.QLineEdit()
        self.file_path = QtWidgets.QComboBox()
        self.file_path.addItems([str(file) for file in files])

        self.add_widget(self.name_edit, "Name", required=True)
        self.add_widget(self.description_edit, "Description", required=True)
        self.add_widget(self.file_path, "File", required=True)

    @pyqtSlot()
    def accept(self):
        self.controller.add(
            name=self.name_edit.text(),
            description=self.description_edit.text(),
            file_path=self.file_path.currentText(),
        )
        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()
