# The PIL python library is required to run this script.
from PIL import Image, ImageDraw

def readfile(imgname, tuplesfile):
    n = 0
    with open(tuplesfile, "r") as f:
        vectorlist = eval(f.read())

        #create image - fix to take in image as parameter
        im = Image.open(imgname)
        im.save('outputimage.bmp')
        j = 1

        for i, val in enumerate(vectorlist):
            (startcoord, endcoord) = vectorlist[i]
            drawvector('outputimage.bmp', startcoord, endcoord)

# NOTE: From file, tuples are in form (u,v) which corresponds with (y,x) on a coordinate plane
def drawvector(filename, start, end):
    (y1, x1) = start
    (y2, x2) = end
    im = Image.open(filename)
    draw = ImageDraw.Draw(im)
    draw.line((x1,y1, x2+3,y2+3), fill=128)
    im.save('outputimage.bmp')

# run
readfile('frame1.bmp', 'sample2_frame2_to_frame1')
