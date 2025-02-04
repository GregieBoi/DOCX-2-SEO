from PyQt6.QtCore import QObject
from model.main_model import MainModel
import sys
import os
import shutil
import __main__
import json

# responsibilites of the client model
# 1. Store the attributes of the selected client or a potential new client
# 2. Provide a way to save the attributes to an entry in a directory
# 3. Provide a way to load the attributes from an entry in a directory
# 4. Provide a way to fetch all possible clients from a directory
# 5. Delete a client from the directory

class ClientModel(QObject):
  def __init__(self, mainModel: MainModel):
    self._mainModel: MainModel = mainModel
    self.clientDirectory: str = self._mainModel.findClientDirectory()
    self.clientList: list[str] = ['New Client'] + self._mainModel.getClientList()
    self.clientName: str = ""
    self.currentClient: str = ""
    self.clientButton: str = ""
    self.clientStyle: str = ""
    self.clientWrapper: str = ""

  def setClientList(self, clientList: list[str]):
    self.clientList = ['New Client'].append(clientList)

  def getClientList(self):
    return self.clientList

  def setClientName(self, name: str):
    self.clientName = name
  
  def getClientName(self):
    return self.clientName
  
  def setCurrentClient(self, client: str):
    self.currentClient = client
  
  def getCurrentClient(self):
    return self.currentClient
  
  def setClientButton(self, button: str):
    self.clientButton = button
  
  def getClientButton(self):
    return self.clientButton
  
  def setClientStyle(self, style: str):
    self.clientStyle = style
  
  def getClientStyle(self):
    return self.clientStyle
  
  def setClientWrapper(self, wrapper: str):
    self.clientWrapper = wrapper
  
  def getClientWrapper(self):
    return self.clientWrapper
  
  # reset the client attributes
  def clear(self):
    self.clientName = ""
    self.currentClient = self.clientList[0]
    self.clientButton = ""
    self.clientStyle = ""
    self.clientWrapper = ""

  def refreshClientList(self):
    self.clientList = self.fetchClientList("refreshClientList")

  # find the main window directory
  def findMWD(self):
    if getattr(sys, 'frozen', False):
      return os.path.join(os.path.dirname(sys.executable), 'CLIENTS')
    return os.path.join(os.path.dirname(__main__.__file__), 'CLIENTS')

  # save the client attributes to a new directory
  def saveClient(self):
    # create a new directory with the name of the client
    newClientDir = os.path.join(self.clientDirectory, self.clientName)
    if not os.path.exists(newClientDir):
      os.mkdir(newClientDir)

    with open(os.path.join(newClientDir, 'topics.json'), 'w') as f:
      f.write('{}')
      f.close()
    with open(os.path.join(newClientDir, 'button.html'), 'w') as f:
      f.write(self.clientButton)
      f.close()
    with open(os.path.join(newClientDir, 'styles.json'), 'w') as f:
      styleJSON = json.loads(self.clientStyle)
      json.dump(styleJSON, f, indent=2)
      f.close()
    with open(os.path.join(newClientDir, 'wrapper.html'), 'w') as f:
      f.write(self.clientWrapper)
      f.close()

    # refresh the client list
    self.refreshClientList()

    # update the current client
    self.setCurrentClient(self.clientName)

  # load the client attributes from a directory
  def loadClient(self, clientName: str):
    # clear the client attributes
    self.clear()

    if clientName in ["New Client", "", None]:
      self.currentClient = "New Client"
      self.clientName = ""
      return

    # set the currentClient to the clientName
    self.currentClient = clientName
    self.clientName = clientName

    # read the client attributes from the directory and set the attributes
    with open(os.path.join(self.clientDirectory, clientName, 'button.html'), 'r') as f:
      self.clientButton = f.read()
      f.close()
    with open(os.path.join(self.clientDirectory, clientName, 'styles.json'), 'r') as f:
      self.clientStyle = f.read()
      f.close()
    with open(os.path.join(self.clientDirectory, clientName, 'wrapper.html'), 'r') as f:
      self.clientWrapper = f.read()
      f.close()

  # update the client attributes
  def updateClient(self):
    # check if currentClient is same as clientName
    if self.currentClient == self.clientName:
      with open(os.path.join(self.clientDirectory, self.currentClient, 'button.html'), 'w') as f:
        f.write(self.clientButton)
        f.close()
      with open(os.path.join(self.clientDirectory, self.currentClient, 'styles.json'), 'w') as f:
        styleJSON = json.loads(self.clientStyle)
        json.dump(styleJSON, f, indent=2)
        f.close()
      with open(os.path.join(self.clientDirectory, self.currentClient, 'wrapper.html'), 'w') as f:
        f.write(self.clientWrapper)
        f.close()
      return
    
    # if not create a new directory and delete the old one
    oldClientDir = os.path.join(self.clientDirectory, self.currentClient)
    newClientDir = os.path.join(self.clientDirectory, self.clientName)
    newClientName = self.clientName

    # create the updated client directory
    if not os.path.exists(newClientDir):
      os.mkdir(newClientDir)

    # save the client attributes as files to the new directory
    with open(os.path.join(oldClientDir, 'topics.json'), 'r') as r:
      with open(os.path.join(newClientDir, 'topics.json'), 'w') as w:
        w.write(r.read())
        w.close()
        r.close()
    with open(os.path.join(newClientDir, 'button.html'), 'w') as f:
      f.write(self.clientButton)
      f.close()
    with open(os.path.join(newClientDir, 'styles.json'), 'w') as f:
      styleJSON = json.loads(self.clientStyle)
      json.dump(styleJSON, f, indent=2)
      f.close()
    with open(os.path.join(newClientDir, 'wrapper.html'), 'w') as f:
      f.write(self.clientWrapper)
      f.close()

    # remove the old client directory
    shutil.rmtree(oldClientDir)

    # clear the client attributes
    self.refreshClientList()

    # change the current client name to the new client
    self.setCurrentClient(newClientName)

  # delete a client from the directory
  def deleteClient(self):
    # delete the client directory
    shutil.rmtree(os.path.join(self.clientDirectory, self.currentClient))

    # update the clientList and all data points
    self.clear()
    self.refreshClientList()
    return

  # fetch the list of clients from the directory
  def fetchClientList(self, caller: str):
    # read the client directories from the directory and append them to list
    clients = self._mainModel.refreshClientList()
    
    # return the list of clients
    return ['New Client'] + (clients)
