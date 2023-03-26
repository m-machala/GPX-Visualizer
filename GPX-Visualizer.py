import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog


def main():
    app = QApplication([])
    window = Window()

    app.exec()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("GPX Visualizer")
        self.setGeometry(100, 100, 500, 500)

        self.programNameLabel = QLabel("GPX Visualizer by Martin Machala", self)
        font = self.programNameLabel.font()
        font.setPointSize(20)
        self.programNameLabel.setFont(font)
        self.programNameLabel.move(10, 10)

        self.fileSelectLabel = QLabel('Select a GPX file:', self)
        font = self.fileSelectLabel.font()
        font.setPointSize(10)
        self.fileSelectLabel.setFont(font)
        self.fileSelectLabel.move(10, 60)

        self.fileInputLine = QLineEdit(self)
        self.fileInputLine.move(10, 90)
        self.fileInputLine.setPlaceholderText('path to .gpx file')

        self.fileInputButton = QPushButton('Browse', self)
        self.fileInputButton.move(10, 130)
        self.fileInputButton.clicked.connect(self.fileSelect)

        self.show()

    def fileSelect(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a GPX file", "", "GPX Files (*.gpx)", options=options)
        if fileName:
            self.file_input.setText(fileName)


if __name__ == "__main__":
    main()
