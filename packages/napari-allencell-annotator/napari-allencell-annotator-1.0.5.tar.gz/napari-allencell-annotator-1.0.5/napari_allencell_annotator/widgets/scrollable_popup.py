from typing import Set
from napari_allencell_annotator._style import Style
from qtpy.QtGui import QFont
from qtpy.QtWidgets import QLayout
from qtpy import QtWidgets
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QScrollArea, QLabel, QListWidget, QListWidgetItem, QDialog, QDialogButtonBox


class ScrollablePopup(QDialog):
    """
    A class used to create a popup asking for user approval that displays a scrollable list.
    """

    def __init__(self, question: str, names: Set[str], parent=None):
        super().__init__(parent)
        self.setMinimumSize(500, 500)

        self.setStyleSheet(Style.get_stylesheet("main.qss"))

        self.label = QLabel(question)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content = QListWidget()
        self.scroll.setWidget(self.content)

        for str in names:
            widget = QLabel(str)
            widget.setFont(QFont("Arial", 18))
            item = QListWidgetItem(self.content)
            item.setSizeHint(widget.minimumSizeHint())
            self.content.setItemWidget(item, widget)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.buttons)
        self.layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.setLayout(self.layout)
