import sys,os, getopt, json, winsound, time
import numpy as np
from scipy.misc import imsave
import PIL.Image as Image
from PIL import *
import argparse
import argcomplete


def main():
    parser = _parser()
    argcomplete.autocomplete(parser)
    args = _parser().parse_args()
    f = open(args.input, "rb")

    thefileArray = open('array/array.txt', 'w')
    thefileMatrix = open('array/matrix.txt', 'w')
    thefileChannelG = open('array/G.txt', 'w')
    thefileChannelB = open('array/B.txt', 'w')
    thefileChannelR = open('array/R.txt', 'w')


    # list in text file
    cols_count = 1928
    rows_count = 1088
    image_array = np.fromfile(f, dtype=np.uint16, count=1928 * 1088)
    # raw to tiff
    image = Image.frombuffer("I", [1928, 1088], image_array.astype('I'), 'raw', 'I', 0, 1)
    #imsave('tiff/test.tiff', image)
    for item in image_array:
        thefileArray.write("%s\n" % item)
    #Matrix 2d of the image
    matrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
    matrix = np.array(matrix)
    matrix = np.reshape(image_array, (1088, 1928))
    #Write in text file the list
    for item in matrix:
        thefileMatrix.write("%s\n" % item)

    ChannelB = [[0 for x in range(cols_count)] for y in range(rows_count)]  # 524416
    ChannelR = [[0 for x in range(cols_count)] for y in range(rows_count)]  # 524416
    ChannelG = [[0 for x in range(cols_count)] for y in range(rows_count)]  # 1048832

    for i in range(0, 1928, 2):
        for j in range(0, 1028, 2):
            ChannelB[j][i] = matrix[j][i]


    for i in range(1, 1928, 2):
        for j in range(0, 1028, 2):
            ChannelG[j][i] = matrix[j][i]

    for i in range(0, 1928, 2):
        for j in range(1, 1028, 2):
            ChannelG[j][i] = matrix[j][i]

    for i in range(1, 1928, 2):
        for j in range(1, 1028, 2):
            ChannelR[j][i] = matrix[j][i]
    #Write in text file the list
    for item in ChannelB:
        thefileChannelB.write("%s\n" % item)
    for item in ChannelG:
        thefileChannelG.write("%s\n" % item)
    for item in ChannelR:
        thefileChannelR.write("%s\n" % item)

    #Check the color
    xPoint, yPoint = args.x,args.y
    if (ChannelB[yPoint][xPoint] != 0) and (args.bitdepth == 16):
        print 'Blue ' + str(ChannelB[yPoint][xPoint])
    elif (ChannelG[yPoint][xPoint] != 0) and (args.bitdepth == 16):
        print 'Green '+ str(ChannelG[yPoint][xPoint])
    elif (ChannelR[yPoint][xPoint] !=0) and (args.bitdepth == 16):
        print 'Red ' + str(ChannelR[yPoint][xPoint])
    elif(ChannelB[yPoint][xPoint] !=0) and (args.bitdepth == 10):
        print 'Blue ' + str(ChannelB[yPoint][xPoint] / 64)
    elif(ChannelG[yPoint][xPoint] !=0) and (args.bitdepth == 10):
        print 'Green ' + str(ChannelG[yPoint][xPoint] / 64)
    elif(ChannelR[yPoint][xPoint] !=0) and (args.bitdepth == 10):
        print 'Red ' + str(ChannelR[yPoint][xPoint]/64)
    elif (ChannelB[yPoint][xPoint] != 0) and (args.bitdepth == 8):
        print 'Blue ' + str(ChannelB[yPoint][xPoint]/256)
    elif (ChannelG[yPoint][xPoint] != 0) and (args.bitdepth == 8):
        print 'Green ' + str(ChannelG[yPoint][xPoint] / 256)
    elif (ChannelR[yPoint][xPoint] != 0) and (args.bitdepth == 8):
        print 'Blue ' + str(ChannelR[yPoint][xPoint] / 256)

    print(args)
def _parser():
    parser = argparse.ArgumentParser(description='Check a pixel color and value in the raw image')
    parser.add_argument("input", type=str, help='input raw file')
    parser.add_argument("x", type=int, help='Position in x')
    parser.add_argument("y", type=int, help='Position in y')
    parser.add_argument("--bitdepth", type=int, default=16, help='bit depth 16 or 10 or 8')

    return parser
if __name__ == '__main__':
    main()
