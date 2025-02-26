import os
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

class HackerUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MaskFile")
        self.setFixedSize(450, 300)
        self.setStyleSheet("background-color: black; color: grey; font-family: 'Courier New';")

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(10)

        self.image_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("imgmaskfile.png")  
        self.image_label.setPixmap(pixmap.scaled(300, 120, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        file_format_layout = QtWidgets.QHBoxLayout()
        file_format_layout.setSpacing(10)

        self.browse_button = QtWidgets.QPushButton("📂 Browse File")
        self.browse_button.setFixedWidth(200)
        self.browse_button.setStyleSheet("background-color: grey; color: black; border-radius: 10px; padding: 5px;")
        self.browse_button.clicked.connect(self.browse_file)
        file_format_layout.addWidget(self.browse_button)

        self.extension_input = QtWidgets.QComboBox()
        self.extension_input.setFixedWidth(200)
        self.extension_input.addItem("🗂️ Select format")
        self.extension_input.addItems(["jpg", "txt", "pdf", "png", "docx", "xlsx"])
        self.extension_input.setCurrentIndex(0)
        self.extension_input.setStyleSheet("background-color: black; color: grey; border: 1px solid grey; border-radius: 10px; padding: 5px;")
        file_format_layout.addWidget(self.extension_input)

        layout.addLayout(file_format_layout)

        self.mask_button = QtWidgets.QPushButton("🚀 GO!")
        self.mask_button.setFixedWidth(200)
        self.mask_button.setStyleSheet("background-color: grey; color: black; border-radius: 10px; padding: 5px;")
        self.mask_button.clicked.connect(self.mask_file)
        layout.addWidget(self.mask_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.output = QtWidgets.QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: black; color: grey; border: 1px solid grey; border-radius: 10px; padding: 5px;")
        self.output.setFixedHeight(30)
        self.output.hide()
        layout.addWidget(self.output)

        self.setLayout(layout)

    def browse_file(self):
        file_dialog = QtWidgets.QFileDialog()
        self.file_path, _ = file_dialog.getOpenFileName(self, "Select File to Mask")
        if self.file_path:
            file_name = os.path.basename(self.file_path)
            self.browse_button.setText(f"📂 Selected: {file_name}")

    def mask_file(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            QtWidgets.QMessageBox.warning(self, "Error", "No file selected.")
            return

        fake_extension = self.extension_input.currentText()

        if fake_extension == "Select format":
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a valid format.")
            return

        if not os.path.isfile(self.file_path):
            QtWidgets.QMessageBox.warning(self, "Error", "The specified file does not exist.")
            return

        base_name, original_extension = os.path.splitext(os.path.basename(self.file_path))
        directory = os.path.dirname(self.file_path)

        # Create a disguised filename
        disguised_name = f"{base_name}.{fake_extension}{original_extension}"
        disguised_path = os.path.join(directory, disguised_name)

        try:
            os.rename(self.file_path, disguised_path)
            self.output.setText(f"[✅] Success: '{self.file_path}' has been disguised as '{disguised_path}'.\nThe file appears renamed but retains its original format.")
            self.output.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to rename the file. {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = HackerUI()
    window.show()
    app.exec_()
