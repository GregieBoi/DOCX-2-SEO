

class ClientModel:
  def __init__(self):
    self.clientName = ""
    self.currentClient = ""
    self.clientButton = ""
    self.clientStyle = ""
    self.clientWrapper = ""

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
  
  def clear(self):
    self.clientName = ""
    self.currentClient = ""
    self.clientButton = ""
    self.clientStyle = ""
    self.clientWrapper = ""
