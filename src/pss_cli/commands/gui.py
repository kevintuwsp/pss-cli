import sys
import typer
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from PyQt5 import QtWidgets, QtSql

from pss_cli.gui.app import MainWindow
from pss_cli.core.database import db

app = typer.Typer()


@app.command()
def show():
    typer.echo("Showing...")
    app = qtw.QApplication([])
    mw = MainWindow()

    app.exec_()
