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
from . import Matrix

import pickle

def test_image_mode(img):
    mode = img.mode
    if mode == '1':
        print("Unsupported Image Mode: 1-bit(black and white)")
        sys.exit(1)
    elif mode == 'L':
        return True
    elif mode == 'RGB':
        return False
    elif mode == 'RGBA':
        print("Unsupported Image Mode: RGBA")
        sys.exit(1)
    elif mode == 'P':
        print("Unsupported Image Mode: Palette")
        sys.exit(1)
    print("Unsupported Image Mode:", mode)
    sys.exit(1)


def get_block(pixels, xbp, ybp, N):
    (xoff, xlen) = xbp
    (yoff, ylen) = ybp
    M = Matrix.zero_matrix(N)
    for yo in range(ylen):
        y = yoff + yo
        for xo in range(xlen):
            M[yo][xo] = pixels[xoff + xo, y]
    return M

def put_block(img, xbp, ybp, N, M):
    (xoff, xlen) = xbp
    (yoff, ylen) = ybp
    for yo in range(ylen):
        y = yoff + yo
        for xo in range(xlen):
            img.putpixel((xoff + xo, y), M[yo][xo])


def block_image(img, N=8):
    (width, height) = img.size

    width_mod = width % N
    width_blocks = width // N
    width_bp = (width - width_mod, width_mod)

    height_mod = height % N
    height_blocks = height // N
    height_bp = (height - height_mod, height_mod)

    #
    # The gist of this:
    #
    #  Loop over y blocks:
    #    Loop over x blocks.
    #    Loop over x overflow block.
    #  Loop over y overflow block:
    #    Loop over x blocks.
    #    Loop over x overflow block.
    #
    # This is probably the ugliest thing I've written in a long time.
    #

    pixels = img.load()
    for yb in range(height_blocks):
        yoff = yb * N
        ybp = (yoff, N)
        for xb in range(width_blocks):
            M = get_block(pixels, (xb * N, N), ybp, N)
            process_block(img, M)
            put_block(img, (xb * N, N), ybp, N, M)
        # Address partial width block
        if width_mod != 0:
            M = get_block(pixels, width_bp, ybp, N)
			process_block(img, M)
            put_block(img, width_bp, ybp, N, M)
    # Address parital height block
    if height_mod != 0:
        for xb in range(width_blocks):
            M = get_block(pixels, (xb * N, N), height_bp, N)
			process_block(img, M)
			put_block(img, (xb * N, N), height_bp, N, M)
        # Address lower right block if partial height and partial width
        if width_mod != 0:
            M = get_block(pixels, width_bp, height_bp, N)
			process_block(img, M)
            put_block(img, width_bp, height_bp, N, M)
    return True



def process_block(oimg, M, spec):
    # Single Channel: Luminance
    D = DCT.DCT(M)
    add_dct_block(D)
    C = Quantize.quantize(D, Quantize.QBASE_LUM)
    R = RLC.RLC(C)
    oimg.write_block_rlc(R)


infile = None
outfile = None

if len(args) < 1:
    print("Missing arguments!")
    usage()
    sys.exit(1)
elif len(args) > 1:
    print("Too many arguments!")
    usage()
    sys.exit(1)

infile = args[0]
#outfile = args[1]

img = Image.open(infile)
if not test_image_mode(img):
    img = img.convert('L') # Grayscale

block_image(img)

sys.exit(0)
