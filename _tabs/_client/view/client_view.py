from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from _widgets.labeled_dropdown import LabeledDropdown
from _widgets.labeled_line_edit import LabeledLineEdit
from _widgets.labeled_textedit import LabeledTextEdit

class ClientView(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Client')  # Window title
    self.layout = QVBoxLayout()  # Vertical layout

    # initialize the layout for the client name and dropdown
    self.clientNameLayout = QHBoxLayout()

    # create the clientnamelineedit and clientdropdown widgets
    self.clientName = LabeledLineEdit('Client Name', "New Client")
    self.clientCombo = LabeledDropdown('Client', ["Client 1", "Client 2", "Client 3"])
    
    # add the widgets to the client name layout
    self.clientNameLayout.addWidget(self.clientName)
    self.clientNameLayout.addWidget(self.clientCombo)

    # set the alignment of the client name layout and add it to the layout
    self.clientNameLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    self.layout.addLayout(self.clientNameLayout)

    # create the client button text edit, client style text edit, and client wrapper text edit
    self.clientButton = LabeledTextEdit('Button HTML', '<a>Your Client Button</a>', 3)
    self.clientStyle = LabeledTextEdit('Style JSON', '{\n\t"style": "",\n\t"p": {\n\t\t"style": ""\n\t},\n\t"img": {\n\t\t"style": "",\n\t\t"width": ""\n\t},\n\t"td": {\n\t\t"style": ""\n\t}\n}', 13)
    self.clientWrapper = LabeledTextEdit('Wrapper HTML', '<div>\n\t<div>\n\t</div>\n</div>', 4)
    self.layout.addWidget(self.clientButton)
    self.layout.addWidget(self.clientStyle)
    self.layout.addWidget(self.clientWrapper)

    # create the button layour
    self.buttonLayout = QHBoxLayout()

    # create the buttons for the button layout
    self.saveButton = QPushButton('Save')
    self.saveButton.setEnabled(False)
    self.deleteButton = QPushButton('Delete')
    self.deleteButton.setEnabled(False)
    self.deleteButton.setObjectName('deleteButton')
    '''self.deleteButton.setStyleSheet("""
                                    QPushButton {
                                      background-color: red; 
                                      color: white; 
                                      border-radius: 5px; 
                                      padding-top: 1px; 
                                      padding-bottom: 3px; 
                                      padding-left: 12px; 
                                      padding-right: 12px; 
                                      margin-top: 2px;
                                    } 
                                    QPushButton:pressed {
                                      background-color: darkRed; 
                                      color: grey;
                                    }
                                    QPushButton:disabled {
                                      background-color: darkRed; 
                                      color: grey; 
                                    }
                                    """)'''
    

    # add the buttons to the button layout
    self.buttonLayout.addWidget(self.saveButton)
    self.buttonLayout.addWidget(self.deleteButton)

    # set the alignment of the button layout and add it to the layout
    self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    self.layout.addLayout(self.buttonLayout)

    self.setLayout(self.layout)  # Set the layout to the widget