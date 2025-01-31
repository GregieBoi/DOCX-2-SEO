from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from _widgets.labeled_line_edit import LabeledLineEdit
from _widgets.labeled_dropdown import LabeledDropdown
from _widgets.topic_section import TopicSections

class TopicsView(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Client')  # Window title
    self.layout = QVBoxLayout()  # Vertical layout

    # initialize topic selection layout
    self.topicSelectionLayout = QHBoxLayout()

    # create the client dropdown, topic dropdown, topic name line edit, and link to line edit
    self.clientCombo = LabeledDropdown('Client')
    self.topicCombo = LabeledDropdown('Topic')
    self.topicNameLineEdit = LabeledLineEdit('Topic Name')
    self.topicLinkLineEdit = LabeledLineEdit('Topic Redirect Link')

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
    self.saveButton.setEnabled(False)
    self.deleteButton = QPushButton('Delete')
    self.deleteButton.setEnabled(False)
    self.deleteButton.setObjectName('destructiveButton')

    # add the buttons to the button layout
    self.buttonLayout.addWidget(self.saveButton)
    self.buttonLayout.addWidget(self.deleteButton)

    # set the alignment of the button layout and add it to the layout
    self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    self.layout.addLayout(self.buttonLayout)

    self.setLayout(self.layout)  # Set the layout to the widget