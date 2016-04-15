# The PIL python library is required to run this script.
from PIL import Image

import sys
import math

def usage():
    print("Usage: %s file1.jpg file2.jpg" % (sys.argv[0],))
    print("  file1.jpg is likely the target frame")
    print("  file2.jpg is likely the motion-componsated frame")
    sys.exit(1)


def error_gray(im1, im2):
    s = 0

    for Y in range(im1.size[1]):
        for X in range(im1.size[0]):
            s1 = im1.getpixel((X, Y))
            s2 = im2.getpixel((X, Y))

            s += pow(s1 - s2, 2)
    scalar = (im1.size[0] * im2.size[1])

    s /= scalar
    print("MSE:", str(s))

    # PSNR

    if s != 0:
        s = 20 * math.log10(255 / math.sqrt(s))
    print("PSNR:", str(s))


if not len(sys.argv) is 3:
    usage()
    sys.exit(1)

im1 = Image.open(sys.argv[1])
im2 = Image.open(sys.argv[2])

if im1.mode != 'L':
    im1 = im1.convert('L')
if im2.mode != 'L':
    im2 = im2.convert('L')

error_gray(im1, im2)
sys.exit(0)

# vim:ts=4:sws=4:st=4:ai
