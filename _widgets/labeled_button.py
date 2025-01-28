from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt

class LabeledButton(QWidget):
  clicked = pyqtSignal(str)

  def __init__(self, labelText: str, buttonText: str, parent=None):
    super().__init__(parent)
    self.label = QLabel(labelText)
    self.button = QPushButton(buttonText)

    self.button.clicked.connect(self.buttonClicked)

    self.button.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

    layout = QVBoxLayout()
    layout.addWidget(self.label)
    layout.addWidget(self.button)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.setLayout(layout)

  def getLabel(self):
    return self.label

  def getButton(self):
    return self.button

  def buttonClicked(self):
    self.clicked.emit(self.button.text())