import os
import tifffile as tiff
import numpy as np
import argparse
import argcomplete

def main():
    parser = _parser()
    argcomplete.autocomplete(parser)
    args = _parser().parse_args()
    f = open(args.input, "rb")
    cols_count = args.width
    rows_count = args.height
    image_array = np.fromfile(f, dtype=np.uint16, count=cols_count * rows_count)
    matrix = [[0 for x in range(cols_count)] for y in range(rows_count)]
    matrix = np.array(matrix)
    matrix = np.reshape(image_array, (1088, 1928))
    tiff.imsave(args.output + '/' + str(os.path.splitext(args.input)[0]) + '.tiff', matrix )
def _parser():
    parser = argparse.ArgumentParser(description='.raw file to .tiff file format')
    parser.add_argument("input", type=str, help='input file to check for new raw file')
    parser.add_argument("output", type=str, help='output folder to check for new tiff file')
    parser.add_argument("width", type=int, help='width of the picture')
    parser.add_argument("height", type=int, help='height of the picture')

    return parser
if __name__ == "__main__":
    main()