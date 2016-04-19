# The PIL python library is required to run this script.
from PIL import Image, ImageDraw
import sys
from Stuff import Util

def die_usage(s = None):
    if s is not None:
        print(s)
    print("Usage: %s <image> <motion vector list> <outfile> [N]")
    sys.exit(1)


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
    die_usage("Too few arguments!")
if len(sys.argv) > 5:
    die_usage("Too many arguments!")

infile = sys.argv[1]
vectorfile = sys.argv[2]
outfile = sys.argv[3]

if len(sys.argv) == 5:
    try:
        N = int(sys.argv[4])
    except ValueError:
        die_usage("N is not an integer!")
else:
    N = 16

readfile(infile, vectorfile, outfile, N)
sys.exit(0)
