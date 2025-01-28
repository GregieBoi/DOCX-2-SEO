from PyQt6.QtCore import QObject, pyqtSignal

class MainViewModel(QObject):
  countChanged = pyqtSignal(int)  # Signal to update the count in the view

  def __init__(self, model):
    super().__init__()
    self._model = model

  def increment(self):
    self._model.increment()  # Call the increment method in the model
    self.countChanged.emit(self._model.count)  # Emit the countChanged signal with the current count

  