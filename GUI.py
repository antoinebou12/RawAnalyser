import sys, os, json
import time
from win32api import GetSystemMetrics
from os.path import basename
import tifffile as tiff
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QWidget, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QEvent

widthScreen = GetSystemMetrics(0)
heightScreen = GetSystemMetrics(1)
widthApp = widthScreen
heightApp = heightScreen


class MenuFile(QMainWindow):
    def __init__(self, parent=None):
        super(MenuFile, self).__init__(parent)
        self.setCentralWidget(FormWidget(self))
        self.Menu()

    def Menu(self):
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.resize(widthApp, heightApp)
        self.move(0, 0)
        self.setWindowTitle('RawView')
        self.setWindowIcon(QIcon('image\icon.png'))

    def showDialog(self):
        self.setCentralWidget(FormWidget(self))


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        qApp.installEventFilter(self)
        self.UI()

    def UI(self):
        global position
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/Users/antoine.boucher/Desktop/',
                                                 "(*.tiff *.raw)")
        print self.fname[0]
        name = self.fname[0]
        global matrix
        cols_count = 1928
        rows_count = 1088
        matrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
        if name[-4:] == 'tiff':
            self.pix = QPixmap(self.fname[0])
            image_array = np.fromfile(self.fname[0], dtype=np.uint16, count=1928 * 1088)
            matrix = np.array(matrix)
            matrix = np.reshape(image_array, (1088, 1928))
        elif name[-3:] == 'raw':
            f = open(self.fname[0], "rb")
            image_array = np.fromfile(f, dtype=np.uint16, count=1928 * 1088)
            matrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
            matrix = np.array(matrix)
            matrix = np.reshape(image_array, (1088, 1928))
            # raw to tiff
            tiff.imsave('tiff/' + basename(name) + 'raw.tiff', matrix)
            time.sleep(1)
            self.pix = QPixmap('tiff/' + basename(name) + 'raw.tiff')

        self.image = QLabel(self)
        self.image.setPixmap(self.pix)
        self.image.setObjectName("image")
        self.image.mousePressEvent = self.getPos
        self.num = 0
        self.point = 'first ROI '
        self.text = ''
        self.setToolTip(self.text)
        self.feeds = {
            'gray_first_x': 1,
            'gray_first_y': 1,
            'first_x': 1,
            'first_y': 1,
            'last_x': 1928,
            'last_y': 1088,
            'gray_last_x': 1,
            'gray_last_y': 1
        }
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.NoButton:
                global position
                position = event.pos()
                #print ''
                #print position.x()
                #print position.y()
                #print ''
                if ((position.x() % 2 == 0) & (position.y() % 2 == 0)):
                    self.color = 'blue'
                elif ((position.x() % 2 == 1) & (position.y() % 2 == 1)):
                    self.color = 'red'
                elif ((position.x() % 2 == 0) & (position.y() % 2 == 1)):
                    self.color = 'green'
                elif ((position.x() % 2 == 1) & (position.y() % 2 == 0)):
                    self.color = 'green'
                self.text = self.point  + 'x: ' + str(position.x()) + ' y:' + str(position.y()) + ' value ' + str(
                    matrix[position.y()][position.x()] / 64) + ' color ' + self.color
                self.setToolTip(self.text)
        else:
            pass  # do other stuff
        return super(FormWidget, self).eventFilter(source, event)

    def getPos(self, event):
        global matrix
        mouse_x = event.pos().x()
        mouse_y = event.pos().y()
        print x
        print y
        self.num = self.num + 1
        with open('json/points.json', 'w') as f:
            if self.num % 4 == 1:
                self.feeds['first_x'] = x
                self.feeds['first_y'] = y
                self.point = 'last ROI '
                self.text = self.point + 'x: ' + str(position.x()) + ' y:' + str(position.y()) + ' value ' + str(matrix[position.y()][position.x()]/64)+ ' color ' + self.color
                self.setToolTip(self.text)
            elif self.num % 4 == 2:
                self.feeds['last_x'] = x
                self.feeds['last_y'] = y
                self.point = 'first gray '
                self.text = self.point + 'x: ' + str(position.x()) + ' y:' + str(position.y()) + ' value ' + str(
                    matrix[position.y()][position.x()] / 64)+ ' color ' + self.color
                self.setToolTip(self.text)
            elif self.num % 4 == 3:
                self.feeds['gray_first_x'] = x
                self.feeds['gray_first_y'] = y
                self.point = 'last gray '
                self.text = self.point + 'x: ' + str(position.x()) + ' y:' + str(position.y()) + ' value ' + str(
                    matrix[position.y()][position.x()] / 64)+ ' color ' + self.color
                self.setToolTip(self.text)
            elif self.num % 4 == 0:
                self.feeds['gray_last_x'] = x
                self.feeds['gray_last_y'] = y
                self.point = 'first ROI'
                self.text = self.point + 'x: ' + str(position.x()) + ' y:' + str(position.y()) + ' value ' + str(
                    matrix[position.y()][position.x()] / 64)+ ' color ' + self.color
                self.setToolTip(self.text)
            json.dump(self.feeds, f)


def main():
    app = QApplication([])
    ex = MenuFile()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

