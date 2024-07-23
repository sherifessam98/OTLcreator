import hou
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit

class HDACreator(QWidget):
    def __init__(self):
        super(HDACreator, self).__init__()

        # Fixed directory for saving HDAs
        #Specfify Your Directory
        self.hda_directory = ""

        # Create the UI components
        self.setWindowTitle('HDA Creator')
        self.setGeometry(100, 100, 400, 150)
        self.layout = QVBoxLayout()

        self.info_label = QLabel('Select a node and provide HDA name:', self)
        self.layout.addWidget(self.info_label)

        self.name_input_layout = QHBoxLayout()
        self.name_input_label = QLabel('HDA Name:', self)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter HDA Name")

        self.name_input_layout.addWidget(self.name_input_label)
        self.name_input_layout.addWidget(self.name_input)
        self.layout.addLayout(self.name_input_layout)

        self.create_button = QPushButton('Create HDA', self)
        self.create_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        self.create_button.clicked.connect(self.create_hda)
        self.layout.addWidget(self.create_button)

        self.result_label = QLabel('', self)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def create_hda(self):
        selected_nodes = hou.selectedNodes()
        if not selected_nodes:
            self.result_label.setText('No node selected')
            self.result_label.setStyleSheet("color: red;")
            return

        hda_name = self.name_input.text().strip()
        if not hda_name:
            self.result_label.setText('HDA name cannot be empty')
            self.result_label.setStyleSheet("color: red;")
            return

        # Full HDA file path
        hda_path = f"{self.hda_directory}/{hda_name}.hda"

        try:
            node = selected_nodes[0]

            # Define HDA label
            hda_label = hda_name.replace('_', ' ').title()

            # Create the HDA
            new_hda = node.createDigitalAsset(name=hda_name, hda_file_name=hda_path, description=hda_label)

            # Install the HDA
            hou.hda.installFile(hda_path)
            hou.hda.reloadAllFiles()

            self.result_label.setText(f'HDA created and installed: {hda_name}')
            self.result_label.setStyleSheet("color: green;")
        except Exception as e:
            self.result_label.setText(f'Error: {str(e)}')
            self.result_label.setStyleSheet("color: red;")

hda_creator = HDACreator()
hda_creator.show()


