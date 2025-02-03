from PyQt6.QtCore import QObject, pyqtSignal
from _tabs._client.model.client_model import ClientModel

# responsibilites of the client viewmodel
# 1. Connect the signals from the model to the view
# 2. Provide a way to update the model from the view
# 3. Provide a way to update the view from the model

# signals and outcomes
# 1. Client Saved - emit the name of the client
#    - update the model to have the new data to be saved
#    - update the view to show the selected client as the saved client
# 2. Client Deleted - emit nothing (since this is just a reset signal)
#    - update the model to have no new data
#    - update the view to show the updated client list and the selected 
#      client as the new client option
# 3. Client Loaded - emit the name, button, style, and wrapper of the client
#    - update the model to have the clientName to load
#    - update the view to should the newly selected client
# 4. Client Updated - emit the name of the client
#    - update the model to have the new data to be saved
#    - update the view to show the updated client list and the selected 
#      client as the updated client 
#      (only really applicable to name changes)

class ClientViewModel(QObject):
  clientSaved = pyqtSignal(str, list)
  clientDeleted = pyqtSignal(list)
  clientLoaded = pyqtSignal(str, str, str, str, str)
  clientUpdated = pyqtSignal(str, list)
  initClients = pyqtSignal(list)

  def __init__(self, model: ClientModel):
    super().__init__()
    self._model = model

  def saveClient(self, clientName, clientButton, clientStyle, clientWrapper):
    self._model.setClientName(clientName)
    self._model.setClientButton(clientButton)
    self._model.setClientStyle(clientStyle)
    self._model.setClientWrapper(clientWrapper)
    self._model.saveClient()
    self.clientSaved.emit(self._model.getClientName(), self._model.getClientList())

  def deleteClient(self):
    self._model.deleteClient()
    self.clientDeleted.emit(self._model.getClientList())

  def loadClient(self, clientName):
    self._model.loadClient(clientName)
    self.clientLoaded.emit(self._model.getCurrentClient(), self._model.getClientName(), self._model.getClientButton(), self._model.getClientStyle(), self._model.getClientWrapper())

  def updateClient(self, clientName, clientButton, clientStyle, clientWrapper):
    self._model.setClientName(clientName)
    self._model.setClientButton(clientButton)
    self._model.setClientStyle(clientStyle)
    self._model.setClientWrapper(clientWrapper)
    self._model.updateClient()
    self.clientUpdated.emit(self._model.getClientName(), self._model.getClientList())

  def startClients(self):
    self.initClients.emit(self._model.getClientList())

  def getClientList(self):
    return self._model.getClientList()