# The PIL python library is required to run this script.
from PIL import Image, ImageDraw
import sys
from Stuff import Util


def copy_block(ipixels, oimg, orig, dest, N):
    (oul_y, oul_x) = Util.uleft_from_center(orig, N)
    (dul_y, dul_x) = Util.uleft_from_center(dest, N)
    for y in range(N):
        yooff = oul_y + y
        ydoff = dul_y + y
        for x in range(N):
            px = ipixels[oul_x + x, yooff]
            oimg.putpixel((dul_x + x, ydoff), px)


def readfile(infile, vectorfile, outfile, N):
    iimg = Image.open(infile)
    oimg = iimg.copy()
    with open(vectorfile, "r") as f:
        vectorlist = eval(f.read())
    pixels = iimg.load()
    for val in vectorlist:
        print((val))
        (orig, dest) = val
        if orig != dest:
            print((orig, dest))
        copy_block(pixels, oimg, orig, dest, N)
    oimg.save(outfile, 'BMP')

if len(sys.argv) < 4:
    print("Too few arguments!")
    sys.exit(1)
if len(sys.argv) > 4:
    print("Too many arguments!")
    sys.exit(1)

readfile(sys.argv[1], sys.argv[2], sys.argv[3], 16)
