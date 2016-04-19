# The PIL python library is required to run this script.
from PIL import Image, ImageDraw
import sys


def die_usage(s=None):
    if s is not None:
        print(s)
    print("Usage: %s <image> <motion vector file> <output file>"
          % (sys.argv[0],))
    sys.exit(1)


def readfile(imgname, tuplesfile, outfile):
    with open(tuplesfile, "r") as f:
        vectorlist = eval(f.read())

    im = Image.open(imgname)
    nim = im.copy()

    for val in vectorlist:
        (start, end) = val
        drawvector(nim, start, end)

    nim.save(outfile)


# NOTE: From file, tuples are in form (u,v) which corresponds with (y,x)
# on a coordinate plane
def drawvector(img, start, end):
    (y1, x1) = start
    (y2, x2) = end
    draw = ImageDraw.Draw(img)
    draw.line((x1,y1, x2,y2), fill=128)


if len(sys.argv) < 4:
    die_usage("Missing arguments!")
if len(sys.argv) > 4:
    die_usage("Too many arguments!")

imgfile = sys.argv[1]
vectorfile = sys.argv[2]
outfile = sys.argv[3]

# run
readfile(imgfile, vectorfile, outfile)
sys.exit(0)
