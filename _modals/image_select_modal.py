from PyQt6.QtWidgets import QDialog, QSizePolicy, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog
from PyQt6.QtCore import Qt

class ImageSelectModal(QDialog):
  def __init__(self, numImages: int):
    super().__init__()
    self.numImages = numImages
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Image Srcs')
    self.setWindowModality(Qt.WindowModality.ApplicationModal)
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding)

    self.layout = QVBoxLayout()
    self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.setLayout(self.layout)

    self.altText = QLineEdit()
    self.altText.setPlaceholderText('Alt Text')
    self.layout.addWidget(self.altText)

    self.imageList = []
    for i in range(self.numImages):
      self.imageList.append(QLineEdit())
      self.imageList[i].setPlaceholderText('Image ' + str(i + 1))
      self.layout.addWidget(self.imageList[i])

    self.submitButton = QPushButton('Submit')
    self.submitButton.clicked.connect(self.accept)
    self.layout.addWidget(self.submitButton)

    self.cancelButton = QPushButton('Cancel')
    self.cancelButton.clicked.connect(self.reject)
    self.layout.addWidget(self.cancelButton)
    self.layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

  def getAltText(self):
    return self.altText.text()

  def getImageList(self):
    return [image.text() for image in self.imageList]