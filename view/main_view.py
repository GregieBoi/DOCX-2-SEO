import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QPushButton
from _widgets.labeled_dropdown import LabeledDropdown
from model.main_model import MainModel
from _tabs._client.model.client_model import ClientModel
from _tabs._client.viewmodel.client_viewmodel import ClientViewModel
from _tabs._client.view.client_view import ClientView
from _tabs._generate.model.generate_model import GenerateModel
from _tabs._generate.viewmodel.generate_viewmodel import GenerateViewModel
from _tabs._generate.view.generate_view import GenerateView
from _tabs._topics.view.topics_view import TopicsView
from _tabs._topics.model.topics_model import TopicsModel
from _tabs._topics.viewmodel.topics_viewmodel import TopicsViewModel

class MainView(QWidget):
  def __init__(self, viewModel):
    super().__init__()
    self.setFixedSize(750, 750) # mess with size later
    self._viewModel = viewModel
    self._viewModel.countChanged.connect(self.updateLabel)  # Connect signal to the slot
    self.initUI()

  def initUI(self):
    self.setWindowTitle('DOCX-2-SEO')  # Window title
    self.layout = QVBoxLayout()
    self.tabs = QTabWidget()
    self.layout.addWidget(self.tabs)
    self.mainModel = MainModel()
    self.clientModel = ClientModel(self.mainModel)
    self.clientModelView = ClientViewModel(self.clientModel)
    self.clientTab = ClientView(self.clientModelView)
    self.tabs.addTab(self.clientTab, 'Client')
    self.generateModel = GenerateModel(self.mainModel)
    self.generateModelView = GenerateViewModel(self.generateModel)
    self.generateTab = GenerateView(self.generateModelView)
    self.tabs.addTab(self.generateTab, 'Generate')
    self.topicsModel = TopicsModel(self.mainModel)
    self.topicsModelView = TopicsViewModel(self.topicsModel)
    self.topicsTab = TopicsView(self.topicsModelView)
    self.tabs.addTab(self.topicsTab, 'Topics')
    self.setLayout(self.layout)  # Set the layout of the widget

  def updateLabel(self, count):
    self.label.setText(str(count))  # Update the label with the current count