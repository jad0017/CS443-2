from PIL import Image
from . import Util


def search_points(imTgt, imRef, ptO, ptC, N, S):
    (center_i, center_j) = ptC
    points = [
        (center_i - S, center_j), # North of the macro block
        (center_i + S, center_j), # South of the macro block
        (center_i, center_j - S), # West of the macro block
        (center_i, center_j + S), # East of the macro block
        (center_i - S, center_j - S), # NorthWest of the macro block
        (center_i - S, center_j + S), # NorthEast of the macro block
        (center_i + S, center_j - S), # SouthWest of the macro block
        (center_i + S, center_j + S), # SouthEast of the macro block
    ]
    sidx = -1
    ptOL = Util.uleft_from_center(ptO, N)
    sweight = Util.xMAD(N, ptOL, ptC, imTgt, imRef)
    for x in range(len(points)):
        if Util.detectOOB(imTgt.size, points[x], N):
            continue
        w = Util.xMAD(N, ptOL, points[x], imTgt, imRef)
        # Check if minimum
        if w < sweight:
            sweight = w
            sidx = x
    if sidx == -1:
        return ptC
    return points[sidx]


def WS_odd(imTgt, imRef, ptTgt, N, S):
    cTgt = Util.center_from_uleft(ptTgt, N)
    cRef = (cTgt[0], cTgt[1])
    while True:
        cRef = search_points(imTgt, imRef, cTgt, cRef, N, S)
        if S == 1:
            break
        S = (S // 2) + (S & 1) # ceil(S / 2)
    return (cTgt, cRef) # Return the motion vector


def search_points2(imTgt, imRef, ptO, ptC, N, S):
    # Center is the upper left of a 2x2 block of pixels
    s = S - 2
    (center_i, center_j) = ptC
    points = [
        (center_i - s, center_j),     # North the macro block
        (center_i + s + 1, center_j), # South the macro block
        (center_i, center_j - s),     # West of the macro block
        (center_i, center_j + s + 1), # East of the macro block
        (center_i - s, center_j - s),     # NorthWest of the macro block
        (center_i - s, center_j + s + 1), # NorthEast of the macro block
        (center_i + s + 1, center_j - s),     # SouthWest of the macro block
        (center_i + s + 1, center_j + s + 1), # SouthEast of the macro block
    ]
    sidx = -1
    ptOL = Util.uleft_from_center(ptO, N)
    sweight = Util.xMAD(N, ptOL, ptC, imTgt, imRef)
    for x in range(len(points)):
        if Util.detectOOB(imTgt.size, points[x], N):
            continue
        w = Util.xMAD(N, ptOL, points[x], imTgt, imRef)
        # Check if minimum
        if w < sweight:
            sweight = w
            sidx = x
    if sidx == -1:
        return ptC
    return points[sidx]



def WS_even(imTgt, imRef, ptTgt, N, S):
    cTgt = Util.center_from_uleft(ptTgt, N)
    cRef = (cTgt[0], cTgt[1])
    while True:
        cRef = search_points2(imTgt, imRef, cTgt, cRef, N, S)
        if S == 1:
            break
        S = (S // 2) + (S & 1) # ceil(S / 2)
    return (cTgt, cRef) # Return the motion vector



# Should be using S = p/2 + (p&1)
def WindowSearch(imTgt, imRef, ptTgt, N, S=8):
    """ ptTgt is the upper left pixel of the Macro bock in the target """

    # Given the block edge length, N, we can determine the center.
    # Granted, N is likely even, so we can't select an absolute center
    # in that case.

    if (N & 1) == 1:
        return WS_odd(imTgt, imRef, ptTgt, N, S)
    return WS_even(imTgt, imRef, ptTgt, N, S)

