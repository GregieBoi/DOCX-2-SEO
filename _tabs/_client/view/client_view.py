from PyQt6.QtWidgets import QWidget, QDialog, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from _tabs._client.viewmodel.client_viewmodel import ClientViewModel
from _widgets.labeled_dropdown import LabeledDropdown
from _widgets.labeled_line_edit import LabeledLineEdit
from _widgets.labeled_textedit import LabeledTextEdit
from _modals.destructive_modal import DestructiveModal
from bs4 import BeautifulSoup
import json

class ClientView(QWidget):
  def __init__(self, viewModel: ClientViewModel):
    super().__init__()
    self._viewModel = viewModel
    self._viewModel.clientSaved.connect(self.updateOnSave)
    self._viewModel.clientDeleted.connect(self.updateOnDelete)
    self._viewModel.clientLoaded.connect(self.updateOnLoad)
    self._viewModel.clientUpdated.connect(self.updateOnUpdate)
    self.initUI()
    self._viewModel.initClients.connect(self.updateOnInit)
    self._viewModel.startClients()

  def initUI(self):
    self.setWindowTitle('Client')  # Window title
    self.layout = QVBoxLayout()  # Vertical layout

    # initialize the layout for the client name and dropdown
    self.clientNameLayout = QHBoxLayout()

    # create the clientnamelineedit and clientdropdown widgets
    self.clientName = LabeledLineEdit('Client Name', "New Client")
    self.clientName.textChanged.connect(self.canSave)
    self.clientCombo = LabeledDropdown('Client', [])
    self.clientCombo.currentTextChanged.connect(lambda: self._viewModel.loadClient(self.clientCombo.getCurrentText()))
    self.clientCombo.currentTextChanged.connect(self.canUpdateOrDelete)
    
    # add the widgets to the client name layout
    self.clientNameLayout.addWidget(self.clientName)
    self.clientNameLayout.addWidget(self.clientCombo)

    # set the alignment of the client name layout and add it to the layout
    self.clientNameLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    self.layout.addLayout(self.clientNameLayout)

    # create the client button text edit, client style text edit, and client wrapper text edit
    self.clientButton = LabeledTextEdit('Button HTML', '<a>Your Client Button</a>', 3)
    self.clientButton.textChanged.connect(self.canSave)
    self.clientStyle = LabeledTextEdit('Style JSON', '{\n\t"style": "",\n\t"p": {\n\t\t"style": ""\n\t},\n\t"img": {\n\t\t"style": "",\n\t\t"width": ""\n\t},\n\t"td": {\n\t\t"style": ""\n\t}\n}', 13)
    self.clientStyle.textChanged.connect(self.canSave)
    self.clientWrapper = LabeledTextEdit('Wrapper HTML', '<div>\n\t<div>\n\t</div>\n</div>', 4)
    self.clientWrapper.textChanged.connect(self.canSave)
    self.layout.addWidget(self.clientButton)
    self.layout.addWidget(self.clientStyle)
    self.layout.addWidget(self.clientWrapper)

    # create the button layour
    self.buttonLayout = QHBoxLayout()

    # create the buttons for the button layout
    self.saveButton = QPushButton('Save Client')
    self.saveButton.setEnabled(False)
    self.saveButton.clicked.connect(lambda: self.saveClick(self.clientName.getText(), self.clientButton.getText(), self.clientStyle.getText(), self.clientWrapper.getText()))
    self.deleteButton = QPushButton('Delete')
    self.deleteButton.setEnabled(False)
    self.deleteButton.setObjectName('destructiveButton')
    self.deleteButton.clicked.connect(self.deleteClick)

    # add the buttons to the button layout
    self.buttonLayout.addWidget(self.saveButton)
    self.buttonLayout.addWidget(self.deleteButton)

    # set the alignment of the button layout and add it to the layout
    self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    self.layout.addLayout(self.buttonLayout)

    # check initialize the canSave and canUpdateOrDelete status
    self.canSave()
    self.canUpdateOrDelete()

    self.setLayout(self.layout)  # Set the layout to the widget

  # checks if the client attributes are valid and enables or disables the save button
  def canSave(self):
    name = self.clientName.getText()
    button = self.clientButton.getText()
    buttonSoup = BeautifulSoup(button, 'html.parser')
    style = self.clientStyle.getText()
    
    wrapper = self.clientWrapper.getText()
    wrapperSoup = BeautifulSoup(wrapper, 'html.parser')

    whyNot = ""
    if name.isspace() or name == "":
      whyNot += "You must enter a name for the client \n"
    elif name == "New Client":
      whyNot += "You cannot use the name 'New Client' \n"
    
    if button.isspace() or button == "":
      whyNot += "You must enter a button for the client \n"
    elif buttonSoup.find("a") == None:
      whyNot += "You must enter a button with an anchor tag \n"

    if style.isspace() or style == "":
      whyNot += "You must enter a style for the client \n"
    else:
      try:
        json.loads(style)
      except:
        whyNot += "You must enter valid JSON for the style \n"

    if wrapper.isspace() or wrapper == "":
      whyNot += "You must enter a wrapper for the client \n"
    elif wrapperSoup.find("div") == None:
      whyNot += "You must enter a wrapper with two div tags \n"
    elif wrapperSoup.find("div").find("div") == None:
      whyNot += "You must enter a wrapper with two div tags (one inside the other) \n"

    if whyNot:
      self.saveButton.setEnabled(False)
      self.saveButton.setToolTip(whyNot[:-2])
      return
    
    self.saveButton.setEnabled(True)
    self.saveButton.setToolTip("")

  # updates the client combo on init
  def updateOnInit(self, clientList):
    self.clientCombo.clear()
    self.clientCombo.addItems(clientList)

  # checks if the selected client is an existing client and enables or disables the delete button
  def canUpdateOrDelete(self):
    if self.clientCombo.getCurrentText() == "New Client":
      self.clientName.setPlaceholderText("New Client")
      self.deleteButton.setEnabled(False)
      self.deleteButton.setToolTip("You can only delete saved clients")
      return
    
    self.clientName.setPlaceholderText(self.clientCombo.getCurrentText())
    self.deleteButton.setEnabled(True)
    self.deleteButton.setToolTip("")

  # handle update confirmation if conflict and send data to viewmodel for saving or updating
  def saveClick(self, clientName, clientButton, clientStyle, clientWrapper):
    if self.clientCombo.getCurrentText() == "New Client":
      self.saveButton.setEnabled(False)
      self.saveButton.setText("Saving...")
      if self.clientName.getText().lower() in [x.lower() for x in self._viewModel.getClientList()]:
        warning = "A client with the name " + self.clientName.getText() + " already exists. Would you like to replace the existing client? This action cannot be undone!"
        destructiveButtonText = "Replace"
        dialog = DestructiveModal(warning, destructiveButtonText)
        dialog.exec()

        if dialog.result() == QDialog.DialogCode.Accepted:
          clients = self._viewModel.getClientList()
          for i, client in enumerate(clients):
            if client.lower() == self.clientName.getText().lower():
              clientName = clients[i]
          self._viewModel.saveClient(clientName, clientButton, clientStyle, clientWrapper)
          self.saveButton.setEnabled(True)
          self.saveButton.setText("Saved!")
          QTimer.singleShot(1500, lambda: self.saveButton.setText("Save Client"))
          return
        else:
          self.saveButton.setEnabled(True)
          self.saveButton.setText("Cancelled!")
          QTimer.singleShot(1500, lambda: self.saveButton.setText("Save Client"))
          return
      self.saveButton.setEnabled(True)
      self.saveButton.setText("Saved!")
      QTimer.singleShot(1500, lambda: self.saveButton.setText("Save Client"))
      self._viewModel.saveClient(clientName, clientButton, clientStyle, clientWrapper)
      return

    if (self.clientName.getText().lower() != self.clientCombo.getCurrentText().lower()) and (self.clientName.getText().lower() in [x.lower() for x in self._viewModel.getClientList()]):
      warning = "A client with the name " + self.clientName.getText() + " already exists. Would you like to replace the existing client? This action cannot be undone!"
      destructiveButtonText = "Replace"
      dialog = DestructiveModal(warning, destructiveButtonText)
      dialog.exec()
      self.saveButton.setEnabled(False)
      self.saveButton.setText("Saving...")

      if dialog.result() == QDialog.DialogCode.Accepted:
        clients = self._viewModel.getClientList()
        for i, client in enumerate(clients):
          if client.lower() == self.clientName.getText().lower():
            clientName = clients[i]
        self._viewModel.updateClient(clientName, clientButton, clientStyle, clientWrapper)
        self.saveButton.setEnabled(True)
        self.saveButton.setText("Saved!")
        QTimer.singleShot(1500, lambda: self.saveButton.setText("Save Client"))
        return
      else:
        self.saveButton.setEnabled(True)
        self.saveButton.setText("Cancelled!")
        QTimer.singleShot(1500, lambda: self.saveButton.setText("Save Client"))
        return
      
    self.saveButton.setEnabled(True)
    self.saveButton.setText("Saved!")
    QTimer.singleShot(1500, lambda: self.saveButton.setText("Save Client"))
    self._viewModel.updateClient(clientName, clientButton, clientStyle, clientWrapper)

  # handle delete confirmation and send data to viewmodel for deleting
  def deleteClick(self):
    self.deleteButton.setEnabled(False)
    self.deleteButton.setText("Deleting...")
    warning = "Are you sure you want to delete " + self.clientCombo.getCurrentText() + " from the client list? This action cannot be undone."
    destructiveButtonText = "Delete"
    dialog = DestructiveModal(warning, destructiveButtonText)
    dialog.exec()

    if dialog.result() == QDialog.DialogCode.Accepted:
      self._viewModel.deleteClient()
      self.deleteButton.setText("Deleted!")
      QTimer.singleShot(1500, lambda: self.deleteButton.setText("Delete"))
      return
    
    self.deleteButton.setEnabled(True)
    self.deleteButton.setText("Cancelled!")
    QTimer.singleShot(1500, lambda: self.deleteButton.setText("Delete"))

  # update on save
  def updateOnSave(self, clientName, clientList):
    self.clientCombo.clear()
    self.clientCombo.addItems(clientList)
    self.clientCombo.setCurrentText(clientName)
    self.clientName.setText(clientName)

  # update on delete
  def updateOnDelete(self, clientList):
    self.clientCombo.clear()
    self.clientCombo.addItems(clientList)
    self.clientCombo.setCurrentText("New Client")

  # update on load
  def updateOnLoad(self, currentClient: str, clientName: str, clientButton: str, clientStyle: str, clientWrapper: str):
    self.clientCombo.setCurrentText(currentClient)
    self.clientName.setText(clientName)
    self.clientButton.setText(clientButton)
    self.clientStyle.setText(clientStyle)
    self.clientWrapper.setText(clientWrapper)

  # update on update
  def updateOnUpdate(self, clientName, clientList):
    self.clientCombo.clear()
    self.clientCombo.addItems(clientList)
    self.clientCombo.setCurrentText(clientName)
    self.clientName.setText(clientName)