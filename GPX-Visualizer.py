import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt

import gpxpy
from gpxpy.geo import haversine_distance

from statistics import mean

height = 600
width = 600


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
        self.programNameLabel = QLabel("GPX Visualizer", self)
        font = self.programNameLabel.font()
        font.setPointSize(20)
        self.programNameLabel.setFont(font)
        self.programNameLabel.resize(width - 20, self.programNameLabel.height())
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

        # trackpoint counter
        self.trackPointDefault = "Track points: "
        self.trackPointLabel = QLabel(self.trackPointDefault, self)
        font = self.trackPointLabel.font()
        font.setPointSize(11)
        self.trackPointLabel.setFont(font)
        self.trackPointLabel.resize(width - 20, self.trackPointLabel.height())
        self.trackPointLabel.move(10, 240)

        # start timestamp
        self.startTimeDefault = "Trip start: "
        self.startTimeLabel = QLabel(self.startTimeDefault, self)
        font = self.startTimeLabel.font()
        font.setPointSize(11)
        self.startTimeLabel.setFont(font)
        self.startTimeLabel.resize(width - 20, self.startTimeLabel.height())
        self.startTimeLabel.move(10, 280)

        # end timestamp
        self.endTimeDefault = "Trip end: "
        self.endTimeLabel = QLabel(self.endTimeDefault, self)
        font = self.endTimeLabel.font()
        font.setPointSize(11)
        self.endTimeLabel.setFont(font)
        self.endTimeLabel.resize(width - 20, self.endTimeLabel.height())
        self.endTimeLabel.move(10, 320)

        # duration
        self.tripDurationDefault = "Trip duration: "
        self.tripDurationLabel = QLabel(self.tripDurationDefault, self)
        font = self.tripDurationLabel.font()
        font.setPointSize(11)
        self.tripDurationLabel.setFont(font)
        self.tripDurationLabel.resize(width - 20, self.tripDurationLabel.height())
        self.tripDurationLabel.move(10, 360)

        # distance in km
        self.distanceTraveledDefault = "Distance traveled: "
        self.distanceTraveledLabel = QLabel(self.distanceTraveledDefault, self)
        font = self.distanceTraveledLabel.font()
        font.setPointSize(11)
        self.distanceTraveledLabel.setFont(font)
        self.distanceTraveledLabel.resize(width - 20, self.distanceTraveledLabel.height())
        self.distanceTraveledLabel.move(10, 400)

        # velocity in km/h
        self.averageVelocityDefault = "Average velocity: "
        self.averageVelocityLabel = QLabel(self.averageVelocityDefault, self)
        font = self.averageVelocityLabel.font()
        font.setPointSize(11)
        self.averageVelocityLabel.setFont(font)
        self.averageVelocityLabel.resize(width - 20, self.averageVelocityLabel.height())
        self.averageVelocityLabel.move(10, 440)

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

            # distance in meters
            distance = 0
            distances = [0]
            distanceTimes = [0]
            # velocity in km/h
            velocities = []
            velocityTimes = []
            # add up distances if there are multiple points with same time
            distanceHold = 0
            seconds = 0

            for i in range(len(track.segments[0].points)):
                point = track.segments[0].points[i]
                prevPoint = track.segments[0].points[i - 1]

                lats.append(point.latitude)
                lons.append(point.longitude)

                if i > 0:
                    dDifference = haversine_distance(point.latitude, point.longitude, prevPoint.latitude,
                                                     prevPoint.longitude)
                    tDifference = point.time_difference(prevPoint)
                    if tDifference == 0:
                        distanceHold += dDifference
                        continue
                    seconds += tDifference

                    distance += dDifference
                    distances.append(distance)
                    distanceTimes.append(seconds)

                    velocity = (dDifference + distanceHold) / tDifference
                    distanceHold = 0
                    # multiplied by a constant to convert from m/s to km/h
                    velocities.append(velocity * 3.6)
                    velocityTimes.append(seconds)

            fig, ax = plt.subplots()
            ax.plot(lons, lats)
            ax.set_title("Map")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            plt.axis("equal")
            plt.show()

            fig, ax = plt.subplots()
            ax.plot(distanceTimes, distances)
            ax.set_title("Distance")
            ax.set_xlabel("s")
            ax.set_ylabel("km")
            plt.show()

            fig, ax = plt.subplots()
            ax.plot(velocityTimes, velocities)
            ax.set_title("Velocity")
            ax.set_xlabel("s")
            ax.set_ylabel("km/h")
            plt.show()  


            pointCount = len(track.segments[0].points)
            tripStart = track.segments[0].points[0].time
            tripEnd = track.segments[0].points[-1].time
            tripDuration = track.segments[0].points[0].time_difference(track.segments[0].points[-1])
            tripDurationHr = int(tripDuration / 3600)
            tripDurationMin = int((tripDuration % 3600) / 60)

            self.trackPointLabel.setText(self.trackPointDefault + str(pointCount))
            self.startTimeLabel.setText(self.startTimeDefault + str(tripStart) + " (UTC)")
            self.endTimeLabel.setText(self.endTimeDefault + str(tripEnd) + " (UTC)")
            self.tripDurationLabel.setText(self.tripDurationDefault + str(tripDurationHr) + ":" + str(tripDurationMin))
            self.distanceTraveledLabel.setText(self.distanceTraveledDefault + str(round(float(distance) / 1000, 2)) + " km")
            self.averageVelocityLabel.setText(self.averageVelocityDefault + str(round(mean(velocities), 2)) + " km/h")


        except FileNotFoundError:
            self.fileName.setText("File not found!")
            self.eraseData()

        except:
            self.fileName.setText("Invalid file!")
            self.eraseData()

    def eraseData(self):
        self.trackPointLabel.setText(self.trackPointDefault)
        self.startTimeLabel.setText(self.startTimeDefault)
        self.endTimeLabel.setText(self.endTimeDefault)
        self.tripDurationLabel.setText(self.tripDurationDefault)
        self.distanceTraveledLabel.setText(self.distanceTraveledDefault)
        self.averageVelocityLabel.setText(self.averageVelocityDefault)


if __name__ == "__main__":
    main()
