import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt

import gpxpy
from gpxpy.geo import haversine_distance

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

        # show window
        self.show()

    def fileSelect(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a GPX file", "", "GPX Files (*.gpx)", options=options)
        if fileName:
            self.fileInputLine.setText(fileName)

    def analyzeData(self):
        try:
            file = open(self.fileInputLine.text(), 'r')
            gpx = gpxpy.parse(file)
            track = gpx.tracks[0]
            self.fileName.setText(track.name)

            lats = []
            lons = []
            pointCount = len(track.segments[0].points)
            tripStart = track.segments[0].points[0].time
            tripEnd = track.segments[0].points[-1].time
            # distance in meters
            distance = 0
            distances = [0]
            # velocity in km/h
            velocities = []
            # add up distances if there are multiple points with same time
            distanceHold = 0

            for i in range(len(track.segments[0].points)):
                point = track.segments[0].points[i]
                prevPoint = track.segments[0].points[i - 1]

                lats.append(point.latitude)
                lons.append(point.longitude)

                if i > 0:
                    dDifference = haversine_distance(point.latitude, point.longitude, prevPoint.latitude, prevPoint.longitude)
                    distance += dDifference
                    distances.append(distance)

                    tDifference = point.time_difference(prevPoint)
                    if tDifference == 0:
                        distanceHold += dDifference
                        continue

                    velocity = (dDifference + distanceHold) / tDifference
                    distanceHold = 0
                    # multiplied by a constant to convert from m/s to km/h
                    velocities.append(velocity * 3.6)
            fig, ax = plt.subplots()
            ax.plot(lons, lats)
            plt.axis("equal")
            plt.show()


        except FileNotFoundError:
            self.fileName.setText("File not found!")

        except:
            self.fileName.setText("Invalid file!")



if __name__ == "__main__":
    main()
