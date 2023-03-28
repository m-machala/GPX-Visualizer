import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt
height = 750
width = 750


def main():
    app = QApplication([])
    window = Window()

    app.exec_()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        # window title
        self.setWindowTitle("GPX Visualizer")
        self.setFixedSize(width, height)

        # program name
        self.programNameLabel = QLabel("GPX Visualizer by Martin Machala", self)
        font = self.programNameLabel.font()
        font.setPointSize(20)
        self.programNameLabel.setFont(font)
        self.programNameLabel.move(10, 10)

        # label above file select
        self.fileSelectLabel = QLabel("Select a GPX file:", self)
        font = self.fileSelectLabel.font()
        font.setPointSize(10)
        self.fileSelectLabel.setFont(font)
        self.fileSelectLabel.move(10, 60)

        #  file path input
        self.fileInputLine = QLineEdit(self)
        self.fileInputLine.resize(width - 20, 35)
        self.fileInputLine.move(10, 90)
        self.fileInputLine.setPlaceholderText("path to .gpx file")

        # file browser button
        self.fileInputButton = QPushButton("Browse", self)
        self.fileInputButton.resize(75, 35)
        self.fileInputButton.move(10, 130)
        self.fileInputButton.clicked.connect(self.fileSelect)

        # analysis button
        self.analyzeButton = QPushButton("Analyze", self)
        self.analyzeButton.resize(75, 35)
        self.analyzeButton.move(width - 85, 130)
        self.analyzeButton.clicked.connect(self.analyzeData)

        # filename label
        self.fileName = QLabel("No file selected", self)
        font = self.fileName.font()
        font.setPointSize(15)
        self.fileName.setFont(font)
        self.fileName.resize(width - 20, self.fileName.height())
        self.fileName.move(10, 190)

        # map image
        self.imageLabel = QLabel(self)
        self.mapHeight = 500
        self.imageLabel.resize(width - 20, self.mapHeight)
        self.imageLabel.move(10, 240)

        # show window
        self.show()

    def fileSelect(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a GPX file", "", "GPX Files (*.gpx)", options=options)
        if fileName:
            self.fileInputLine.setText(fileName)

    def analyzeData(self):
        fig, ax = plt.subplots()
        ax.plot([1, 1, 5, 2, 5, 6], [1, 2, 1, 5, 6, 7])
        mp = Canvas(fig)
        mp.draw()
        w, h = mp.get_width_height()
        buf = mp.buffer_rgba()
        data = buf.tobytes()
        qimage = QImage(data, w, h, QImage.Format_RGBA8888)
        self.imageLabel.setPixmap(QPixmap.fromImage(qimage))

if __name__ == "__main__":
    main()
