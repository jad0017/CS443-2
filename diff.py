# The PIL python library is required to run this script.
from PIL import Image

import sys
import math
import Compressor.Colors

def usage():
    print("Usage: %s image1.jpg image2.jpg out.bmp" % (sys.argv[0],))
    print("       %s target.jpg reference.jpg FD.bmp" % (sys.argv[0],))
    print("       %s target.jpg MC.jpg DFD.bmp" % (sys.argv[0],))
    sys.exit(1)


def Other(p1, p2):
    if p1 > p2:
        return 255 - (p1 - p2)
    return p2 - p1


# Other is a much better version.
def FD(p1, p2):
    if p1 > p2:
        return p1 - p2
    return p2 - p1


def diff_gray(im1, im2, outfile):
    oimg = Image.new('L', im1.size)
    for Y in range(im1.size[1]):
        for X in range(im1.size[0]):
            p1 = im1.getpixel((X, Y))
            p2 = im2.getpixel((X, Y))
            oimg.putpixel((X,Y), Other(p1, p2));
    oimg.save(outfile, 'BMP')


if len(sys.argv) != 4:
    usage()
    sys.exit(1)

im1 = Image.open(sys.argv[1])
im2 = Image.open(sys.argv[2])
outfile = sys.argv[3]

if im1.size != im2.size:
    print("Images are different sizes!")
    sys.exit(1)

if im1.mode != 'L':
    im1 = im1.convert('L') # Grayscale it

if im2.mode != 'L':
    im2 = im2.convert('L')

diff_gray(im1, im2, outfile)
sys.exit(0)

# vim:ts=4:sws=4:st=4:ai
