from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

class LabeledTextEdit(QWidget):
  textChanged = pyqtSignal()

  def __init__(self, labelText: str, placeholderText: str=None, lines: int=None, parent=None):
    super().__init__(parent)
    self.label = QLabel(labelText)
    self.textEdit = QTextEdit()
    self.textEdit.textChanged.connect(self.sendText)
    if placeholderText:
      self.textEdit.setPlaceholderText(placeholderText)
    if lines:
      metrics = self.textEdit.fontMetrics()
      line_height = metrics.lineSpacing()
      self.textEdit.setFixedHeight(lines * line_height + 10)
      tab_width = 2 * metrics.horizontalAdvance(' ')
      self.textEdit.setTabStopDistance(tab_width)
    layout = QVBoxLayout()
    layout.addWidget(self.label)
    layout.addWidget(self.textEdit)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.setLayout(layout)

  def sendText(self):
    self.textChanged.emit()

  def getLabel(self):
    return self.label

  def getTextEdit(self):
    return self.textEdit

  def getText(self):
    return self.textEdit.toPlainText()

  def setText(self, text: str):
    self.textEdit.setPlainText(text)
  
  def clear(self):
    self.textEdit.clear()