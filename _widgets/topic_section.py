from PyQt6.QtWidgets import QWidget, QSizePolicy,QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QLineEdit, QSpacerItem
from PyQt6.QtCore import Qt

class TopicSections(QWidget):
    

    def __init__(self, label: str, parent=None):
        super().__init__(parent)

        self.links = []

        # Main layout
        self.layout = QVBoxLayout()

        # Create a horizontal layout for the buttons
        self.button_layout = QHBoxLayout()

        # Add a label
        self.label = QLabel(label)
        self.button_layout.addWidget(self.label)

        # Add spacer to push buttons to the right
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.button_layout.addItem(self.spacer)

        # Add button to add QLineEdit
        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.add_line_edit)
        self.button_layout.addWidget(self.add_button)

        # Add button to remove QLineEdit
        self.remove_button = QPushButton("-")
        self.remove_button.clicked.connect(self.remove_line_edit)
        self.button_layout.addWidget(self.remove_button)

        # Add button layout to the main layout
        self.layout.addLayout(self.button_layout)

        # Create a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)

    def add_line_edit(self):
        # Create a horizontal layout for the label and QLineEdit
        entry_layout = QHBoxLayout()

        # Create the number label
        number_label = QLabel(str(len(self.links) + 1))
        number_label.setFixedWidth(20)  # Set a fixed width for alignment
        entry_layout.addWidget(number_label)

        # Create the QLineEdit
        line_edit = QLineEdit()
        entry_layout.addWidget(line_edit)

        # Add the entry layout to the scroll layout
        self.scroll_layout.addLayout(entry_layout)

        # Store the number label and line edit together
        self.links.append((number_label, line_edit))

    def remove_line_edit(self):
        if self.scroll_layout.count() > 0:  # Ensure we don't remove the buttons
            # Remove the last entry layout
            item = self.scroll_layout.takeAt(self.scroll_layout.count() - 1)
            widget = item.layout()
            if widget is not None:
                # Delete widgets in the layout
                while widget.count():
                    sub_item = widget.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                widget.deleteLater()
                self.links.pop()

            # Update remaining number labels
            for idx, (label, _) in enumerate(self.links):
                label.setText(str(idx + 1))

    def fetch_links(self):
        return [le.text() for _, le in self.links]
    
    def clear(self):
        self.links = []
        for link in range(self.scroll_layout.count()):
            item = self.scroll_layout.takeAt(self.scroll_layout.count() - 1)
            widget = item.layout()
            if widget is not None:
                # Delete widgets in the layout
                while widget.count():
                    sub_item = widget.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                widget.deleteLater()