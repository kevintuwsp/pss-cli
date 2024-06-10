import typer
import PyQt5.QtWidgets as qtw

from pss_cli.gui.app import MainWindow

app = typer.Typer()


@app.command()
def show():
    typer.echo("Showing...")
    app = qtw.QApplication([])

    mw = MainWindow()
    mw.show()
    app.exec_()


@app.command()
def icons():
    import sys
    from PyQt5.QtWidgets import QApplication, QGridLayout, QPushButton, QStyle, QWidget

    class Window(QWidget):
        def __init__(self):
            super(Window, self).__init__()

            icons = sorted([attr for attr in dir(QStyle) if attr.startswith("SP_")])
            layout = QGridLayout()

            for n, name in enumerate(icons):
                btn = QPushButton(name)

                pixmapi = getattr(QStyle, name)
                icon = self.style().standardIcon(pixmapi)
                btn.setIcon(icon)
                layout.addWidget(btn, n / 4, n % 4)

            self.setLayout(layout)

    app = QApplication(sys.argv)

    w = Window()
    w.show()

    app.exec_()
