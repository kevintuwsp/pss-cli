from PyQt5.QtWidgets import QComboBox, QCompleter


class SearchableQComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_searchable(self):
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.completer().setCompletionMode(QCompleter.PopupCompletion)
