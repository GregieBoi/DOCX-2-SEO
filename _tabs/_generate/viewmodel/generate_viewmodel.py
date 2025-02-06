from PyQt6.QtCore import QObject, pyqtSignal
import os
from _tabs._generate.model.generate_model import GenerateModel

class GenerateViewModel(QObject):
  clientLoaded = pyqtSignal(str, list)
  topicLoaded = pyqtSignal(str)
  clientListChanged = pyqtSignal(list)
  topicListChanged = pyqtSignal(list)
  htmlGenerated = pyqtSignal(bool)
  initData = pyqtSignal(list, list)

  def __init__(self, model: GenerateModel):
    super().__init__()
    self._model = model
    self._model.clientListChanged.connect(self.refreshClientList)
    self._model.topicListChanged.connect(self.refreshTopicList)

  def generateHTML(self, autoSelect: bool, imageSrcs: list[str], altText: str, buttonTextOverride: str, linkOverride: str, docxPath: str, savePath: str):
    self._model.setLastDownloadDir(docxPath)
    self._model.setButtonTextOverride(buttonTextOverride)
    self._model.setLinkOverride(linkOverride)
    self._model.generateHTML(autoSelect, imageSrcs, altText, savePath)
    self.htmlGenerated.emit(True)

  def loadClient(self, clientName):
    self._model.loadClient(clientName)
    self.clientLoaded.emit(self._model.getCurrentClient(), self._model.getTopicList())

  def loadTopic(self, topicName):
    self._model.loadTopic(topicName)
    self.topicLoaded.emit(self._model.getTopicLink())

  def getClientList(self):
    return self._model.getClientList()
  
  def getTopicList(self):
    return self._model.getTopicList()
  
  def refreshClientList(self, clientList: list):
    self.clientListChanged.emit(clientList)

  def refreshTopicList(self, topicList: list):
    self.topicListChanged.emit(topicList)

  def getCurrentClient(self):
    return self._model.getCurrentClient()

  def getCurrentTopic(self):
    return self._model.getSelectedTopic()
  
  def uploadDocx(self, path: str):
    self._model.setLastUploadDir(os.path.dirname(path))
    self._model.setDocxPath(path)

  def getImgsNeeded(self):
    return self._model.getImgsNeeded()

  def startData(self):
    self.initData.emit(self._model.getClientList(), self._model.getTopicList())