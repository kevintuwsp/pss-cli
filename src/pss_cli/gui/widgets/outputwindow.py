import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import logging

from pss_cli.core.logging import logger, ColoredFormatter


class QTextEditLogger(QtCore.QObject, logging.Handler):
    new_record = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit()
        self.widget.setReadOnly(True)
        formatter = ColoredFormatter(
            fmt="[%(asctime)s] [%(levelname)s] : %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
        )
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        self.new_record.emit(msg)


class OutputWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.logTextBox = QTextEditLogger()
        logger.addHandler(self.logTextBox)
        self.logTextBox.new_record.connect(self.logTextBox.widget.appendHtml)

        self._layout = QtWidgets.QVBoxLayout()
        self._button = QtWidgets.QPushButton(self)

        self.setLayout(self._layout)

        self._button.setText("Test Me")
        self._layout.addWidget(self._button)
        self._layout.addWidget(self.logTextBox.widget)
        self._button.clicked.connect(self.test)

    def test(self):
        logger.debug("damn, a bug")
        logger.info("something to remember")
        logger.warning("that's not right")
        logger.error("foobar")


class OutputWindow(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Output Window")
        self.widget = OutputWidget()
        self.setWidget(self.widget)
