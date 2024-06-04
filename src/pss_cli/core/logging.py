import logging
from rich.logging import RichHandler

from pss_cli.gui.settings import settings

fmt_colors = {
    logging.DEBUG: "green",
    logging.INFO: "blue",
    logging.WARNING: "orange",
    logging.ERROR: "red",
    logging.CRITICAL: "red",
}

fmt_str = "[%(asctime)s] <font color='{}'>[%(levelname)s]</font>: %(message)s"
fmts = {k: fmt_str.format(v) for k, v in fmt_colors.items()}
default_fmt = fmt_str.format("white")


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        last_fmt = self._style._fmt
        fmt = fmts.get(record.levelno, default_fmt)
        self._style._fmt = fmt
        res = logging.Formatter.format(self, record)
        self._style._fmt = last_fmt
        return res


FORMAT = "%(message)s"
logging.basicConfig(
    level=settings.value("logging/level"),
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(markup=True, rich_tracebacks=True)],
)


logger = logging.getLogger("rich")
