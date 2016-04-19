from PIL import Image
from . import Util


# Should be using S = p/2 + (p&1)
def SequentialSearch(imTgt, imRef, ptTgt, N, S=8):
    """ ptTgt is the upper left pixel of the Macro bock in the target """
    cTgt = Util.center_from_uleft(ptTgt, N)
    cRef = cTgt;
    sweight = Util.xMAD(N, ptTgt, cRef, imTgt, imRef)
    # Upper left of the search window.
    (swy, swx) = Util.uleft_from_center(cTgt, S)
    for yoff in range(S):
        y = swy + yoff
        if y < 0:
            continue
        for xoff in range(S):
            x = swx + xoff
            if (x < 0) or Util.detectOOB(imTgt.size, (y, x), N):
                continue
            w = Util.xMAD(N, ptTgt, (y, x), imTgt, imRef);
            if (w < sweight):
                sweight = w
                cRef = (y, x)
    return (cTgt, cRef) # Return the motion vector


