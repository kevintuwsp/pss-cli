from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot

from pss_cli.core.logging import logger
from pss_cli.gui.dialogs.simple_dialog import SimpleDialog
from pss_cli.gui.widgets.checkable_combobox import CheckableComboBox
from pss_cli.gui.dialogs.check_license import CheckLicenseDialog
from pss_cli.core.controllers_new import ControllerFactory


class AddCase(SimpleDialog):
    """Add a case to the database"""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        controller_factory = ControllerFactory()
        self.controller = controller_factory.create_controller(self, "case")
        self.root_dir = "."
        super().__init__(parent)

    def init_ui(self):
        self.setWindowTitle("Add Case to the database")
        self.name_edit = QtWidgets.QLineEdit()
        self.description_edit = QtWidgets.QLineEdit()
        self.file_path = QtWidgets.QComboBox()
        self.scenarios = CheckableComboBox()

        self.add_widget(self.name_edit, "Name", required=True)
        self.add_widget(self.description_edit, "Description", required=True)
        self.add_widget(self.file_path, "File", required=True)
        self.add_widget(self.scenarios, "Scenarios", required=False)

        scenario_names = self.controller.get_objects("scenario", attribute="name")
        files = self.controller.get_files(root_dir=self.root_dir, pattern="*.sav")

        if not files:
            logger.error(
                f"No files with match-pattern '*.sav' found within '"
                f"{self.root_dir}' and subdirectories."
            )
            return

        self.scenarios.addItems(scenario_names)
        self.file_path.addItems([str(file) for file in files])

    @pyqtSlot()
    def accept(self):
        result = CheckLicenseDialog(self).exec_()
        if result == QtWidgets.QMessageBox.Cancel:
            return

        scenario_names = self.scenarios.currentData()
        self.controller.add(
            name=self.name_edit.text(),
            description=self.description_edit.text(),
            file_path=self.file_path.currentText(),
            scenario_names=scenario_names,
        )
        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()
