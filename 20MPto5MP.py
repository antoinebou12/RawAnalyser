import os
import sys
from os.path import basename
import tifffile as tiff
import numpy as np
import argparse
import argcomplete
global args
global file
global f

def main():
    global args
    global file
    global f
    parser = _parser()
    argcomplete.autocomplete(parser)
    args = _parser().parse_args()
    if args.folder == 'folder':
        for file in os.listdir(args.input):
            if file[-3:] == 'raw':
                print file
                f = open(args.input+ '/' + file, "rb")
                _imageConvert()
    elif args.folder == 'file':
        f = open(args.input, "rb")
        _imageConvert()

def _imageConvert():
    cols_count = args.width
    rows_count = args.height
    image_array = np.fromfile(f, dtype=np.uint16, count=(cols_count * rows_count))

    matrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
    matrix = np.array(matrix)
    matrix = np.reshape(image_array, (rows_count, cols_count))

    if args.gain == 16:
        matrix = matrix * (args.gain*4)
        if args.tiff == 'tiff':
            if args.folder == 'folder':
                tiff.imsave(args.output + '/' + str(os.path.splitext(basename(file))[0])+ '_old' + '.tiff', matrix)
            elif args.folder == 'file':
                tiff.imsave(args.output + '/' + str(os.path.splitext(basename(args.input))[0]) + '_old' + '.tiff', matrix)
        matrix = matrix / (args.gain * 4)
        matrix = matrix * (args.gain)
    elif args.gain == 10:
        if args.tiff == 'tiff':
            if args.folder == 'folder':
                tiff.imsave(args.output + '/' + str(os.path.splitext(basename(file))[0]) + '_old' + '.tiff', matrix)
            elif args.folder == 'file':
                tiff.imsave(args.output + '/' + str(os.path.splitext(basename(args.input))[0]) + '_old' + '.tiff', matrix)
    new_array = [[0 for x in range(cols_count/2)] for y in range(rows_count/2)]

    for i in range(0, cols_count, 4):
        for j in range(0, rows_count, 4):
            new_array[j/2][i/2] = matrix[j][i] + matrix[j][i + 1] + matrix[j + 1][i] + matrix[j + 1][i + 1]
    for i in range(2, cols_count, 4):
        for j in range(0, rows_count, 4):
            new_array[j/2][i/2] = matrix[j][i] + matrix[j][i + 1] + matrix[j + 1][i] + matrix[j + 1][i + 1]
    for i in range(0, cols_count, 4):
        for j in range(2, rows_count, 4):
            new_array[j/2][i/2] = matrix[j][i] + matrix[j][i + 1] + matrix[j + 1][i] + matrix[j + 1][i + 1]
    for i in range(2, cols_count, 4):
        for j in range(2, rows_count, 4):
            new_array[j/2][i/2] = matrix[j][i] + matrix[j][i + 1] + matrix[j + 1][i] + matrix[j + 1][i + 1]


    new_array = np.array(new_array)
    new_array = np.reshape( new_array, ((rows_count/2),(cols_count/2)))
    if args.tiff == 'tiff':
        if args.folder == 'folder':
            tiff.imsave(args.output + '/' + str(basename(file)) + '_5mp' + '.tiff',  new_array)
            if args.gain == 16:
                new_array = new_array / 16
                new_array = np.reshape(new_array, ((rows_count / 2)*(cols_count / 2),1))
                new_array.astype('int16').tofile(
                args.output + '/' + str(os.path.splitext(basename(file))[0]) + '_5mp' + '.raw')
            elif args.gain == 10:
                new_array = np.reshape(new_array, ((rows_count / 2) * (cols_count / 2), 1))
                new_array.astype('int16').tofile(
                    args.output + '/' + str(os.path.splitext(basename(file))[0]) + '_5mp' + '.raw')
        elif args.folder == 'file':
            tiff.imsave(args.output + '/' + str(basename(args.input)) + '_5mp' + '.tiff', new_array)
            if args.gain == 16:
                new_array = new_array / 16
                new_array = np.reshape(new_array, ((rows_count / 2) * (cols_count / 2), 1))
                new_array.astype('int16').tofile(
                args.output + '/' + str(os.path.splitext(basename(args.input))[0]) + '_5mp' + '.raw')
            elif args.gain == 10:
                new_array.astype('int16').tofile(
                    args.output + '/' + str(os.path.splitext(basename(args.input))[0]) + '_5mp' + '.raw')
    elif args.tiff == 'notiff':
        if args.folder == 'folder':
            if args.gain == 16:
                new_array = new_array / 16
                new_array = np.reshape(new_array, ((rows_count / 2) * (cols_count / 2), 1))
                new_array.astype('int16').tofile(
                args.output + '/' + str(os.path.splitext(basename(file))[0]) + '_5mp' + '.raw')
            elif args.gain == 10:
                new_array = np.reshape(new_array, ((rows_count / 2) * (cols_count / 2), 1))
                new_array.astype('int16').tofile(
                    args.output + '/' + str(os.path.splitext(basename(file))[0]) + '_5mp' + '.raw')
        elif args.folder == 'file':
            if args.gain == 16:
                new_array = new_array/16
                new_array = np.reshape(new_array, ((rows_count / 2) * (cols_count / 2), 1))
                new_array.astype('int16').tofile(
                args.output + '/' + str(os.path.splitext(basename(args.input))[0]) + '_5mp' + '.raw')
            elif args.gain == 10:
                new_array = np.reshape(new_array, ((rows_count / 2) * (cols_count / 2), 1))
                new_array.astype('int16').tofile(
                    args.output + '/' + str(os.path.splitext(basename(args.input))[0]) + '_5mp' + '.raw')

def _parser():
    parser = argparse.ArgumentParser(description='.raw file to .tiff file format')
    parser.add_argument("--input", default=".", type=str, help='input folder or file to check for new raw file')
    parser.add_argument("--output",default=".", type=str, help='output folder to check for new tiff file')
    parser.add_argument("--width",default=5184, type=int, help='width of the picture')
    parser.add_argument("--height",default=3904, type=int, help='height of the picture')
    parser.add_argument("--folder",default='folder', type=str, help='input folder to check for new raw file')
    parser.add_argument("--tiff",default='notiff', type=str, help='tiff')
    parser.add_argument("--gain", type=int,default=10, help='gain for the old and new resolution')

    return parser
if __name__ == "__main__":
    main()