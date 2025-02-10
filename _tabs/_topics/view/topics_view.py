from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from _tabs._topics.viewmodel.topics_viewmodel import TopicsViewModel
from _modals.destructive_modal import DestructiveModal
from _widgets.labeled_line_edit import LabeledLineEdit
from _widgets.labeled_dropdown import LabeledDropdown
from _widgets.topic_section import TopicSections

class TopicsView(QWidget):
  def __init__(self, viewModel: TopicsViewModel):
    super().__init__()
    self._viewModel = viewModel
    self._viewModel.clientListChanged.connect(self.updateOnClientListChange)
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
    self.clientCombo.currentTextChanged.connect(self.canDelete)
    self.clientCombo.currentTextChanged.connect(self.canSave)
    self.topicCombo = LabeledDropdown('Topic')
    self.topicCombo.currentTextChanged.connect(self._viewModel.loadTopic)
    self.topicCombo.currentTextChanged.connect(self.canDelete)
    self.topicNameLineEdit = LabeledLineEdit('Topic Name', 'New Topic')
    self.topicNameLineEdit.textChanged.connect(self.canSave)
    self.topicLinkLineEdit = LabeledLineEdit('Topic Redirect Link', 'https://www.example.com/topic')
    self.topicLinkLineEdit.textChanged.connect(self.canSave)

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
    self.saveButton = QPushButton('Save Topic')
    self.saveButton.clicked.connect(lambda: self.saveClick(self.topicNameLineEdit.getText(), self.topicLinkLineEdit.getText(), self.heroSection.fetch_links(), self.techSection.fetch_links(), self.interiorSection.fetch_links(), self.miscSection.fetch_links()))
    self.saveButton.setEnabled(False)
    self.deleteButton = QPushButton('Delete')
    self.deleteButton.clicked.connect(self.deleteClick)
    self.deleteButton.setEnabled(False)
    self.deleteButton.setObjectName('destructiveButton')

    # add the buttons to the button layout
    self.buttonLayout.addWidget(self.saveButton)
    self.buttonLayout.addWidget(self.deleteButton)

    # set the alignment of the button layout and add it to the layout
    self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    self.layout.addLayout(self.buttonLayout)

    self.setLayout(self.layout)  # Set the layout to the widget

  def canSave(self):
    client = self.clientCombo.getCurrentText()
    name = self.topicNameLineEdit.getText()
    link = self.topicLinkLineEdit.getText()
    whyNot = ""
    if client in [None, '']:
      whyNot += "You must select a client \n"

    if name.isspace() or name == "":
      whyNot += "You must enter a name for the topic \n"
    elif name == "New Topic":
      whyNot += "You cannot use the name 'New Topic' \n"
    
    if link.isspace() or link == "":
      whyNot += "You must enter a link for the topic \n"
    elif link.startswith("http://") == False and link.startswith("https://") == False:
      whyNot += "You must enter a valid link for the topic \n"

    if whyNot:
      self.saveButton.setEnabled(False)
      self.saveButton.setToolTip(whyNot[:-2])
      return
    
    self.saveButton.setEnabled(True)
    self.saveButton.setToolTip("")

  def canDelete(self):
    if self.topicCombo.getCurrentText() in ["New Topic", "", None]:
      self.deleteButton.setEnabled(False)
      self.deleteButton.setToolTip("You can only delete saved topics")
      return
    
    self.deleteButton.setEnabled(True)
    self.deleteButton.setToolTip("")

  def saveClick(self, topicName, topicLink, topicHeroSrcs, topicTechSrcs, topicInteriorSrcs, topicMiscSrcs):
    
    self.saveButton.setEnabled(False)
    self.saveButton.setText("Saving...")

    if (topicName != self.topicCombo.getCurrentText()) and topicName in self._viewModel.getTopicList():
      warning = "A topic with the name " + topicName + " already exists. Would you like to overwrite it?"
      destructiveButtonText = "Overwrite"
      dialog = DestructiveModal(warning, destructiveButtonText)
      dialog.exec()
      self.saveButton.setEnabled(False)
      self.saveButton.setText("Saving...")

      if dialog.result() == QDialog.DialogCode.Accepted:
        self._viewModel.saveTopic(topicName, topicLink, topicHeroSrcs, topicTechSrcs, topicInteriorSrcs, topicMiscSrcs)
        self.saveButton.setEnabled(True)
        self.saveButton.setText("Saved!")
        QTimer.singleShot(1500, lambda: self.saveButton.setText("Save Topic"))
        return
      self.saveButton.setEnabled(True)
      self.saveButton.setText("Cancelled!")
      QTimer.singleShot(1500, lambda: self.saveButton.setText("Save Topic"))
      return

    self._viewModel.saveTopic(topicName, topicLink, topicHeroSrcs, topicTechSrcs, topicInteriorSrcs, topicMiscSrcs)
    self.saveButton.setEnabled(True)
    self.saveButton.setText("Saved!")
    QTimer.singleShot(1500, lambda: self.saveButton.setText("Save Topic"))

  def deleteClick(self):
    self.deleteButton.setEnabled(False)
    self.deleteButton.setText("Deleting...")
    warning = "Are you sure you want to delete " + self.topicCombo.getCurrentText() + " from the topic list? This action cannot be undone."
    destructiveButtonText = "Delete"
    dialog = DestructiveModal(warning, destructiveButtonText)
    dialog.exec()
    self.deleteButton.setEnabled(False)
    self.deleteButton.setText("Deleting...")

    if dialog.result() == QDialog.DialogCode.Accepted:
      self._viewModel.deleteTopic()
      self.deleteButton.setText("Deleted!")
      QTimer.singleShot(1500, lambda: self.deleteButton.setText("Delete"))
      return
    
    self.deleteButton.setEnabled(True)
    self.deleteButton.setText("Cancelled!")
    QTimer.singleShot(1500, lambda: self.deleteButton.setText("Delete"))
    
  def updateOnSave(self, topicName, topicList):
    self.topicCombo.clear()
    self.topicCombo.addItems(topicList)
    self.topicCombo.setCurrentText(topicName)
    self.topicNameLineEdit.setText(topicName)

  def updateOnDelete(self, topicList):
    self.topicCombo.clear()
    self.topicCombo.addItems(topicList)
    self.topicCombo.setCurrentText("New Topic" if self.clientCombo.getCurrentText() not in ["", None] else "")

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
    if currentClient not in [None, ""]:
      self.topicCombo.addItems(topicList)
    self.topicCombo.setCurrentText("New Topic")

  def updateOnInit(self, clientList, topicList):
    self.topicCombo.clear()
    self.clientCombo.clear()
    self.clientCombo.addItems(clientList)

  def updateOnClientListChange(self, clientList):
    self.clientCombo.blockSignals(True)
    self.clientCombo.clear()
    self.clientCombo.addItems(clientList)
    if self._viewModel.getCurrentClient() in clientList:
      self.clientCombo.setCurrentText(self._viewModel.getCurrentClient())
    else:
      self.clientCombo.setCurrentText(clientList[0] if clientList else '')
      self._viewModel.loadClient(self.clientCombo.getCurrentText())
    self.clientCombo.blockSignals(False)