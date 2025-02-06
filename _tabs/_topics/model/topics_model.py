from PyQt6.QtCore import QObject, pyqtSignal
from model.main_model import MainModel
import json
import os
from typing import TypedDict

# responsibilites of the topics model
# 1. Store the atttributes of the selected topic
# 2. provide a way to save the attributes to an entry in the clients topic.json
# 3. provide a way to load the attributes from an entry in the clients topic.json
# 4. provide a way to fetch all possible topics from the clients topic.json
# 5. delete a topic from the clients topic.json

'''class Images:
  hero: list[str]
  tech: list[str]
  interior: list[str]
  misc: list[str]

class TopicData(TypedDict):
  link: str
  images: Images'''

# ugly type hint for topic.json
# dict[str, dict[str, str | dict[str, list[str]]]]

# nicer type hint for topic.json
IMAGESTYPEHINT = TypedDict('Images', {'hero': list[str], 'tech': list[str], 'interior': list[str], 'misc': list[str]})
TOPICSTYPEHINT = TypedDict('Topic', {'link': str, 'images': IMAGESTYPEHINT})

class TopicsModel(QObject):
  clientListChanged = pyqtSignal(list)

  def __init__(self, mainModel: MainModel):
    super().__init__()
    self._mainModel = mainModel
    self._mainModel.clientListChanged.connect(self.refreshClientList)
    self.clientDirectory: str = self._mainModel.findClientDirectory()
    self.clientList: list[str] = self._mainModel.getClientList()
    self.currentClient: str = self.clientList[0]
    self.topicsJson: dict[str, TOPICSTYPEHINT] = self.fetchTopicsJSON()
    self.topicList: list[str] = self.fetchTopicList()
    self.selectedTopic: str = "New Topic"
    self.topicName: str = ""
    self.topicLink: str = ""
    self.topicHeroSrcs: list[str] = []
    self.topicTechSrcs: list[str] = []
    self.topicInteriorSrcs: list[str] = []
    self.topicMiscSrcs: list[str] = []

  def setTopicList(self, topicList: list[str]):
    self.topicList = topicList

  def getTopicList(self):
    return self.topicList
  
  def setClientList(self, clientList: list[str]):
    self.clientList = clientList

  def getClientList(self):
    return self.clientList
  
  def setCurrentClient(self, client: str):
    self.currentClient = client

  def getCurrentClient(self):
    return self.currentClient
  
  def setSelectedTopic(self, topic: str):
    self.selectedTopic = topic

  def getSelectedTopic(self):
    return self.selectedTopic

  def setTopicName(self, name: str):
    self.topicName = name
  
  def getTopicName(self):
    return self.topicName
  
  def setTopicLink(self, link: str):
    self.topicLink = link
  
  def getTopicLink(self):
    return self.topicLink
  
  def setTopicHeroSrcs(self, srcs: list[str]):
    self.topicHeroSrcs = srcs
  
  def getTopicHeroSrcs(self):
    return self.topicHeroSrcs
  
  def setTopicTechSrcs(self, srcs: list[str]):
    self.topicTechSrcs = srcs
  
  def getTopicTechSrcs(self):
    return self.topicTechSrcs
  
  def setTopicInteriorSrcs(self, srcs: list[str]):
    self.topicInteriorSrcs = srcs
  
  def getTopicInteriorSrcs(self):
    return self.topicInteriorSrcs
  
  def setTopicMiscSrcs(self, srcs: list[str]):
    self.topicMiscSrcs = srcs
  
  def getTopicMiscSrcs(self):
    return self.topicMiscSrcs
  
  # clear topic and client attributes
  def clear(self):
    self.clearTopic()
    self.currentClient = self.clientList[0]

  # reset the topic attributes
  def clearTopic(self):
    self.topicName = ""
    self.selectedTopic = self.topicList[0]
    self.topicLink = ""
    self.topicHeroSrcs = []
    self.topicTechSrcs = []
    self.topicInteriorSrcs = []
    self.topicMiscSrcs = []

  # refresh the list of topics from the clients topic.json
  def refreshTopicList(self):
    self.topicList = self.fetchTopicList()

  # save the new topic to clients topic.json
  def saveTopic(self):

    # grab all the images srcs from the topic sections and add them to the dict
    images: IMAGESTYPEHINT = {}
    images['hero'] = self.topicHeroSrcs
    images['tech'] = self.topicTechSrcs
    images['interior'] = self.topicInteriorSrcs
    images['misc'] = self.topicMiscSrcs

    # add the link and dict of images to the topic dict
    topic: TOPICSTYPEHINT = {}
    topic['link'] = self.topicLink
    topic['images'] = images

    # save the topic dict after adding the new one
    with open(os.path.join(self.clientDirectory, self.currentClient, 'topics.json'), 'w') as f:
      self.topicsJson[self.topicName] = topic
      json.dump(self.topicsJson, f, indent=2)
      f.close()

    self.selectedTopic = self.topicName
    self.refreshTopicList()
    self._mainModel.updateTopicList()

  # load the selected topic
  def loadTopic(self, topicName: str):
    self.clearTopic()

    if topicName in ["New Topic", "", None]:
      self.selectedTopic = "New Topic"
      self.topicName = ""
      return
    
    self.selectedTopic = topicName
    self.topicName = topicName
    self.topicLink = self.topicsJson[topicName]['link']
    self.topicHeroSrcs = self.topicsJson[topicName]['images']['hero']
    self.topicTechSrcs = self.topicsJson[topicName]['images']['tech']
    self.topicInteriorSrcs = self.topicsJson[topicName]['images']['interior']
    self.topicMiscSrcs = self.topicsJson[topicName]['images']['misc']

  # delete the selected topic
  def deleteTopic(self):
    
    del self.topicsJson[self.selectedTopic]
    with open(os.path.join(self.clientDirectory, self.currentClient, 'topics.json'), 'w') as f:
      json.dump(self.topicsJson, f, indent=2)
      f.close()

    self.clearTopic()
    self.refreshTopicList()
    self._mainModel.updateTopicList()
    
  # fetch the list of topics from the clients topic.json
  def fetchTopicList(self):
    topics = []
    for topic in self.topicsJson.keys(): topics.append(topic) 
    return ['New Topic'] + sorted(topics)

  # fetch the topics.json file as a dictionary
  def fetchTopicsJSON(self):
    with open(os.path.join(self.clientDirectory, self.currentClient, 'topics.json'), 'r') as f:
      self.topicsJson = json.load(f)
      f.close()
    return self.topicsJson
  
  # load the selected client
  def loadClient(self, clientName: str):
    
    self.clear()

    self.currentClient = clientName
    self.topicsJson = self.fetchTopicsJSON()
    self.topicList = self.fetchTopicList()

  def refreshClientList(self, clientList: list):
    self.clientList = clientList
    self.clientListChanged.emit(self.clientList)
