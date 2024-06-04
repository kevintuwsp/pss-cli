import PyQt5.QtCore as QtCore
import logging

settings = QtCore.QSettings("PSS", "PSS Application")

default_settings = {
    "gui/geometry": QtCore.QRect(0, 0, 1600, 1000),
    "logging/level": logging.INFO,
    "gui/theme": "dark",
}

for key, value in default_settings.items():
    if not settings.contains(key):
        settings.setValue(key, value)
