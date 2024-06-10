from typing import Optional
import PyQt5.QtWidgets as QtWidgets


class CheckLicenseDialog(QtWidgets.QMessageBox):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Check for PSSE License")
        self.setText("Please ensure that you have a PSSE license.")
        self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
