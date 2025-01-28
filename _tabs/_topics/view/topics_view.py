from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from _widgets.labeled_textedit import LabeledTextEdit

class TopicsView(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Client')  # Window title
    self.layout = QVBoxLayout()  # Vertical layout
    self.clientCombo = LabeledTextEdit('Client', "Client 1")
    self.layout.addWidget(self.clientCombo)
    self.setLayout(self.layout)  # Set the layout to the widget