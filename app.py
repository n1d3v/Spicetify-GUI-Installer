import sys
import platform
import requests
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QTextEdit
from PyQt5.QtCore import Qt, QProcess

class SampleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spicetify GUI Installer')
        self.setGeometry(100, 100, 600, 400)  # (x, y, width, height)
        self.setFixedSize(600, 400)  # Anchors the window size

        self.stacked_widget = QStackedWidget(self)
        self.page1 = self.create_page("Spicetify GUI Installer", "Disclaimer!! \nThe Spicetify Project is not mine, I only wrote this GUI and nothing else.\nI do not take ownership of the Spicetify Project, this is made for fun.")
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

        system_type = platform.system()
        try:
            if system_type == "Windows":
                # Install spicetify-cli for Windows
                spicetify_script = requests.get("https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1").text
                self.execute_script("powershell", ["-ExecutionPolicy", "Bypass", spicetify_script])

                # Install Spicetify Marketplace script for Windows
                marketplace_script = requests.get("https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1").text
                self.execute_script("powershell", ["-ExecutionPolicy", "Bypass", marketplace_script])
            elif system_type in ["Linux", "Darwin"]:
                # Install spicetify-cli for Unix-based systems (Linux and macOS)
                spicetify_script = "curl -k https://raw.githubusercontent.com/n1d3v/Spicetify-GUI-Installer/main/spicetify-edited/cli/install.sh | sh"
                self.execute_script("bash", ["-c", spicetify_script])

                # Install Spicetify Marketplace script for Unix-based systems
                marketplace_script = "curl -k https://raw.githubusercontent.com/n1d3v/Spicetify-GUI-Installer/main/spicetify-edited/marketplace/install.sh | sh"
                self.execute_script("bash", ["-c", marketplace_script])
            else:
                raise Exception("Unsupported operating system.")
        except Exception as e:
            self.log_box.append(f"Error: {e}")

    def execute_script(self, executable, arguments):
        process = QProcess()
        process.setProgram(executable)
        process.setArguments(arguments)
        process.readyReadStandardOutput.connect(self.on_script_output)
        process.readyReadStandardError.connect(self.on_script_output)
        process.startDetached()

    def on_script_output(self):
        process = self.sender()
        output = process.readAllStandardOutput().data().decode("utf-8")
        error_output = process.readAllStandardError().data().decode("utf-8")
        self.log_box.append(output)
        self.log_box.append(error_output)

def main():
    app = QApplication(sys.argv)
    window = SampleApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
