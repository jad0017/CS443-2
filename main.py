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
from Stuff import SequentialSearch
from Stuff import LogarithmicSearch
from Stuff import Util

import pickle

def usage():
    print("Usage: %s [options] <target_img> <reference_img> <vector_outfile>"
          % (sys.argv[0],))
    print("""\

Options:
  -L, --logarithmic-search  Use the 2D Logarithmic Search Block-matching algorithm
  -S, --sequential-search   Use the Sequential Search Block-matching algorithm
                            (default)
  -W, --window-search       Use the Window Search Block-matching algorithm
  -N <val>                  Set N (default: 16)
  -p <val>                  Set p (default: 7)
""")


def die_usage(s = None):
    if s is not None:
        print(s)
    usage()
    sys.exit(1)


def die(s):
    print(s)
    sys.exit(1)


def block_image(imTgt, imRef, outfile, N, p, search_fn):
    (width, height) = imTgt.size
    width_blocks = width // N
    height_blocks = height // N

    try:
        out = open(outfile, "w")
    except:
        die("Failed to open outfile: %s" % (outfile,))

    #
    # The gist of this:
    #
    #  Loop over y blocks:
    #    Loop over x blocks.
    #    Ignore x overflow.
    #  Ignore y overflow.
    #
    out.write('[\n')
    for yb in range(height_blocks):
        yoff = yb * N
        for xb in range(width_blocks):
            process_block(imTgt, imRef, (yoff, xb * N), N, p, search_fn, out)
        # Skip partial width blocks?
    # Skip partial height blocks?
    out.write(']\n')
    return True


def process_block(imTgt, imRef, pt, N, p, search_fn, out):
    motion_vector = search_fn(imTgt, imRef, pt, N, (p // 2) + (p & 1))
    out.write(str(motion_vector) + ',\n')


def window_search(imTgt, imRef, pt, N, p):
    S = (p // 2) + (p & 1)
    return WindowSearch.WindowSearch(imTgt, imRef, pt, N, S)


def logarithmic_search(imTgt, imRef, pt, N, p):
    S = (p // 2) + (p & 1)
    return LogarithmicSearch.LogarithmicSearch2D(imTgt, imRef, pt, N, S)


def sequential_search(imTgt, imRef, pt, N, p):
    S = (2 * p) + 1
    return SequentialSearch.SequentialSearch(imTgt, imRef, pt, N, S)


tgtfile = None
reffile = None
outfile = None

alg = None

N = None
p = None

def test_pos_int(x, s):
    try:
        i = int(x)
    except ValueError:
        die_usage(s)
    if i <= 0:
        die_usage(s)
    return i


try:
    longopts=["help", "sequential-search", "logarithmic-search",
              "window-search"]
    opts, args = getopt.gnu_getopt(sys.argv[1:], "hLSWN:p:", longopts)
except getopt.GetoptError as err:
    die_usage(str(err))

for o,a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit(0)
    elif o in ("-S", "--sequential-search"):
        if alg is not None:
            die_usage("Only one search type may be given!")
        alg = sequential_search
    elif o in ("-L", "--logarithmic-search"):
        if alg is not None:
            die_usage("Only one search type may be given!")
        alg = logarithmic_search
    elif o in ("-W", "--window-search"):
        if alg is not None:
            die_usage("Only one search type may be given!")
        alg = window_search
    elif o == '-N':
        N = test_pos_int(a, "N must be a positive integer!")
    elif o == '-p':
        p = test_pos_int(a, "p must be a positive integer!")
    else:
        die_usage("Unknown options: %s" % (o,))

if len(args) < 3:
    die_usage("Missing arguments!")
elif len(args) > 3:
    die_usage("Too many arguments!")

tgtfile = args[0]
reffile = args[1]
outfile = args[2]

imTgt = Image.open(tgtfile)
if imTgt.mode != 'L':
    imTgt = imTgt.convert('L') # Grayscale
imRef = Image.open(reffile)
if imRef.mode != 'L':
    imRef = imRef.convert('L')

if alg is None:
    alg = sequential_search

if N is None:
    N = 16
if p is None:
    p = 7

block_image(imTgt, imRef, outfile, N, p, alg)
sys.exit(0)
