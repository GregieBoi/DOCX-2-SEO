from PyQt6.QtWidgets import QSizePolicy,QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class DestructiveModal(QDialog):
  def __init__(self, warning: str, destructiveButtonText: str, parent=None):
    super().__init__()
    self.warning = warning
    self.destructiveButtonText = destructiveButtonText
    self.initUI()

  def initUI(self):
    self.setWindowTitle('')
    self.setWindowModality(Qt.WindowModality.ApplicationModal)
    self.setFixedWidth(200)
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding)

    self.layout = QVBoxLayout()
    self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    
    self.warningLabel = QLabel(self.warning)
    self.warningLabel.setContentsMargins(0, 0, 0, 0)
    self.warningLabel.setWordWrap(True)
    self.warningLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
    self.warningLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.layout.addWidget(self.warningLabel, stretch=100)

    self.buttonLayout = QHBoxLayout()
    self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
    self.buttonLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)

    self.cancelButton = QPushButton('Cancel')
    self.cancelButton.setFocusPolicy(Qt.FocusPolicy.NoFocus) 
    self.cancelButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    self.cancelButton.clicked.connect(self.reject)
    self.buttonLayout.addWidget(self.cancelButton)

    self.destructiveButton = QPushButton(self.destructiveButtonText)
    self.destructiveButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    self.destructiveButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    self.destructiveButton.setObjectName("destructiveButton")
    self.destructiveButton.clicked.connect(self.accept)
    self.buttonLayout.addWidget(self.destructiveButton)

    self.layout.addLayout(self.buttonLayout, stretch=0)
    self.layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)


    self.setLayout(self.layout)
