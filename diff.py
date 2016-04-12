# The PIL python library is required to run this script.
from PIL import Image

import sys
import math
import Compressor.Colors

def usage():
    print("Usage: %s target.jpg reference.jpg mcf.jpg FD_out.bmp DFD_out.bmp [other_out.bmp]" % (sys.argv[0],))
    sys.exit(1)


def Other(p1, p2):
    if p1 > p2:
        return 255 - (p1 - p2)
    return p2 - p1

def FD(p1, p2):
    return int(abs(p1 - p2))

def diff_gray(imTgt, imRef, imMC, out_FD, out_DFD, out_other=None):
    oFD = Image.new('L', im1.size)
    oDFD = Image.new('L', im1.size)
    if out_other is not None:
        oOther = Image.new('L', im1.size)
    for Y in range(im1.size[1]):
        for X in range(im1.size[0]):
            pt = imTgt.getpixel((X, Y))
            pr = imRef.getpixel((X, Y))
            pm = imMC.getpixel((X, Y))
            oFD.putpixel((X,Y), FD(pt, pr))
            oDFD.putpixel((X,Y), FD(pt, pm))
            if out_other is not None:
                oOther.putpixel((X,Y), Other(pt, pm))
    oFD.save(out_FD, 'BMP')
    oDFD.save(out_DFD, 'BMP')
    if out_other is not None:
       oOther.save(out_other, 'BMP')


def diff_rgb(im1, im2, outfile):
    oimg = Image.new('RGB', im1.size)
    for Y in range(im1.size[1]):
        for X in range(im1.size[0]):
            (r1, g1, b1) = im1.getpixel((X, Y))
            (r2, g2, b2) = im2.getpixel((X, Y))
            P = (val(r1, r2), val(g1, g2), val(b1, b2))
            oimg.putpixel((X,Y), P)
    oimg.save(outfile, 'BMP')


if (len(sys.argv) < 6) or (len(sys.argv) > 7):
    usage()
    sys.exit(1)

imTgt = Image.open(sys.argv[1])
imRef = Image.open(sys.argv[2])
imMC = Image.open(sys.argv[3])
out_FD = sys.argv[4]
out_DFD = sys.argv[5]
if len(sys.argv) == 7:
    out_other = sys.argv[6]
else:
    out_other = None

if imTgt.size != imRef.size:
    print("Images are different sizes!")
    sys.exit(1)

if imTgt.mode != 'L':
    imTgt = imTgt.convert('L') # Grayscale it
if imRef.mode != 'L':
    imRef = imRef.convert('L') # Grayscale it
if imMC.mode != 'L':
    imMC = imMC.convert('L') # Grayscale it


diff_gray(imTgt, imRef, imMC, out_FD, out_DFD, out_other)
sys.exit(0)

# vim:ts=4:sws=4:st=4:ai
