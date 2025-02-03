from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from _tabs._topics.viewmodel.topics_viewmodel import TopicsViewModel
from _widgets.labeled_line_edit import LabeledLineEdit
from _widgets.labeled_dropdown import LabeledDropdown
from _widgets.topic_section import TopicSections

class TopicsView(QWidget):
  def __init__(self, viewModel: TopicsViewModel):
    super().__init__()
    self._viewModel = viewModel
    self._viewModel.topicSaved.connect(self.updateOnSave)
    self._viewModel.topicDeleted.connect(self.updateOnDelete)
    self._viewModel.topicLoaded.connect(self.updateOnTopicLoad)
    self._viewModel.clientLoaded.connect(self.updateOnClientLoad)
    self.initUI()
    self._viewModel.initTopics.connect(self.updateOnInit)
    self._viewModel.startTopics()

  def initUI(self):
    self.setWindowTitle('Client')  # Window title
    self.layout = QVBoxLayout()  # Vertical layout

    # initialize topic selection layout
    self.topicSelectionLayout = QHBoxLayout()

    # create the client dropdown, topic dropdown, topic name line edit, and link to line edit
    self.clientCombo = LabeledDropdown('Client')
    self.clientCombo.currentTextChanged.connect(self._viewModel.loadClient)
    self.topicCombo = LabeledDropdown('Topic')
    self.topicCombo.currentTextChanged.connect(self._viewModel.loadTopic)
    self.topicNameLineEdit = LabeledLineEdit('Topic Name', 'New Topic')
    self.topicLinkLineEdit = LabeledLineEdit('Topic Redirect Link', 'https://www.example.com/topic')

    # add the widgets to the topic selection layout
    self.topicSelectionLayout.addWidget(self.clientCombo)
    self.topicSelectionLayout.addWidget(self.topicCombo)
    self.topicSelectionLayout.addWidget(self.topicNameLineEdit)
    self.topicSelectionLayout.addWidget(self.topicLinkLineEdit)

    # set the alignment of the topic selection layout and add it to the layout
    self.topicSelectionLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    self.layout.addLayout(self.topicSelectionLayout)

    # initialize the topic sections top layouts
    self.topicSectionsTopLayout = QHBoxLayout()
    self.topicSectionsBotLayout = QHBoxLayout()

    # create the topic sections
    self.heroSection = TopicSections('Hero Image Srcs')
    self.techSection = TopicSections('Tech Image Srcs')
    self.interiorSection = TopicSections('Interior Image Srcs')
    self.miscSection = TopicSections('Misc Image Srcs')

    # add the topic sections to the topic sections layouts
    self.topicSectionsTopLayout.addWidget(self.heroSection)
    self.topicSectionsTopLayout.addWidget(self.techSection)
    self.topicSectionsBotLayout.addWidget(self.interiorSection)
    self.topicSectionsBotLayout.addWidget(self.miscSection)

    # set the alignment of the topic sections layouts and add them to the layout
    self.topicSectionsTopLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    self.topicSectionsBotLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    self.layout.addLayout(self.topicSectionsTopLayout)
    self.layout.addLayout(self.topicSectionsBotLayout)

    # initalize the button layout
    self.buttonLayout = QHBoxLayout()

    # create the save and delete buttons
    self.saveButton = QPushButton('Save')
    self.saveButton.clicked.connect(lambda: self._viewModel.saveTopic(self.topicNameLineEdit.getText(), self.topicLinkLineEdit.getText(), self.heroSection.fetch_links(), self.techSection.fetch_links(), self.interiorSection.fetch_links(), self.miscSection.fetch_links()))
    #self.saveButton.setEnabled(False)
    self.deleteButton = QPushButton('Delete')
    self.deleteButton.clicked.connect(self._viewModel.deleteTopic)
    #self.deleteButton.setEnabled(False)
    self.deleteButton.setObjectName('destructiveButton')

    # add the buttons to the button layout
    self.buttonLayout.addWidget(self.saveButton)
    self.buttonLayout.addWidget(self.deleteButton)

    # set the alignment of the button layout and add it to the layout
    self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    self.layout.addLayout(self.buttonLayout)

    self.setLayout(self.layout)  # Set the layout to the widget
    
  def updateOnSave(self, topicName, topicList):
    self.topicCombo.clear()
    self.topicCombo.addItems(topicList)
    self.topicCombo.setCurrentText(topicName)
    self.topicNameLineEdit.setText(topicName)

  def updateOnDelete(self, topicList):
    self.topicCombo.clear()
    self.topicCombo.addItems(topicList)
    self.topicCombo.setCurrentText("New Topic")

  def updateOnTopicLoad(self, currentClient, selectedTopic, topicName, topicLink, topicHeroSrcs, topicTechSrcs, topicInteriorSrcs, topicMiscSrcs):
    self.heroSection.clear()
    self.techSection.clear()
    self.interiorSection.clear()
    self.miscSection.clear()
    
    self.clientCombo.setCurrentText(currentClient)
    self.topicCombo.setCurrentText(selectedTopic)
    self.topicNameLineEdit.setText(topicName)
    self.topicLinkLineEdit.setText(topicLink)
    self.heroSection.setSrcs(topicHeroSrcs)
    self.techSection.setSrcs(topicTechSrcs)
    self.interiorSection.setSrcs(topicInteriorSrcs)
    self.miscSection.setSrcs(topicMiscSrcs)

  def updateOnClientLoad(self, currentClient, topicList):
    self.clientCombo.setCurrentText(currentClient)
    self.topicCombo.clear()
    self.topicCombo.addItems(topicList)
    self.topicCombo.setCurrentText("New Topic")

  def updateOnInit(self, clientList, topicList):
    print(topicList)
    self.topicCombo.clear()
    self.clientCombo.clear()
    self.clientCombo.addItems(clientList)