import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtGui
from model.main_model import MainModel
from view.main_view import MainView
from viewmodel.main_viewmodel import MainViewModel

styles = '''
QPushButton#destructiveButton {
  background-color: red; 
  color: white; 
  border-radius: 5px; 
  padding-top: 1px; 
  padding-bottom: 3px; 
  padding-left: 12px; 
  padding-right: 12px; 
  margin-bottom: 1px;
} 
QPushButton#destructiveButton:pressed {
  background-color: darkRed; 
  color: grey;
}
QPushButton#destructiveButton:disabled {
  background-color: darkred; 
  color: grey; 
}
'''

if __name__ == '__main__':
  app = QApplication(sys.argv)
  app.setStyleSheet(styles)
  app.setWindowIcon(QtGui.QIcon('icon.icns'))
  model = MainModel()
  viewModel = MainViewModel(model)
  view = MainView(viewModel)
  view.show()
  sys.exit(app.exec())