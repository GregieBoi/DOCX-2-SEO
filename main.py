import sys
from PyQt6.QtWidgets import QApplication
from model.main_model import MainModel
from view.main_view import MainView
from viewmodel.main_viewmodel import MainViewModel

if __name__ == '__main__':
  app = QApplication(sys.argv)
  qss = "styles.qss"
  with open(qss) as f:
    app.setStyleSheet(f.read())
  model = MainModel()
  viewModel = MainViewModel(model)
  view = MainView(viewModel)
  view.show()
  sys.exit(app.exec())