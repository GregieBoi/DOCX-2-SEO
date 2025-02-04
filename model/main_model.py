from PyQt6.QtCore import QObject, pyqtSignal
import sys
import __main__
import os


# responsibilites of the main model
# 1. Store any data that is needed by multiple views to all for data to be shared
#    and updated efficiently
class MainModel(QObject):
  clientListChanged = pyqtSignal(list)

  def __init__(self):
    super().__init__()
    self.clientDirectory: str = self.findClientDirectory()
    self.clientList = self.fetchClientList()

  # get the client list
  def getClientList(self):
    return self.clientList

  # find the client directory
  def findClientDirectory(self):
    if getattr(sys, 'frozen', False):
      return os.path.join(os.path.dirname(sys.executable), 'CLIENTS')
    return os.path.join(os.path.dirname(__main__.__file__), 'CLIENTS')

  # fetch all clients from the client directory
  def fetchClientList(self):
    clients = []
    for entry in os.scandir(self.clientDirectory):
      if entry.is_dir():
        clients.append(entry.name)

    return sorted(clients)
  
  # refresh the client list
  def refreshClientList(self):
    self.clientList = self.fetchClientList()
    self.clientListChanged.emit(self.clientList)
    return self.clientList
