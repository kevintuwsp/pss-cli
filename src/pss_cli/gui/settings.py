import PyQt5.QtCore as QtCore
import logging

settings = QtCore.QSettings("PSS", "PSS Application")

default_settings = {
    "gui/geometry": QtCore.QRect(0, 0, 1600, 1000),
    "logging/level": logging.INFO,
    "gui/theme": "dark",
    "gui/error_color": "red",
    "gui/error_border_px": 1,
    "gui/error_border_style": "solid",
}

error_border_style = (
    f"border:"
    f"{settings.value('gui/error_border_px')}px"
    f"{settings.value('gui/error_border_style')}"
    f"{settings.value('gui/error_border_color')}"
)


for key, value in default_settings.items():
    if not settings.contains(key):
        settings.setValue(key, value)
