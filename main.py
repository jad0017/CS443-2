# This is from the PIL module.
# I recommend using the pillow fork instead (same import name/module).
#
# Linux and OSX:
#   easy_install pillow   (or PIL if you're feeling lucky)
#
# Windows:
#   Wish upon a star?
#
from PIL import Image

import sys
import getopt
from Stuff import Matrix
from Stuff import WindowSearch
from Stuff import LogarithmicSearch
from Stuff import Util

import pickle

def get_block(pixels, xbp, ybp, N):
    (xoff, xlen) = xbp
    (yoff, ylen) = ybp
    M = Matrix.zero_matrix(N)
    for yo in range(ylen):
        y = yoff + yo
        for xo in range(xlen):
            M[yo][xo] = pixels[xoff + xo, y]
    return M

def put_block(im, xbp, ybp, N, M):
    (xoff, xlen) = xbp
    (yoff, ylen) = ybp
    for yo in range(ylen):
        y = yoff + yo
        for xo in range(xlen):
            im.putpixel((xoff + xo, y), M[yo][xo])


def block_image(imTgt, imRef, N, p, search_fn):
    (width, height) = imTgt.size
    width_blocks = width // N
    height_blocks = height // N

    #
    # The gist of this:
    #
    #  Loop over y blocks:
    #    Loop over x blocks.
    #    Ignore x overflow.
    #  Ignore y overflow.
    #
    print('[')
    for yb in range(height_blocks):
        yoff = yb * N
        for xb in range(width_blocks):
            process_block(imTgt, imRef, (yoff, xb * N), N, p, search_fn)
        # Skip partial width blocks?
    # Skip partial height blocks?
    print(']')
    return True


def process_block(imTgt, imRef, pt, N, p, search_fn):
    motion_vector = search_fn(imTgt, imRef, pt, N, (p // 2) + (p & 1))
    print(motion_vector, ',')


tgtfile = None
reffile = None
outfile = None

def usage():
    pass

if len(sys.argv) < 3:
    print("Missing arguments!")
    usage()
    sys.exit(1)
elif len(sys.argv) > 3:
    print("Too many arguments!")
    usage()
    sys.exit(1)

tgtfile = sys.argv[1]
reffile = sys.argv[2]
#outfile = sys.argv[3]

imTgt = Image.open(tgtfile)
if imTgt.mode != 'L':
    imTgt = imTgt.convert('L') # Grayscale
imRef = Image.open(reffile)
if imRef.mode != 'L':
    imRef = imRef.convert('L')

block_image(imTgt, imRef, 16, 7, LogarithmicSearch.LogarithmicSearch2D)

sys.exit(0)
