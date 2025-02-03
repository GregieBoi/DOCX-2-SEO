from PyQt6.QtCore import QObject, pyqtSignal
from _tabs._topics.model.topics_model import TopicsModel

class TopicsViewModel(QObject):
  topicSaved = pyqtSignal(str, list)
  topicDeleted = pyqtSignal(list)
  topicLoaded = pyqtSignal(str, str, str, str, list, list, list, list)
  initTopics = pyqtSignal(list, list)
  clientLoaded = pyqtSignal(str, list)
  clientListChanged = pyqtSignal(list)

  def __init__(self, model: TopicsModel):
    super().__init__()
    self._model = model

  def saveTopic(self, topicName, topicLink, topicHeroSrcs, topicTechSrcs, topicInteriorSrcs, topicMiscSrcs):
    self._model.setTopicName(topicName)
    self._model.setTopicLink(topicLink)
    self._model.setTopicHeroSrcs(topicHeroSrcs)
    self._model.setTopicTechSrcs(topicTechSrcs)
    self._model.setTopicInteriorSrcs(topicInteriorSrcs)
    self._model.setTopicMiscSrcs(topicMiscSrcs)
    self._model.saveTopic()
    self.topicSaved.emit(self._model.getTopicName(), self._model.getTopicList())

  def deleteTopic(self):
    self._model.deleteTopic()
    self.topicDeleted.emit(self._model.getTopicList())

  def loadTopic(self, topicName):
    self._model.loadTopic(topicName)
    self.topicLoaded.emit(self._model.getCurrentClient(), self._model.getSelectedTopic(), self._model.getTopicName(), self._model.getTopicLink(), self._model.getTopicHeroSrcs(), self._model.getTopicTechSrcs(), self._model.getTopicInteriorSrcs(), self._model.getTopicMiscSrcs())
  
  def startTopics(self):
    self.initTopics.emit(self._model.getClientList(), self._model.getTopicList())

  def loadClient(self, clientName):
    self._model.loadClient(clientName)
    self.clientLoaded.emit(self._model.getCurrentClient(), self._model.getTopicList())

  def getClientList(self):
    return self._model.getClientList()