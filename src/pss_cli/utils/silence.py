import os
import sys


class SilenceStdout:
    def __init__(self):
        self._original_stdout = sys.stdout

    def __enter__(self):
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
