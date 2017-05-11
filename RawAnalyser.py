import sys, os
import json
#import winsound
import time
from os.path import basename


import numpy as np
import cv2
from scipy.misc import imsave
import PIL.Image as Image
from PIL import *
import tifffile as tiff


import plotly
plotly.tools.set_credentials_file(username='antoine13', api_key='DZN51FyyaBILK1Ie1InJ')
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout, Histogram
import plotly.tools as tls
import plotly.plotly as py
import matplotlib.pyplot as plt




import colorama
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import argparse
import argcomplete


# _______________________________________________________________________________________________
#
# This python file doesn't use pep8 convention
# RawAnalyser
# RawAnalyser
# Simple RawAnalyser for black and white clipping, gamma calculation, flatness with vignette
#
#______________________________________________________________________________________________




# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__



class NewAnalyse(FileSystemEventHandler):
    def on_created(self, event):
        global numFile
        global newFile
        if event.src_path[-3:] == 'raw':
            newFile = event.src_path
            print newFile
        numFile=numFile+1
        with open(args.points, 'r') as f:
            point = json.load(f)

        f = open(newFile, "rb")


        # list in text file
        #thefileCrop = open('array/crop.txt', 'w')
        #thefileArray = open('array/array.txt', 'w')
        #thefileMatrix = open('array/matrix.txt', 'w')
        #thefileChannelG = open('array/G.txt', 'w')
        #thefileChannelB = open('array/B.txt', 'w')
        #thefileChannelR = open('array/R.txt', 'w')
        global matrix
        image_array = np.fromfile(f, dtype=np.uint16, count=1928 * 1088)
        #for item in image_array:
        #    thefileArray.write("%s\n" % item)
        
        #Matrix 2d of the image
        global cols_count
        global rows_count
        cols_count = 1928
        rows_count = 1088

        matrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
        matrix = np.array(matrix)
        matrix = np.reshape(image_array, (1088, 1928))
        # raw to tiff
        tiff.imsave('tiff/'+ str(basename(newFile))  + str(numFile) + '.tiff', matrix )

        # Dead Pixel
        #for j in range(0,1088)
        #    for i in range(0,1928)
        #        if image_array[j][i] == 0:
        #            print "dead pixel at " + "x: " + str(j) + " y: " +str(i)

        #Write in text file the list
        #for item in matrix:
        #    thefileMatrix.write("%s\n" % item)
        # B 524416
        # R 524416
        # G 1048832

        cropMatrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
        for xCrop in range(point['first_x'], point['last_x'], 1):
            for yCrop in range(point['first_y'], point['last_y'], 1):
                cropMatrix[yCrop][xCrop] = matrix[yCrop][xCrop]

        grayMatrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
        for xGray in range(point['gray_first_x'], point['gray_last_x'], 1):
            for yGray in range(point['gray_first_y'], point['gray_last_y'], 1):
                grayMatrix[yGray][xGray] = cropMatrix[yGray][xGray]
        # Write in text file the list
        #for itemCrop in cropMatrix:
        #    thefileCrop.write("%s\n" % itemCrop)

        ChannelB = [[0 for x in range(cols_count)] for y in range(rows_count)]
        ChannelR = [[0 for x in range(cols_count)] for y in range(rows_count)]
        ChannelG = [[0 for x in range(cols_count)] for y in range(rows_count)]
        GrayB = [[0 for x in range(cols_count)] for y in range(rows_count)]
        GrayR = [[0 for x in range(cols_count)] for y in range(rows_count)]
        GrayG = [[0 for x in range(cols_count)] for y in range(rows_count)]

        for i in range(0, 1928, 2):
            for j in range(0, 1028, 2):
                ChannelB[j][i] = cropMatrix[j][i]
                GrayB[j][i] = grayMatrix[j][i]

        for i in range(1, 1928, 2):
            for j in range(0, 1028, 2):
                ChannelG[j][i] = cropMatrix[j][i]
                GrayG[j][i] = grayMatrix[j][i]

        for i in range(0, 1928, 2):
            for j in range(1, 1028, 2):
                ChannelG[j][i] = cropMatrix[j][i]
                GrayG[j][i] = grayMatrix[j][i]

        for i in range(1, 1928, 2):
            for j in range(1, 1028, 2):
                ChannelR[j][i] = cropMatrix[j][i]
                GrayR[j][i] = grayMatrix[j][i]
        #Write in text file the list
        #for item in ChannelB:
        #    thefileChannelB.write("%s\n" % item)
        #for item in ChannelG:
        #    thefileChannelG.write("%s\n" % item)
        #for item in ChannelR:
        #    thefileChannelR.write("%s\n" % item)

        def clipping():

            print """ 
            
   _____  _  _                _               
  / ____|| |(_)              (_)              
 | |     | | _  _ __   _ __   _  _ __    __ _ 
 | |     | || || '_ \ | '_ \ | || '_ \  / _` |
 | |____ | || || |_) || |_) || || | | || (_| |
  \_____||_||_|| .__/ | .__/ |_||_| |_| \__, |
               | |    | |                __/ |
               |_|    |_|               |___/ 
            
            
                                                """
            Blue = np.unique(np.array(ChannelB), return_counts=True)
            #print Blue
            #print Blue[0].size
            #print Blue[1].size
            Green = np.unique(np.array(ChannelG), return_counts=True)
            #print Green
            #print Green[0].size
            #print Green[1].size
            Red = np.unique(np.array(ChannelR), return_counts=True)
            #print Red
            #print Red[0].size
            #print Red[1].size

            print 'Clipping at 1 (10bit) for black(min) level'
            print 'B Black level ' + str(min(np.array(ChannelB)[np.nonzero(np.array(ChannelB))]) / 64) + ' count ' + str(Blue[1][1]) + ' second closest value ' + str((Blue[0][2])/64)
            print 'G Black level ' + str(min(np.array(ChannelG)[np.nonzero(np.array(ChannelG))])/64) + ' count ' + str(Green[1][1]) + ' second closest value ' + str((Green[0][2])/64)
            print 'R Black level ' + str(min(np.array(ChannelR)[np.nonzero(np.array(ChannelR))]) / 64) + ' count ' + str(Red[1][1]) + ' second closest value ' + str((Red[0][2])/64)


            if ((min(np.array(ChannelB)[np.nonzero(np.array(ChannelB))])<=64) or (min(np.array(ChannelG)[np.nonzero(np.array(ChannelG))])<=64) or (min(np.array(ChannelR)[np.nonzero(np.array(ChannelR))])<=64)):
                # winsound.PlaySound('sound/black.wav', winsound.SND_FILENAME)
                print  colorama.Fore.RED + 'WARNING:' + 'CLIPPING BLACK!!!!'+ colorama.Fore.RESET
            else:
                print 'NOT CLIPPING BLACK'



            print 'Clipping at 1023 (10bit) for white(max) level'
            print 'B White level ' + str(np.array(ChannelB).max()/64) + ' count ' + str(Blue[1][(Blue[1].size-1)]) + ' closest value ' + str((Blue[0][(Blue[1].size-2)])/64)
            print 'G White level ' + str(np.array(ChannelG).max()/64) + ' count ' + str(Green[1][(Green[1].size-1)]) + ' closest value ' + str((Green[0][(Green[1].size-2)])/64)
            print 'R White level ' + str(np.array(ChannelR).max() / 64) + ' count ' + str(Red[1][(Red[1].size-1)]) + ' closest value ' + str((Red[0][(Red[1].size-2)])/64)


            if ((np.array(ChannelR).max()>= 65472) or (np.array(ChannelR).max()>=65472) or (np.array(ChannelR).max()>=65472)):
            #  winsound.PlaySound('sound/white.wav', winsound.SND_FILENAME)
                print colorama.Fore.RED + 'WARNING:' + 'CLIPPING WHITE(saturation)!!!'+ colorama.Fore.RESET
            else:
                print 'NOT CLIPPING WHITE'

        def gamma():
            global squareLength
            width = point['gray_last_x']-point['gray_first_x']
            height = point['gray_last_y']-point['gray_first_y']
            squareLength= (((8*width)/53)-5)
            if squareLength != height:
                print colorama.Fore.RED +'camera calibration check please'+ colorama.Fore.RESET

            white = [[0 for x in range(squareLength)] for y in range(squareLength)]
            whiteG = [[0 for x in range(squareLength)] for y in range(squareLength)]
            whiteB = [[0 for x in range(squareLength)] for y in range(squareLength)]
            whiteR = [[0 for x in range(squareLength)] for y in range(squareLength)]

            neutral8 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral8B = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral8G = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral8R = [[0 for x in range(squareLength)] for y in range(squareLength)]

            neutral65 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral65B = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral65G = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral65R = [[0 for x in range(squareLength)] for y in range(squareLength)]

            neutral5= [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral5B = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral5G = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral5R = [[0 for x in range(squareLength)] for y in range(squareLength)]

            neutral35= [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral35B = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral35G = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral35R = [[0 for x in range(squareLength)] for y in range(squareLength)]

            black= [[0 for x in range(squareLength)] for y in range(squareLength)]
            blackB = [[0 for x in range(squareLength)] for y in range(squareLength)]
            blackG = [[0 for x in range(squareLength)] for y in range(squareLength)]
            blackR = [[0 for x in range(squareLength)] for y in range(squareLength)]

            newPatche =  ((squareLength / 8) + squareLength)
            for w in range(0,squareLength):
                for h in range(0, squareLength):
                    newY = h + point['gray_first_y']
                    newX = w + point['gray_first_x']

                    white[h][w] = grayMatrix[newY][newX]
                    whiteB[h][w] = GrayB[newY][newX]
                    whiteG[h][w] = GrayG[newY][newX]
                    whiteR[h][w] = GrayR[newY][newX]

                    neutral8[h][w] = grayMatrix[newY][newX+ newPatche]
                    neutral8B[h][w] = GrayB[newY][newX + newPatche]
                    neutral8G[h][w] = GrayG[newY][newX + newPatche]
                    neutral8R[h][w] = GrayR[newY][newX + newPatche]

                    neutral65[h][w] = grayMatrix[newY][newX+ 2 * newPatche]
                    neutral65B[h][w] = GrayB[newY][newX + 2 * newPatche]
                    neutral65G[h][w] = GrayG[newY][newX + 2 *newPatche]
                    neutral65R[h][w] = GrayR[newY][newX + 2 * newPatche]

                    neutral5[h][w] = grayMatrix[newY][newX+ 3 * newPatche]
                    neutral5B[h][w] = GrayB[newY][newX + 3 * newPatche]
                    neutral5G[h][w] = GrayG[newY][newX + 3 *newPatche]
                    neutral5R[h][w] = GrayR[newY][newX + 3 * newPatche]

                    neutral35[h][w] = grayMatrix[newY][newX+ 4 * newPatche]
                    neutral35G[h][w] = GrayB[newY][newX + 4 * newPatche]
                    neutral35B[h][w] = GrayG[newY][newX + 4 * newPatche]
                    neutral35R[h][w] = GrayR[newY][newX + 4 * newPatche]

                    black[h][w] = grayMatrix[newY][newX+ 5 * newPatche]
                    blackB[h][w] = GrayB[newY][newX + 5 * newPatche]
                    blackG[h][w] = GrayG[newY][newX + 5 * newPatche]
                    blackR[h][w] = GrayR[newY][newX + 5 * newPatche]

            print """
 _____                                     
/ ____|                                    
| |  __   __ _  _ __ ___   _ __ ___    __ _ 
| | |_ | / _` || '_ ` _ \ | '_ ` _ \  / _` |
| |__| || (_| || | | | | || | | | | || (_| |
 \_____| \__,_||_| |_| |_||_| |_| |_| \__,_|
                                                       """

            #print 'white ' + str(((sum(map(sum, white)))/(np.count_nonzero(np.array(white))))/256) + ' Blue ' + str(((sum(map(sum, whiteB)))/(np.count_nonzero(np.array(whiteB))))/256) + ' Green ' + str(((sum(map(sum, whiteG)))/(np.count_nonzero(np.array(whiteG))))/256) + ' Red ' + str(((sum(map(sum, whiteR)))/(np.count_nonzero(np.array(whiteR))))/256)
            #print 'neutral8 ' + str(((sum(map(sum, neutral8))) / (np.count_nonzero(np.array(neutral8))))/256) + ' Blue '+ str(((sum(map(sum, neutral8B))) / (np.count_nonzero(np.array(neutral8B))))/256) + ' Green ' + str(((sum(map(sum, neutral8G))) / (np.count_nonzero(np.array(neutral8G))))/256) + ' Red ' + str(((sum(map(sum, neutral8R))) / (np.count_nonzero(np.array(neutral8R))))/256)
            #print 'neutral65 ' + str(((sum(map(sum, neutral65))) / (np.count_nonzero(np.array(neutral65))))/256) + ' Blue ' + str(((sum(map(sum, neutral65B))) / (np.count_nonzero(np.array(neutral65B))))/256) + ' Green ' + str(((sum(map(sum, neutral65G))) / (np.count_nonzero(np.array(neutral65G))))/256) + ' Red ' + str(((sum(map(sum, neutral65R))) / (np.count_nonzero(np.array(neutral65R))))/256)
            #print 'neutral5 ' + str(((sum(map(sum, neutral5))) / (np.count_nonzero(np.array(neutral5))))/256) + ' Blue ' + str(((sum(map(sum, neutral5B))) / (np.count_nonzero(np.array(neutral5B))))/256) + ' Green ' + str(((sum(map(sum, neutral5G))) / (np.count_nonzero(np.array(neutral5G))))/256) + ' Red ' + str(((sum(map(sum, neutral5G))) / (np.count_nonzero(np.array(neutral5R))))/256)
            #print 'neutral35 ' + str(((sum(map(sum, neutral35))) / (np.count_nonzero(np.array(neutral35))))/256) + ' Blue ' + str(((sum(map(sum, neutral35B))) / (np.count_nonzero(np.array(neutral35B))))/256) + ' Green ' + str(((sum(map(sum, neutral35G))) / (np.count_nonzero(np.array(neutral35G))))/256) + ' Red ' + str(((sum(map(sum, neutral35R))) / (np.count_nonzero(np.array(neutral35R))))/256)
            #print 'black ' + str(((sum(map(sum, black))) / (np.count_nonzero(np.array(black))))/256) + ' Blue ' + str(((sum(map(sum, blackB))) / (np.count_nonzero(np.array(blackB))))/256) + ' Green ' + str(((sum(map(sum, blackG))) / (np.count_nonzero(np.array(blackG))))/256) + ' Red ' + str(((sum(map(sum, blackR))) / (np.count_nonzero(np.array(blackR))))/256)

            #print '#################'

            #print 'Calculated densites for white' + str((-np.log10(((((sum(map(sum, white)))/float((np.count_nonzero(np.array(white)))))/256)/255))))
            #print 'Calculated densites for neutral8' + str((-np.log10(((((sum(map(sum, neutral8))) / float((np.count_nonzero(np.array(neutral8)))))/ 256)/255))))
            #print 'Calculated densites for neutral65' + str((-np.log10(((((sum(map(sum, neutral65))) / float((np.count_nonzero(np.array(neutral65))))) / 256)/255))))
            #print 'Calculated densites for neutral5' + str((-np.log10(((((sum(map(sum, neutral5))) / float((np.count_nonzero(np.array(neutral5)))))/ 256)/255))))
            #print 'Calculated densites for neutral35' + str((-np.log10(((((sum(map(sum, neutral35))) / float((np.count_nonzero(np.array(neutral35))))) / 256)/255))))
            #print 'Calculated densites for black' + str((-np.log10(((((sum(map(sum, black))) / float((np.count_nonzero(np.array(black))))) / 256)/255))))

            #print '#################'

            #print str(((-np.log10(((((sum(map(sum, white)))/float((np.count_nonzero(np.array(white)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral8))) / float((np.count_nonzero(np.array(neutral8)))))/ 256)/255))))/-0.1660817663)
            #print str(((-np.log10(((((sum(map(sum, neutral8)))/float((np.count_nonzero(np.array(neutral8)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral65))) / float((np.count_nonzero(np.array(neutral65)))))/ 256)/255))))/-0.2056390617)
            #print str(((-np.log10(((((sum(map(sum, neutral65)))/float((np.count_nonzero(np.array(neutral65)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral5))) / float((np.count_nonzero(np.array(neutral5)))))/ 256)/255))))/-0.2835423157)
            #print str(((-np.log10(((((sum(map(sum, neutral5)))/float((np.count_nonzero(np.array(neutral5)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral35))) / float((np.count_nonzero(np.array(neutral35)))))/ 256)/255))))/-0.3494155563)

            print (( (((-np.log10(((((sum(map(sum, white)))/float((np.count_nonzero(np.array(white)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral8))) / float((np.count_nonzero(np.array(neutral8)))))/ 256)/255))))/-0.1660817663) + (((-np.log10(((((sum(map(sum, neutral8)))/float((np.count_nonzero(np.array(neutral8)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral65))) / float((np.count_nonzero(np.array(neutral65)))))/ 256)/255))))/-0.2056390617) + (((-np.log10(((((sum(map(sum, neutral65)))/float((np.count_nonzero(np.array(neutral65)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral5))) / float((np.count_nonzero(np.array(neutral5)))))/ 256)/255))))/-0.2835423157) +(((-np.log10(((((sum(map(sum, neutral5)))/float((np.count_nonzero(np.array(neutral5)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral35))) / float((np.count_nonzero(np.array(neutral35)))))/ 256)/255))))/-0.3494155563))/4)

        def vignette():
            global numFile
            global newFile
            print """           
 __      ___                  _   _       
 \ \    / (_)                | | | |      
  \ \  / / _  __ _ _ __   ___| |_| |_ ___ 
   \ \/ / | |/ _` | '_ \ / _ \ __| __/ _  
    \  /  | | (_| | | | |  __/ |_| ||  __/
     \/   |_|\__, |_| |_|\___|\__|\__\___|
              __/ |                       
             |___/                                   """
            global squareLength
            matrixVig = [[0 for x in range(cols_count)] for y in range(rows_count)]
            blockPrint()
            vig = np.load(args.vignette);
            enablePrint()
            for i in range(0,1928):
                for j in range(0,1088):
                    matrixVig[j][i] = float(matrix[j][i] - args.bl)
            vignetteMatrix = matrixVig/vig
            vignetteMatrix = vignetteMatrix
            Image_arrayVig=np.reshape(np.array(vignetteMatrix),(1928*1088,1))
            tiff.imsave('tiff/' + str(basename(newFile)) + 'vig' + str(numFile) + '.tiff', Image_arrayVig )

            cropMatrixVig = [[0 for x in range(cols_count)] for y in range(rows_count)]
            for xCrop in range(point['first_x'], point['last_x'], 1):
                for yCrop in range(point['first_y'], point['last_y'], 1):
                    cropMatrixVig[yCrop][xCrop] = vignetteMatrix[yCrop][xCrop]

            grayMatrixVig = [[0 for x in range(cols_count)] for y in range(rows_count)]
            for xGray in range(point['gray_first_x'], point['gray_last_x'], 1):
                for yGray in range(point['gray_first_y'], point['gray_last_y'], 1):
                    grayMatrixVig[yGray][xGray] = cropMatrixVig[yGray][xGray]
            # Write in text file the list
            # for itemCrop in cropMatrix:
            #    thefileCrop.write("%s\n" % itemCrop)

            ChannelBVig = [[0 for x in range(cols_count)] for y in range(rows_count)]
            ChannelRVig = [[0 for x in range(cols_count)] for y in range(rows_count)]
            ChannelGVig = [[0 for x in range(cols_count)] for y in range(rows_count)]
            GrayBVig = [[0 for x in range(cols_count)] for y in range(rows_count)]
            GrayRVig = [[0 for x in range(cols_count)] for y in range(rows_count)]
            GrayGVig = [[0 for x in range(cols_count)] for y in range(rows_count)]

            for i in range(0, 1928, 2):
                for j in range(0, 1028, 2):
                    ChannelBVig[j][i] = cropMatrixVig[j][i]
                    GrayBVig[j][i] = grayMatrixVig[j][i]

            for i in range(1, 1928, 2):
                for j in range(0, 1028, 2):
                    ChannelGVig[j][i] = cropMatrixVig[j][i]
                    GrayGVig[j][i] = grayMatrixVig[j][i]

            for i in range(0, 1928, 2):
                for j in range(1, 1028, 2):
                    ChannelGVig[j][i] = cropMatrixVig[j][i]
                    GrayGVig[j][i] = grayMatrixVig[j][i]

            for i in range(1, 1928, 2):
                for j in range(1, 1028, 2):
                    ChannelRVig[j][i] = cropMatrixVig[j][i]
                    GrayRVig[j][i] = grayMatrixVig[j][i]




            whiteVig = [[0 for x in range(squareLength)] for y in range(squareLength)]
            whiteVig1 = [[0 for x in range(squareLength / 4)] for y in range(squareLength / 4)]
            whiteVig2 = [[0 for x in range(squareLength / 4)] for y in range(squareLength / 4)]
            whiteVig3 = [[0 for x in range(squareLength / 4)] for y in range(squareLength / 4)]
            whiteVig4 = [[0 for x in range(squareLength / 4)] for y in range(squareLength / 4)]


            neutral8Vig = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral8Vig5 = [[0 for x in range(squareLength/4)] for y in range(squareLength/4)]
            neutral8Vig6 = [[0 for x in range(squareLength/4)] for y in range(squareLength/4)]
            neutral8Vig7 = [[0 for x in range(squareLength/4)] for y in range(squareLength/4)]
            neutral8Vig8 = [[0 for x in range(squareLength/4)] for y in range(squareLength/4)]

            neutral65Vig = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral65Vig9 = [[0 for x in range(squareLength/4)] for y in range(squareLength/4)]
            neutral65Vig10 = [[0 for x in range(squareLength/4)] for y in range(squareLength/4)]
            neutral65Vig11 = [[0 for x in range(squareLength/4)] for y in range(squareLength/4)]
            neutral65Vig12 = [[0 for x in range(squareLength/4)] for y in range(squareLength/4)]


            neutral5Vig = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral5Vig13 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral5Vig14 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral5Vig15 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral5Vig16 = [[0 for x in range(squareLength)] for y in range(squareLength)]

            neutral35Vig = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral35Vig17 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral35Vig18 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral35Vig19 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            neutral35Vig20 = [[0 for x in range(squareLength)] for y in range(squareLength)]


            blackVig = [[0 for x in range(squareLength)] for y in range(squareLength)]
            blackVig21 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            blackVig22 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            blackVig23 = [[0 for x in range(squareLength)] for y in range(squareLength)]
            blackVig24 = [[0 for x in range(squareLength)] for y in range(squareLength)]


            newPatche = ((squareLength / 8) + squareLength)
            for w in range(0, squareLength):
                for h in range(0, squareLength):
                    newY = h + point['gray_first_y']
                    newX = w + point['gray_first_x']
                    whiteVig[h][w] = grayMatrixVig[newY][newX]
                    neutral8Vig[h][w] = grayMatrix[newY][newX + newPatche]
                    neutral65Vig[h][w] = grayMatrix[newY][newX + 2 * newPatche]
                    neutral5Vig[h][w] = grayMatrix[newY][newX + 3 * newPatche]
                    neutral35Vig[h][w] = grayMatrix[newY][newX + 4 * newPatche]
                    blackVig[h][w] = grayMatrix[newY][newX + 5 * newPatche]
            newQuad = ((squareLength / 4))
            for wFlat in range(0, newQuad):
                for hFlat in range(0, newQuad):

                    whiteVig1[hFlat][wFlat] =  whiteVig[hFlat][wFlat]
                    whiteVig2[hFlat][wFlat] =  whiteVig[hFlat][wFlat+newQuad]
                    whiteVig3[hFlat][wFlat] =  whiteVig[hFlat+newQuad][wFlat]
                    whiteVig4[hFlat][wFlat] = whiteVig[hFlat+newQuad][wFlat+newQuad]

                    neutral8Vig5[hFlat][wFlat] = neutral8Vig[hFlat][wFlat]
                    neutral8Vig6[hFlat][wFlat] = neutral8Vig[hFlat][wFlat+newQuad]
                    neutral8Vig7[hFlat][wFlat] = neutral8Vig[hFlat+newQuad][wFlat]
                    neutral8Vig8[hFlat][wFlat] = neutral8Vig[hFlat+newQuad][wFlat+newQuad]

                    neutral65Vig9[hFlat][wFlat] = neutral65Vig[hFlat][wFlat]
                    neutral65Vig10[hFlat][wFlat] = neutral65Vig[hFlat][wFlat+newQuad]
                    neutral65Vig11[hFlat][wFlat] = neutral65Vig[hFlat+newQuad][wFlat]
                    neutral65Vig12[hFlat][wFlat] = neutral65Vig[hFlat+newQuad][wFlat+newQuad]

                    neutral5Vig13[hFlat][wFlat] = neutral5Vig[hFlat][wFlat]
                    neutral5Vig14[hFlat][wFlat] = neutral5Vig[hFlat][wFlat+newQuad]
                    neutral5Vig15[hFlat][wFlat] = neutral5Vig[hFlat+newQuad][wFlat]
                    neutral5Vig16[hFlat][wFlat] = neutral5Vig[hFlat+newQuad][wFlat+newQuad]

                    neutral35Vig17[hFlat][wFlat] = neutral35Vig[hFlat][wFlat]
                    neutral35Vig18[hFlat][wFlat] = neutral35Vig[hFlat][wFlat + newQuad]
                    neutral35Vig19[hFlat][wFlat] = neutral35Vig[hFlat+ newQuad][wFlat]
                    neutral35Vig20[hFlat][wFlat] = neutral35Vig[hFlat+newQuad][wFlat+newQuad]

                    blackVig21[hFlat][wFlat] = blackVig[hFlat][wFlat]
                    blackVig22[hFlat][wFlat] = blackVig[hFlat][wFlat+newQuad]
                    blackVig23[hFlat][wFlat] = blackVig[hFlat+newQuad][wFlat]
                    blackVig24[hFlat][wFlat] = blackVig[hFlat+newQuad][wFlat+newQuad]


            print 'white1 ' + str(((sum(map(sum, whiteVig1))) / (np.count_nonzero(np.array(whiteVig4)))) / 256)
            print 'white2 ' + str(((sum(map(sum, whiteVig2))) / (np.count_nonzero(np.array(whiteVig2)))) / 256)
            print 'white3 ' + str(((sum(map(sum, whiteVig3))) / (np.count_nonzero(np.array(whiteVig3)))) / 256)
            print 'white4 ' + str(((sum(map(sum, whiteVig4))) / (np.count_nonzero(np.array(whiteVig4)))) / 256)
            print (( (((-np.log10(((((sum(map(sum, whiteVig)))/float((np.count_nonzero(np.array(whiteVig)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral8Vig))) / float((np.count_nonzero(np.array(neutral8Vig)))))/ 256)/255))))/-0.1660817663) + (((-np.log10(((((sum(map(sum, neutral8Vig)))/float((np.count_nonzero(np.array(neutral8Vig)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral65Vig))) / float((np.count_nonzero(np.array(neutral65Vig)))))/ 256)/255))))/-0.2056390617) + (((-np.log10(((((sum(map(sum, neutral65Vig)))/float((np.count_nonzero(np.array(neutral65Vig)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral5Vig))) / float((np.count_nonzero(np.array(neutral5Vig)))))/ 256)/255))))/-0.2835423157) +(((-np.log10(((((sum(map(sum, neutral5Vig)))/float((np.count_nonzero(np.array(neutral5Vig)))))/256)/255)))- (-np.log10(((((sum(map(sum, neutral35Vig))) / float((np.count_nonzero(np.array(neutral35Vig)))))/ 256)/255))))/-0.3494155563))/4)

        def histogram():
            global numFile
            global newFile
            global matrix
            plt.hist(np.array(matrix.ravel()), bins=1024, range=(np.array(matrix.ravel()).min(), np.array(matrix.ravel()).max()))
            plt.title('Histogram')
            fig = plt.gcf()
            #plot_url = py.plot_mpl(fig, filename='HistogramRaw', height=np.array(matrix.ravel()).max())
            # Convert to plotly figure
            plotly_fig = tls.mpl_to_plotly(fig)
            global numFile
            py.image.save_as(plotly_fig, 'histogram/'+ str(basename(newFile)) + 'histogram' + str(numFile) + '.png')



        if args.func == 'gamma':
            gamma()
        elif args.func == 'clipping':
            clipping()
        elif args.func == 'vignette':
            vignette()
        elif args.func == 'histogram':
            histogram()
        elif args.func == 'noHist':
            clipping()
            gamma()
            vignette()
        elif args.func == 'basic':
            clipping()
            gamma()
        elif args.func == 'all':
            clipping()
            gamma()
            vignette()
            histogram()




def main():
    if 'PYCHARM_HOSTED' in os.environ:
        convert = False  # in PyCharm, we should disable convert
        strip = False
    else:
        convert = None
        strip = None

    colorama.init(convert=convert, strip=strip)
    global args
    global newFile
    parser = _parser()
    argcomplete.autocomplete(parser)
    args = _parser().parse_args()
    global numFile
    numFile = 0
    print """                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                          
                    .:ss/-`                                                                                                                                                                                                                               
                `.+sddddhsso:`                                                                                                                                                                                                                            
              /shddddddddhssss++.                                                                                                                                                                                                                         
          -/yhddddddddddddhyssssso/:``                                                                                                                                                                                                                    
      `-+sddddddddddddddddddysssssssso:.                                                                                                                                                                                                                  
  ``/yhddddddddddddddddddddddysssssssssso+-.                                                                                                                                                                                                              
-+shddddddddddddddddddddddddddysssssssssssss/:.`                                            ````                                                                       ````                                                                               
+oooooooooooooo+:--------------osssssssssssssss/                                           `+++/                                                                       /+++.                                                                              
//////////////:                `ossssssssssssyh/                                           `+++/                                                                       /+++.                                                                              
/////////////:                  `/ssssssssssyhh/                                           `+++/                                                                       /+++.                                                                              
////////////.                    `/sssssssyyhhh/             -///////////////-.            `+++/            `--///////////-.               .-///////////:-`            /+++.          ////            -//-       `:///:.          :///:-                  
///////////.                      `/sssssyyhhhh/             -+++++++++++++++++/`          `+++/           ./+++++++++++++++/`           `:+++++++++++++++/-           /+++.          ++++            :++:        `:++++:`      ./+++/.                   
//////////.                         .sssyhhhhhh/             ```````````````-+++-          `+++/          `/++/-`````````-+++/`          .+++/`````````./++/`          /+++.          ++++            :++:          `/+++/.   `-++++-`                    
/////////`                           -oyhhhhhhh/                ``.----------++++`         `+++/          -+++:           /+++`         `/+++`          -+++-          /+++.          ++++            :++:           `-/+++:``/+++/-                      
///////+/.                           -shhhhhhhh/              `:+++++++++++++++++`         `+++/          -+++:           /+++`         `++++           -+++-          /+++.          ++++            :++:             ./+++//+++-`                       
/////+++++.                         .shhhhhhhhh/             `/+++:----------++++`         `+++/          -+++:           /+++`         `++++           -+++-          /+++.          ++++            :++:              `-+++++/.                         
////+++++++.                       /yhhhhhhhhhh/             -+++:           ++++`         `+++/          -+++:           /+++`         `++++           -+++-          /+++.          ++++            :++:              `-++++++-`                        
///+++++++++-                     /yhhhhhhhhhhh/             -+++-           ++++`         `+++/          -+++:           /+++`         `++++           -+++-          /+++.          ++++            :++:             ./+++//+++:`                       
//+++++++++++:                  `oyhhhhhhhhhhhh/             -+++:           ++++`         `+++/          -+++:           /+++`         `++++           -+++-          /+++.          ++++           ./++:           `:++++: ./+++/-                      
/+++++++++++++:                `shhhhhhhhhhhhhh/             ./++/-.........:+++/`         `+++/          `:++/-..........++++`          -+++:.........-/+++.          /+++.          -+++:.........-/+++:          -++++:.    ./+++:`                    
+++++++++++++++:...............+yyyyyyyyyyyyyyy/              ./+++++++++++++++:`          `+++/           ./+++++++++++++++++`          `:+++++++++++++++/.           /+++.          `:+++++++++++++++/-`        .:++++-       `:+++/:                   
-//+++++++++++++/:::::::::::::::::::::::::::--.`                .-///////////.`            `///:             .-///////////++++`            `.///////////-.             :///`            `.:///////////-`         `:///:`          .:///-                  
  ``-:+++++++++++/::::::::::::::::::::::--.`                                                                           ``.++++`                                                                                                                           
      `-//++++++++/:::::::::::::::::--..`                                                                 .:::::::::::://++++/`                                                                                                                           
          -:/+++++++:::::::::::::--.`                                                                     .+++++++++++++++/:-`                                                                                                                            
            ``-:+++++:::::::::--`                                                                          ````````````````                                                                                                                               
                `.//++/:::--.`                                                                                                                                                                                                                            
                    `-/:-.`                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                        
                                            """

    print args


    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = NewAnalyse()
    observer = Observer()
    observer.schedule(event_handler, args.folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def _parser():
    parser = argparse.ArgumentParser(description='Check a pixel color and value in the raw image')
    parser.add_argument("folder",default='raw', type=str, help='input folder to check for new raw file')
    parser.add_argument("points",default='json\points.json', type=str, help='the json file with the point for the ROI and Gray Patches ')
    parser.add_argument("--func", default='all', type=str, help='Find the gamma or the clipping')
    parser.add_argument("--bl", default='1024', type=int, help='black level of the camera')
    parser.add_argument("--vignette", default='vignette/OV2740_gauss_std6.npy', type=str, help='vignette of the camera')


    return parser
if __name__ == "__main__":
    main()





