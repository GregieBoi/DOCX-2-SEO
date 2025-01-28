from PyQt6.QtWidgets import QWidget,QLabel, QLineEdit, QVBoxLayout
from PyQt6.QtCore import Qt

class LabeledLineEdit(QWidget):
  def __init__(self, labelText, placeholderText=None, parent=None):
    super().__init__(parent)
    self.label = QLabel(labelText)
    self.lineEdit = QLineEdit()
    if placeholderText:
      self.lineEdit.setText(placeholderText)
    layout = QVBoxLayout()
    layout.addWidget(self.label)
    layout.addWidget(self.lineEdit)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.setLayout(layout)

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

  