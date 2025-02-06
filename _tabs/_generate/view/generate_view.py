from PyQt6.QtWidgets import QWidget, QDialog, QFileDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget
from _tabs._generate.viewmodel.generate_viewmodel import GenerateViewModel
from _widgets.labeled_line_edit import LabeledLineEdit
from _widgets.labeled_dropdown import LabeledDropdown
from _widgets.labeled_button import LabeledButton
from _modals.image_select_modal import ImageSelectModal
from PyQt6.QtCore import Qt, QTimer
import os


class GenerateView(QWidget):
  def __init__(self, viewModel: GenerateViewModel):
    super().__init__()
    self._viewModel = viewModel
    self.lastUploadDir: str = ""
    self.lastDownloadDir: str = ""
    self._viewModel.clientLoaded.connect(self.updateOnClientLoad)
    self._viewModel.topicLoaded.connect(self.updateOnTopicLoad)
    self._viewModel.htmlGenerated.connect(self.updateOnHTMLGenerate)
    self.initUI()
    self._viewModel.initData.connect(self.updateOnInit)
    self._viewModel.startData()

  def initUI(self):

    # Initialize the Title for the tab
    self.setWindowTitle('Client')  # Window title

    # Initialize the main layout for the tab
    self.layout = QVBoxLayout()

    # Initialize the layout for the upload and client dropdown
    self.uploadLayout = QHBoxLayout()

    # Initialize and add upload button and client dropdown to the upload layout
    self.uploadButton = LabeledButton('Docx', 'Upload')
    self.uploadButton.clicked.connect(self.uploadClick)
    self.uploadButton.setToolTip("Upload a DOCX file to generate an HTML file")
    self.uploadLayout.addWidget(self.uploadButton)
    self.clientCombo = LabeledDropdown('Client')
    self.clientCombo.currentTextChanged.connect(self._viewModel.loadClient)
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
    self.manualLinkOverride = LabeledLineEdit('Link Override', "https://www.client.com")
    self.manualGenerateButton = QPushButton('Generate')
    self.manualGenerateButton.clicked.connect(lambda: self.generateClick(False))
    self.manualGenerateButton.setEnabled(False)

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
    self.automaticTopicCombo.currentTextChanged.connect(lambda: self._viewModel.loadTopic(self.automaticTopicCombo.getCurrentText()))
    self.automaticButtonOverride = LabeledLineEdit('Button Override', "View Inventory")
    self.automaticLinkOverride = LabeledLineEdit('Link Override', "https://www.client.com")
    self.automaticGenerateButton = QPushButton('Generate')
    self.automaticGenerateButton.setEnabled(False)

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

  def generateClick(self, autoSelect: bool):
    self.manualGenerateButton.setEnabled(False)
    self.automaticGenerateButton.setEnabled(False)
    self.manualGenerateButton.setText("Generating...")
    self.automaticGenerateButton.setText("Generating...")

    if not autoSelect:
      dialog = ImageSelectModal(self._viewModel.getImgsNeeded())
      dialog.exec()
      if dialog.result() != QDialog.DialogCode.Accepted:
        self.manualGenerateButton.setEnabled(True)
        self.automaticGenerateButton.setEnabled(True)
        self.manualGenerateButton.setText("Generated!")
        self.automaticGenerateButton.setText("Generated!")
        QTimer.singleShot(1500, lambda: self.manualGenerateButton.setText("Generate"))
        QTimer.singleShot(1500, lambda: self.automaticGenerateButton.setText("Generate"))
        return
      altText = dialog.getAltText()
      imageSrcs = dialog.getImageList()
      downloadPath, _ = QFileDialog.getSaveFileName(self, 'Download File', self.lastDownloadDir, '*.html')
      if not downloadPath:
        self.manualGenerateButton.setEnabled(True)
        self.automaticGenerateButton.setEnabled(True)
        self.manualGenerateButton.setText("Failed!")
        self.automaticGenerateButton.setText("Failed!")
        QTimer.singleShot(1500, lambda: self.manualGenerateButton.setText("Generate"))
        QTimer.singleShot(1500, lambda: self.automaticGenerateButton.setText("Generate"))
        return
      self.lastDownloadDir = os.path.dirname(downloadPath)
      self._viewModel.generateHTML(autoSelect, imageSrcs, altText, self.manualButtonOverride.getText(), self.manualLinkOverride.getText(), downloadPath, downloadPath)
      self.manualGenerateButton.setEnabled(True)
      self.automaticGenerateButton.setEnabled(True)
      self.manualGenerateButton.setText("Generated!")
      self.automaticGenerateButton.setText("Generated!")
      QTimer.singleShot(1500, lambda: self.manualGenerateButton.setText("Generate"))
      QTimer.singleShot(1500, lambda: self.automaticGenerateButton.setText("Generate"))
      return

    self.manualGenerateButton.setEnabled(True)
    self.automaticGenerateButton.setEnabled(True)
    self.manualGenerateButton.setText("Generated!")
    self.automaticGenerateButton.setText("Generated!")
    QTimer.singleShot(1500, lambda: self.manualGenerateButton.setText("Generate"))
    QTimer.singleShot(1500, lambda: self.automaticGenerateButton.setText("Generate"))

  def uploadClick(self):
    self.uploadButton.button.setText("Uploading...")
    self.uploadButton.setEnabled(False)
    uploadPath, _ = QFileDialog.getOpenFileName(self, 'Upload File', self.lastUploadDir, '*.docx')
    if uploadPath:
      self.lastUploadDir = os.path.dirname(uploadPath)
      fileName = os.path.basename(uploadPath)
      self._viewModel.uploadDocx(uploadPath)
      self.uploadButton.setToolTip(fileName)
      self.uploadButton.button.setText("Uploaded!")
      self.uploadButton.setEnabled(True)
      self.manualGenerateButton.setEnabled(True)
      self.automaticGenerateButton.setEnabled(True)
      QTimer.singleShot(1500, lambda: self.uploadButton.button.setText("Upload"))
      return
    self.uploadButton.setEnabled(True)
    self.uploadButton.button.setText("Failed!")
    QTimer.singleShot(1500, lambda: self.uploadButton.button.setText("Upload"))

  def updateOnClientLoad(self, currentClient: str, topicList: list[str]):
    self.clientCombo.setCurrentText(currentClient)
    self.manualLinkOverride.setText("")
    self.automaticLinkOverride.setText("")
    self.manualButtonOverride.setText("")
    self.automaticButtonOverride.setText("")
    self.automaticTopicCombo.blockSignals(True)
    self.automaticTopicCombo.clear()
    self.automaticTopicCombo.blockSignals(False)
    self.automaticTopicCombo.addItems(topicList)

  def updateOnTopicLoad(self, topicLink: str):
    self.automaticLinkOverride.setText(topicLink)
    self.automaticButtonOverride.setText("")

  def updateOnHTMLGenerate(self, success: bool):
    if success:
      self.manualGenerateButton.setEnabled(True)
      self.automaticGenerateButton.setEnabled(True)
      self.manualGenerateButton.setText("Generated!")
      self.automaticGenerateButton.setText("Generated!")
      QTimer.singleShot(1500, lambda: self.manualGenerateButton.setText("Generate"))
      QTimer.singleShot(1500, lambda: self.automaticGenerateButton.setText("Generate"))
    else: 
      self.manualGenerateButton.setEnabled(True)
      self.automaticGenerateButton.setEnabled(True)
      self.manualGenerateButton.setText("Failed!")
      self.automaticGenerateButton.setText("Failed!")
      QTimer.singleShot(1500, lambda: self.manualGenerateButton.setText("Generate"))
      QTimer.singleShot(1500, lambda: self.automaticGenerateButton.setText("Generate"))
    
  def updateOnInit(self, clientList: list[str], topicList: list[str]):
    self.clientCombo.clear()
    self.clientCombo.addItems(clientList)
    self.automaticTopicCombo.blockSignals(True)
    self.automaticTopicCombo.clear()
    self.automaticTopicCombo.blockSignals(False)
    self.automaticTopicCombo.addItems(topicList)