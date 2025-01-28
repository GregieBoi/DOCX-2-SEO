from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt

class LabeledTextEdit(QWidget):
  def __init__(self, labelText, placeholderText=None, parent=None):
    super().__init__(parent)
    self.label = QLabel(labelText)
    self.textEdit = QTextEdit()
    if placeholderText:
      self.textEdit.setPlaceholderText(placeholderText)
    layout = QVBoxLayout()
    layout.addWidget(self.label)
    layout.addWidget(self.textEdit)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.setLayout(layout)

  def getLabel(self):
    return self.label

  def getTextEdit(self):
    return self.textEdit

  def getText(self):
    return self.textEdit.toPlainText()

  def setText(self, text: str):
    self.textEdit.setText(text)
  
  def clear(self):
    self.textEdit.clear()