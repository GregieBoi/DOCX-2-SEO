from PyQt6.QtCore import QObject, pyqtSignal
from model.main_model import MainModel
import mammoth
from bs4 import BeautifulSoup
from collections import Counter
import random
import json
import os
from typing import TypedDict

# responsibilites of the generate model
# 1. Store the attributes: clients, selected client, button text overrides, 
# link overrides, selected client topics, selected topic, path to the docx file,
# path to last used upload directory, and path to last used download directory
# 2. Fetch the client's topics.json file
# 3. Parse the docx file and convert it to html
# 4. Add the client's button, wrapper, and styling to the html
# 5. Save the html to the selected directory
# 6. Provide a way to automatically select the image srcs used based on the 
# selected topic
# 7. Load the topics list from the selected client

# Keywords are used to determine the category of an image
KEYWORDS = {"connectivity": "tech", "connect": "tech", "connected": "tech", "technology": "tech", "tech": "tech", "interior": "interior", "cabin": "interior", "seats": "interior", "exterior": "hero", "body": "hero", "power": "hero", "engine": "hero", "luxury": "interior"}

IMAGESTYPEHINT = TypedDict('Images', {'hero': list[str], 'tech': list[str], 'interior': list[str], 'misc': list[str]})
TOPICSTYPEHINT = TypedDict('Topic', {'link': str, 'images': IMAGESTYPEHINT})

class GenerateModel(QObject):
  clientListChanged = pyqtSignal(list)
  topicListChanged = pyqtSignal(list)

  def __init__(self, mainModel: MainModel):
    super().__init__()
    self._mainModel: MainModel = mainModel
    self._mainModel.clientListChanged.connect(self.refreshClientList)
    self._mainModel.topicListChanged.connect(self.refreshClientList)
    self.clientDirectory: str = self._mainModel.findClientDirectory()
    self.clientList: list[str] = self._mainModel.getClientList()
    self.currentClient: str = '' if self.clientList == [] else self.clientList[0]
    self.buttonTextOverride: str = ""
    self.linkOverride: str = ""
    self.topicsJson: dict[str, TOPICSTYPEHINT] = self.fetchTopicsJSON()
    self.topicList: list[str] = self.fetchTopicList()
    self.selectedTopic: str = self.topicList[0] if self.topicList else ''
    self.topicLink: str = ""
    self.topicHeroSrcs: list[str] = []
    self.topicTechSrcs: list[str] = []
    self.topicInteriorSrcs: list[str] = []
    self.topicMiscSrcs: list[str] = []
    self.startTopicSrcs()
    self.docxPath: str = ""
    self.lastUploadDir: str = ""
    self.lastDownloadDir: str = ""
    self.imgsNeeded: int = 0

  def setClientList(self, clientList: list[str]):
    self.clientList = clientList

  def getClientList(self):
    return self.clientList
  
  def setCurrentClient(self, client: str):
    self.currentClient = client

  def getCurrentClient(self):
    return self.currentClient
  
  def setButtonTextOverride(self, text: str):
    self.buttonTextOverride = text
  
  def getButtonTextOverride(self):
    return self.buttonTextOverride
  
  def setLinkOverride(self, link: str):
    self.linkOverride = link
  
  def getLinkOverride(self):
    return self.linkOverride
  
  def setTopicList(self, topics: list[str]):
    self.selectedClientTopics = topics
  
  def getTopicList(self):
    return self.topicList
  
  def setSelectedTopic(self, topic: str):
    self.selectedTopic = topic
  
  def getSelectedTopic(self):
    return self.selectedTopic
  
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
  
  def setDocxPath(self, path: str):
    self.docxPath = path
    self.setImgsNeeded()
  
  def getDocxPath(self):
    return self.docxPath
  
  def setLastUploadDir(self, path: str):
    self.lastUploadDir = path
  
  def getLastUploadDir(self):
    return self.lastUploadDir
  
  def setLastDownloadDir(self, path: str):
    self.lastDownloadDir = path
  
  def getLastDownloadDir(self):
    return self.lastDownloadDir
  
  def startTopicSrcs(self):
    if self.selectedTopic not in [None, '']:
      self.topicLink = self.topicsJson[self.selectedTopic]['link']
      self.topicHeroSrcs = self.topicsJson[self.selectedTopic]['images']['hero']
      self.topicTechSrcs = self.topicsJson[self.selectedTopic]['images']['tech']
      self.topicInteriorSrcs = self.topicsJson[self.selectedTopic]['images']['interior']
      self.topicMiscSrcs = self.topicsJson[self.selectedTopic]['images']['misc']
  
  # clear the generate attributes
  def clear(self):
    self.currentClient = self.clientList[0]
    self.buttonTextOverride = ""
    self.linkOverride = ""
    self.topicList = []
    self.selectedTopic = ""

  def getImgsNeeded(self):
    return self.imgsNeeded
  
  def setImgsNeeded(self):
    soup = self.convertDocx(self.docxPath)
    self.imgsNeeded = len(soup.find_all('h1')) - 1

  def generateHTML(self, autoSelect: bool, imageSrcs: list[str], altText: str, savePath: str):
    html = self.convertDocx(self.docxPath)
    html = self.SOUP(html)
    self.populateImgSrcs(html, autoSelect, imageSrcs, altText)
    self.populateBtns(html, autoSelect)
    self.saveHTML(str(html), savePath)

  def convertDocx(self, path: str):
    with open(path, 'rb') as f:
      parsed = mammoth.convert_to_html(f)
      html = BeautifulSoup(parsed.value, 'html.parser')
      f.close()
      return html
    
  def SOUP(self, html: BeautifulSoup):

    self.clearATags(html)
    
    # add the empty img tags to the html
    self.addImgSOUP(html)

    # add the client's buttons to the html
    self.addButtonSOUP(html, self.buttonTextOverride, self.linkOverride)

    # fix tables
    self.fixTableSOUP(html)

    # format the client's disclaimer
    self.formatDisclaimerSOUP(html)

    # wrap the content sections in the client's wrapper
    html = self.wrapContentSOUP(html)

    # add the client's styling to the html
    self.addStyleSOUP(html)
    
    return html
  
  def clearATags(self, html: BeautifulSoup):
    for a in html.find_all('a'):
      if a.has_attr('href'):
        continue
      a.decompose()
  
  def addImgSOUP(self, html: BeautifulSoup):
    for i, h1 in enumerate(html.find_all('h1')):
      if i == 0:
        h1.decompose()
        continue
      img = html.new_tag('img', src='', alt='')
      h1.insert_before(img)

  def addButtonSOUP(self, html: BeautifulSoup, buttonTextOverride: str, linkOverride: str):
    buttonPath = os.path.join(self.clientDirectory, self.currentClient, 'button.html')
    button = ''
    with open(buttonPath, 'r') as f:
      button = f.read()
      f.close()

    for i, img in enumerate(html.find_all('img')):
      if i == 0:
        continue
      btn = BeautifulSoup(button, 'html.parser')
      print(btn)
      img.insert_before(btn)

    btn = BeautifulSoup(button, 'html.parser')
    html.append(btn)

  def wrapContentSOUP(self, html: BeautifulSoup):
    wrapperPath = os.path.join(self.clientDirectory, self.currentClient, 'wrapper.html')
    wrapper = ''
    with open(wrapperPath, 'r') as f:
      wrapper = f.read()
      f.close()

    sections = []
    currentSection = []
    for element in html.contents:
      if element.name == 'img' and currentSection:
        sections.append(currentSection)
        currentSection = []
      currentSection.append(element)

    if currentSection:
      sections.append(currentSection)

    newSOUP = BeautifulSoup('', 'html.parser')
    for section in sections:
      wrap = BeautifulSoup(wrapper, 'html.parser')
      innerDiv = wrap.find('div').find('div')

      for element in section:
        innerDiv.append(element)
      
      newSOUP.append(wrap)

    return newSOUP

  def fixTableSOUP(self, html: BeautifulSoup):
    for th in html.find_all('th'):
      child = th.findChildren()[0]
      td = html.new_tag('td')
      td.append(child)
      th.replace_with(td)

  def formatDisclaimerSOUP(self, html: BeautifulSoup):
    disclaimer = html.new_tag('div', style="font-size: 10px; font-style: italic; line-height: 12px;")
    p = html.new_tag('p')
    p.string = "Sources:"
    p.append(html.new_tag('br'))
    disclaimer.append(p)

    for h2 in html.find_all('h2'):
      link = h2.find('a')
      if link:
        p.append(link)
        p.append(html.new_tag('br'))
      h2.decompose()
    
    html.append(disclaimer)

  def addStyleSOUP(self, html: BeautifulSoup):
    stylePath = os.path.join(self.clientDirectory, self.currentClient, 'styles.json')
    style = ''
    with open(stylePath, 'r') as f:
      style = f.read()
      f.close()

    styleJSON = json.loads(style)
    for key, value in styleJSON.items():
      if key == 'style' and value != '':
        styles = html.new_tag('style')
        styles.append(value)
        html.insert(0, styles)
        continue
      for k, v in value.items():
        for tag in html.find_all(key):
          tag[k] = v

  def populateImgSrcs(self, html: BeautifulSoup, autoSelect: bool, imageSrcs: list[str], altText: str):
    heros = self.topicHeroSrcs[:]
    techs = self.topicTechSrcs[:]
    interiors = self.topicInteriorSrcs[:]
    miscs = self.topicMiscSrcs[:]
    for i, (img, h1) in enumerate(zip(html.find_all('img'), html.find_all('h1'))):
      if autoSelect:
        img['src'] = self.selectImage(h1.text.lower(), i == 0)
        img['alt'] = self.selectedTopic
        continue
      img['src'] = imageSrcs[0]
      img['alt'] = altText
      imageSrcs.pop(0)
    self.setTopicHeroSrcs(heros[:])
    self.setTopicTechSrcs(techs[:])
    self.setTopicInteriorSrcs(interiors[:])
    self.setTopicMiscSrcs(miscs[:])

  def selectImage(self, h1Text: str, first: bool):
    if first:
      pick = random.choice(self.topicHeroSrcs)
      self.topicHeroSrcs.remove(pick)
      return pick
    keywordCounts = Counter(
      keyword for keyword in KEYWORDS if keyword in h1Text.lower()
    )
    if not keywordCounts:
      if len(self.topicMiscSrcs) > 0:
        pick = random.choice(self.topicMiscSrcs)
        self.topicMiscSrcs.remove(pick)
        return pick
      elif len(self.topicInteriorSrcs) > 0:
        pick = random.choice(self.topicInteriorSrcs)
        self.topicInteriorSrcs.remove(pick)
        return pick
      elif len(self.topicTechSrcs) > 0:
        pick = random.choice(self.topicTechSrcs)
        self.topicTechSrcs.remove(pick)
        return pick
      elif len(self.topicHeroSrcs) > 0:
        pick = random.choice(self.topicHeroSrcs)
        self.topicHeroSrcs.remove(pick)
        return pick
      else:
        return ''

    keyword = keywordCounts.most_common(1)[0][0]
    category = KEYWORDS[keyword]
    if category == 'hero' and len(self.topicHeroSrcs) > 0:
      pick = random.choice(self.topicHeroSrcs)
      self.topicHeroSrcs.remove(pick)
      return pick
    elif category == 'tech' and len(self.topicTechSrcs) > 0:
      pick = random.choice(self.topicTechSrcs)
      self.topicTechSrcs.remove(pick)
      return pick
    elif category == 'interior' and len(self.topicInteriorSrcs) > 0:
      pick = random.choice(self.topicInteriorSrcs)
      self.topicInteriorSrcs.remove(pick)
      return pick
    elif len(self.topicMiscSrcs) > 0:
      pick = random.choice(self.topicMiscSrcs)
      self.topicMiscSrcs.remove(pick)
      return pick
    elif len(self.topicInteriorSrcs) > 0:
      pick = random.choice(self.topicInteriorSrcs)
      self.topicInteriorSrcs.remove(pick)
      return pick
    elif len(self.topicTechSrcs) > 0:
      pick = random.choice(self.topicTechSrcs)
      self.topicTechSrcs.remove(pick)
      return pick
    elif len(self.topicHeroSrcs) > 0:
      pick = random.choice(self.topicHeroSrcs)
      self.topicHeroSrcs.remove(pick)
      return pick
    else:
      return ''
    
  def populateBtns(self, html: BeautifulSoup, autoSelect: bool):
    for btn in html.find_all('a'):
      text = btn.string
      if text and (btn.string.startswith('https://') or btn.string.startswith('http://') or btn.string.startswith('www.')):
        continue

      has_button = True if html.find_all('button') != [] else False

      if autoSelect:
        btn['href'] = self.topicLink if self.linkOverride == '' else self.linkOverride
        if not has_button:
          btn.string = "View Inventory"if self.buttonTextOverride == '' else self.buttonTextOverride
        continue
      btn['href'] = self.linkOverride
      if not has_button:
        btn.string = 'View Inventory' if self.buttonTextOverride == '' else self.buttonTextOverride

    for btn in html.find_all('button'):
      print("found button")
      if autoSelect:
        btn['onclick'] = "window.location.href='" + self.topicLink + "'" if self.linkOverride == '' else "window.location.href='" + self.linkOverride + "'"
        btn.string = "View Inventory" if self.buttonTextOverride == '' else self.buttonTextOverride
        continue
      btn['onclick'] = "window.location.href='" + self.linkOverride + "'"
      btn.string = 'View Inventory' if self.buttonTextOverride == '' else self.buttonTextOverride

  def saveHTML(self, html: str, path: str):
    with open(path, 'w') as f:
      f.write(html)

  # fetch the topics.json file as a dictionary
  def fetchTopicsJSON(self):
    try:
      with open(os.path.join(self.clientDirectory, self.currentClient, 'topics.json'), 'r') as f:
        self.topicsJson = json.load(f)
        f.close()
      return self.topicsJson
    except:
      self.topicsJson = {}
  
  # fetch the list of topics from the clients topic.json
  def fetchTopicList(self):
    topics = []
    if self.topicsJson:
      for topic in self.topicsJson.keys(): topics.append(topic) 
    return sorted(topics)
  
  def loadClient(self, clientName: str):
    self.clear()

    self.currentClient = clientName
    self.topicsJson = self.fetchTopicsJSON()
    self.topicList = self.fetchTopicList()

  def refreshClientList(self, clientList: list):
    self.clientList = clientList
    self.clientListChanged.emit(self.clientList)
    self.topicListChanged.emit(self.topicList)

  def refreshTopicList(self, topicList: list):
    self.topicsJson = self.fetchTopicsJSON()
    self.topicList = self.fetchTopicList()
    self.topicListChanged.emit(self.topicList)

  def loadTopic(self, topicName: str):
    self.selectedTopic = topicName
    self.topicName = topicName
    self.startTopicSrcs()



  