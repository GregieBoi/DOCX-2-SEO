from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget
from _widgets.labeled_line_edit import LabeledLineEdit
from _widgets.labeled_dropdown import LabeledDropdown
from _widgets.labeled_button import LabeledButton
from PyQt6.QtCore import Qt


class GenerateView(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.initUI()

  def initUI(self):

    # Initialize the Title for the tab
    self.setWindowTitle('Client')  # Window title

    # Initialize the main layout for the tab
    self.layout = QVBoxLayout()

    # Initialize the layout for the upload and client dropdown
    self.uploadLayout = QHBoxLayout()

    # Initialize and add upload button and client dropdown to the upload layout
    self.uploadButton = LabeledButton('Docx', 'Upload')
    self.uploadLayout.addWidget(self.uploadButton)
    self.clientCombo = LabeledDropdown('Client', ["Client 1", "Client 2", "Client 3"])
    self.uploadLayout.addWidget(self.clientCombo)

    # set the alignment of the upload layout and add it to the main layout
    self.uploadLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    self.layout.addLayout(self.uploadLayout)
  
    # Initialize the tabs for Manual and Automatic modes
    self.tabs = QTabWidget()
    self.layout.addWidget(self.tabs)

    # Initialize the manual tab and its layout
    self.manualTab = QWidget()
    self.manualTabLayout = QVBoxLayout()

    # create the button override, link override, and button widgets for manual
    self.manualButtonOverride = LabeledLineEdit('Button Override', "View Inventory")
    self.manualLinkOverride = LabeledLineEdit('Link Override')
    self.manualGenerateButton = QPushButton('Generate')

    # add the widgets to the manual tab layout
    self.manualTabLayout.addWidget(self.manualButtonOverride)
    self.manualTabLayout.addWidget(self.manualLinkOverride)
    self.manualTabLayout.addWidget(self.manualGenerateButton)

    # set the manual tab layout alignment and add it to the manual tab
    self.manualTabLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.manualTab.setLayout(self.manualTabLayout)

    # add the manual tab to the tabs
    self.tabs.addTab(self.manualTab, 'Manual')

    # Initialize the automatic tab and its layout
    self.automaticTab = QWidget()
    self.automaticTabLayout = QVBoxLayout()

    # create the topic dropdown, button override, link override, and button widgets for automatic
    self.automaticTopicCombo = LabeledDropdown('Topic')
    self.automaticButtonOverride = LabeledLineEdit('Button Override', "View Inventory")
    self.automaticLinkOverride = LabeledLineEdit('Link Override')
    self.automaticGenerateButton = QPushButton('Generate')

    # add the widgets to the automatic tab layout
    self.automaticTabLayout.addWidget(self.automaticTopicCombo)
    self.automaticTabLayout.addWidget(self.automaticButtonOverride)
    self.automaticTabLayout.addWidget(self.automaticLinkOverride)
    self.automaticTabLayout.addWidget(self.automaticGenerateButton)

    # set the automatic tab layout alignment and add it to the automatic tab
    self.automaticTabLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.automaticTab.setLayout(self.automaticTabLayout)

    # add the automatic tab to the tabs
    self.tabs.addTab(self.automaticTab, 'Automatic')

    # set the main layout to the widget
    self.setLayout(self.layout)