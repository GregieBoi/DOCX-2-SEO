from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout, QSpacerItem
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt

class LabeledDropdown(QWidget):
  currentTextChanged = pyqtSignal(str)

  def __init__(self, labelText: str, dropdownItems: list[str] =None, parent=None):
    super().__init__(parent)
    self.label = QLabel(labelText)
    self.spacer = QSpacerItem(5, 5)
    self.dropdown = QComboBox()
    if dropdownItems:
      self.dropdown.addItems(dropdownItems)

    self.dropdown.currentTextChanged.connect(self.sendCurrentText)

    self.dropdown.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

    layout = QVBoxLayout()
    layout.addWidget(self.label)
    layout.addItem(self.spacer)
    layout.addWidget(self.dropdown)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.setLayout(layout)

  def getLabel(self):
    return self.label

  def getDropdown(self):
    return self.dropdown
  
  def getCurrentText(self):
    return self.dropdown.currentText()
  
  def clear(self):
    self.dropdown.clear()

  def addItem(self, item: str):
    self.dropdown.addItem(item)

  def addItems(self, items : list[str]):
    self.dropdown.addItems(items)

  def removeItem(self, item: str):
    self.dropdown.removeItem(item)

  def setCurrentText(self, text: str):
    self.dropdown.setCurrentText(text)

  def sendCurrentText(self):
    self.currentTextChanged.emit(self.dropdown.currentText())