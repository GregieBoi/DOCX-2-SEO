import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QPushButton
from _widgets.labeled_dropdown import LabeledDropdown
from _tabs._client.view.client_view import ClientView
from _tabs._generate.view.generate_view import GenerateView
from _tabs._topics.view.topics_view import TopicsView

class MainView(QWidget):
  def __init__(self, viewModel):
    super().__init__()
    # self.setFixedSize(600, 600) # mess with size later
    self._viewModel = viewModel
    self._viewModel.countChanged.connect(self.updateLabel)  # Connect signal to the slot
    self.initUI()

  def initUI(self):
    self.setWindowTitle('DOCX-2-SEO')  # Window title
    self.layout = QVBoxLayout()
    self.tabs = QTabWidget()
    self.layout.addWidget(self.tabs)
    self.clientTab = ClientView(self)
    self.tabs.addTab(self.clientTab, 'Client')
    self.generateTab = GenerateView(self)
    self.tabs.addTab(self.generateTab, 'Generate')
    self.topicsTab = TopicsView(self)
    self.tabs.addTab(self.topicsTab, 'Topics')
    self.setLayout(self.layout)  # Set the layout of the widget

  def updateLabel(self, count):
    self.label.setText(str(count))  # Update the label with the current count