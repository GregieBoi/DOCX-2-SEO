from PyQt6.QtWidgets import QWidget,QLabel, QLineEdit, QVBoxLayout, QSpacerItem
from PyQt6.QtCore import Qt, pyqtSignal

class LabeledLineEdit(QWidget):
  textChanged = pyqtSignal()

  def __init__(self, labelText: str, placeholderText: str=None, parent=None):
    super().__init__(parent)
    self.label = QLabel(labelText)
    self.spacer = QSpacerItem(5, 7)
    self.lineEdit = QLineEdit()
    self.lineEdit.textChanged.connect(self.sendText)
    self.lineEdit.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
    if placeholderText:
      self.lineEdit.setPlaceholderText(placeholderText)
    layout = QVBoxLayout()
    layout.addWidget(self.label)
    layout.addItem(self.spacer)
    layout.addWidget(self.lineEdit)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.setLayout(layout)

  def sendText(self):
    self.textChanged.emit()

  def getLabel(self):
    return self.label

  def getLineEdit(self):
    return self.lineEdit

  def getText(self):
    return self.lineEdit.text()
  
  def setPlaceholderText(self, text: str):
    self.lineEdit.setPlaceholderText(text)

  def setText(self, text: str):
    self.lineEdit.setText(text) 
  
  def clear(self):
    self.lineEdit.clear()

  