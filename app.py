import sys
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QTextEdit
from PyQt5.QtCore import Qt

class SampleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spicetify GUI Installer')
        self.setGeometry(100, 100, 600, 400)  # (x, y, width, height)
        self.setFixedSize(600, 400)  # Anchors the window size

        self.stacked_widget = QStackedWidget(self)
        self.page1 = self.create_page("Disclaimer!!", "The Spicetify Project is not mine, I only wrote this GUI and nothing else.\nI do not take ownership of the Spicetify Project, this is made for fun.")
        self.log_box = QTextEdit(self)
        self.log_box.setReadOnly(True)

        self.stacked_widget.addWidget(self.page1)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

    def create_page(self, large_text, small_text):
        page = QWidget()
        layout = QVBoxLayout()

        label_large = QLabel(large_text)
        label_large.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Align text at the top and center horizontally
        label_large.setStyleSheet("font-size: 24px;")  # Set the font size to 24 pixels

        label_small = QLabel(small_text)
        label_small.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Align text at the top and center horizontally
        label_small.setStyleSheet("font-size: 14px;")  # Set the font size to 14 pixels

        install_button = QPushButton("Install")
        install_button.clicked.connect(self.install_spicetify)

        layout.addWidget(label_large)
        layout.addWidget(label_small)
        layout.addWidget(install_button)

        page.setLayout(layout)
        return page

    def install_spicetify(self):
        self.log_box.clear()
        self.log_box.append("Installing Spicetify...\n")

        try:
            # Install spicetify-cli
            spicetify_script = 'Invoke-WebRequest -Uri "https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1" -UseBasicParsing | Invoke-Expression'
            subprocess.run(["powershell.exe", "-Command", spicetify_script], check=True, capture_output=True, text=True)
            self.log_box.append("Spicetify installation completed successfully.")

            # Install Spicetify Marketplace script
            marketplace_script = 'Invoke-WebRequest -Uri "https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1" -UseBasicParsing | Invoke-Expression'
            subprocess.run(["powershell.exe", "-Command", marketplace_script], check=True, capture_output=True, text=True)
            self.log_box.append("Spicetify Marketplace script installation completed successfully.")
        except subprocess.CalledProcessError as e:
            self.log_box.append(f"An error occurred during installation:\n{e.stderr}")

        self.log_box.append("\n")

def main():
    app = QApplication(sys.argv)
    window = SampleApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
