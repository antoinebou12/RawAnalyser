import sys,os, getopt, json, winsound, time
import numpy as np
from scipy.misc import imsave
from scipy import ndimage
import PIL.Image as Image
from PIL import *
import plotly
plotly.tools.set_credentials_file(username='antoine13', api_key='DZN51FyyaBILK1Ie1InJ')
import plotly.plotly as py
import plotly.graph_objs as go
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

global numFile
numFile=0
global pointfile
pointfile = 'json/points.json'



class NewAnalyse(FileSystemEventHandler):
    def on_created(self, event):
        global numFile
        global newFile
        if event.src_path[-3:] == 'raw':
            newFile = event.src_path
            print newFile
        numFile=numFile+1
        with open(pointfile, 'r') as f:
            point = json.load(f)

        f = open(newFile, "rb")


        # list in text file
        #thefileCrop = open('array/image_crop.txt', 'w')
        # thefileArray = open('array/image_array.txt', 'w')
        # thefileMatrix = open('array/matrix.txt', 'w')
        # thefileChannelG = open('array/G.txt', 'w')
        # thefileChannelB = open('array/B.txt', 'w')
        # thefileChannelR = open('array/R.txt', 'w')

        image_array = np.fromfile(f, dtype=np.uint16, count=1928 * 1088)
        # for item in image_array:
        #     thefileArray.write("%s\n" % item)
        # raw to tiff
        image = Image.frombuffer("I", [1928, 1088], image_array.astype('I'), 'raw', 'I', 0, 1)
        imsave('tiff/' + str(numFile) + '.tiff', image)
        #Matrix 2d of the image
        cols_count, rows_count = 1928, 1088;

        matrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
        for i in range(1, 1929):
            for j in range(1, 1089):
                matrix[j - 1][i - 1] = image_array[(i * j) - 1]
                # Dead Pixel
                #if matrix[j-1][i-1] == 0:
                    # print 'deadPixel ' + 'x: ' + str((i-1)) + ' y: ' + str((j-1))
        #Write in text file the list
        # for item in matrix:
        #     thefileMatrix.write("%s\n" % item)



        cropMatrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
        for xCrop in range(point['first_x'], point['last_x'], 1):
            for yCrop in range(point['first_y'], point['last_y'], 1):
                cropMatrix[yCrop][xCrop] = matrix[yCrop][xCrop]
        # Write in text file the list
        # for itemCrop in cropMatrix:
        #    thefileCrop.write("%s\n" % itemCrop)

        ChannelB = [[0 for x in range(cols_count)] for y in range(rows_count)]  # 524416
        ChannelR = [[0 for x in range(cols_count)] for y in range(rows_count)]  # 524416
        ChannelG = [[0 for x in range(cols_count)] for y in range(rows_count)]  # 1048832

        for i in range(0, 1928, 2):
            for j in range(0, 1028, 2):
                ChannelB[j][i] = cropMatrix[j][i]

        for i in range(1, 1928, 2):
            for j in range(0, 1028, 2):
                ChannelG[j][i] = cropMatrix[j][i]

        for i in range(0, 1928, 2):
            for j in range(1, 1028, 2):
                ChannelG[j][i] = cropMatrix[j][i]

        for i in range(1, 1928, 2):
            for j in range(1, 1028, 2):
                ChannelR[j][i] = cropMatrix[j][i]
        # Write in text file the list
        # for item in ChannelB:
        #     thefileChannelB.write("%s\n" % item)
        # for item in ChannelG:
        #     thefileChannelG.write("%s\n" % item)
        # for item in ChannelR:
        #     thefileChannelR.write("%s\n" % item)


        print 'Clipping at 1 (10bit) for black level'
        print 'R Black level ' + str(min(np.array(ChannelB)[np.nonzero(np.array(ChannelB))])/64)
        print 'G Black level ' + str(min(np.array(ChannelG)[np.nonzero(np.array(ChannelG))])/64)
        print 'B Black level ' + str(min(np.array(ChannelR)[np.nonzero(np.array(ChannelR))])/64)

        if ((min(np.array(ChannelB)[np.nonzero(np.array(ChannelB))])<=64) or (min(np.array(ChannelG)[np.nonzero(np.array(ChannelG))])<=64) or (min(np.array(ChannelR)[np.nonzero(np.array(ChannelR))])<=64)):
        # winsound.PlaySound('sound/black.wav', winsound.SND_FILENAME)
          print 'CLIPPING BLACK'
        else:
          print 'NOT CLIPPING BLACK'



        print 'Clipping at 1023 (10bit) for white level'
        print 'R White level ' + str(np.array(ChannelR).max()/64)
        print 'G White level ' + str(np.array(ChannelG).max()/64)
        print 'B White level ' + str(np.array(ChannelB).max()/64)

        if ((np.array(ChannelR).max()>= 65472) or (np.array(ChannelR).max()>=65472) or (np.array(ChannelR).max()>=65472)):
        #  winsound.PlaySound('sound/white.wav', winsound.SND_FILENAME)
           print 'CLIPPING WHITE'
        else:
           print 'NOT CLIPPING WHITE'









def main(argv):
    global newFile
    inputfolder = 'C:/Users/antoine.boucher/Desktop/Algolux/raw'
    pointfile = 'json/points.json'
    try:
        opts, args = getopt.getopt(argv, "hf:p:", ["ffile=","pfile"])
    except getopt.GetoptError:
        print 'test.py -f <pathfolder> -p <pointfile> '
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'The program will check for new file and analysed them'
            print '-f <pathfolder> raw image folder'
            print '-p <pointfile> of the region of interest'
            sys.exit()
        elif opt in ("-f", "--ffile"):
            inputfolder = arg
        elif opt in ("-p", "--pfile"):
            jsonfile = arg
    print 'Folder:', inputfolder
    print 'Json:', pointfile

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = NewAnalyse()
    observer = Observer()
    observer.schedule(event_handler, inputfolder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main(sys.argv[1:])





