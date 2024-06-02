import PyQt5.QtWidgets as QtWidgets


class StatusBar(QtWidgets.QStatusBar):
    def __init__(self):
        super().__init__()
        self.showMessage("Ready")
        self.show()
