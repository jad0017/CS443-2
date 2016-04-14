from PIL import Image
from . import MAD

def xMAD(N, ptO, ptR, imTgt, imRef):
    return MAD.MAD_img(N, ptO, MAD.uleft(ptR, N), imTgt, imRef)


def xMAD2(N, ptO, ptR, imTgt, imRef):
    return MAD.MAD_img(N, ptO, MAD.uleft2(ptR, N), imTgt, imRef)


# TODO: Factor in edges of image
def search_points(imTgt, imRef, ptO, ptC, N, S, store):
    (center_i, center_j) = ptC
    points = [
        (center_i - S, center_j), # Above the macro block
        (center_i + S, center_j), # Below the macro block
        (center_i, center_j - S), # Left of the macro block
        (center_i, center_j + S), # Right of the macro block
    ]
    sidx = -1
    ptOL = MAD.uleft(ptO, N)

    sweight = store.get(ptC, default=None)
    if sweight is None:
        sweight = xMAD(N, ptOL, ptC, imTgt, imRef)
        store[ptC] = sweight
    for x in range(len(points)):
        w = store.get(points[x], default=None)
        if w is None:
            w = xMAD(N, ptOL, points[x], imTgt, imRef)
            store[points[x]] = w
        # Check if minimum
        if w < sweight:
            sweight = w
            sidx = x
    if sidx == -1:
        return ((S / 2) + (S & 1), ptC) # floor(S / 2)
    return (S, points[sidx])


def LS2D_odd(imTgt, imRef, md_i, md_j, N, S):
    Nd2 = N / 2
    cTgt = (md_i + Nd2, md_j + Nd2)
    cRef = (cTgt[0], cTgt[1])
    store = dict()
    while S != 1:
        (S, cRef) = search_points(imTgt, imRef, cTgt, CRef, N, S, store)
    return (cTgt, cRef) # Return the motion vector


# TODO: Factor in edges of image
def search_points2(imTgt, imRef, ptO, ptC, N, S, store):
    # Center is the upper left of a 2x2 block of pixels
    s = S - 2
    (center_i, center_j) = ptC
    points = [
        (center_i - s, center_j),     # Above the macro block
        (center_i + s + 1, center_j), # Below the macro block
        (center_i, center_j - s),     # Left of the macro block
        (center_i, center_j + s + 1), # Right of the macro block
    ]
    sidx = -1
    ptOL = MAD.uleft2(ptO, N)

    sweight = store.get(ptC, default=None)
    if sweight is None:
        sweight = xMAD2(N, ptOL, ptC, imTgt, imRef)
        store[ptC] = sweight
    for x in range(len(points)):
        w = store.get(points[x], default=None)
        if w is None:
            w = xMAD2(N, ptOL, points[x], imTgt, imRef)
            store[points[x]] = w
        # Check if minimum
        if w < sweight:
            sweight = w
            sidx = x
    if sidx == -1:
        return ((S / 2) + (S & 1), ptC) # floor(S / 2)
    return (S, points[sidx])



def LS2D_even(imTgt, imRef, md_i, md_j, N, S):
    Nd2 = (N / 2) - 1
    cTgt = (md_i + Nd2, md_j + Nd2)
    cRef = (cTgt[0], cTgt[1])
    store = dict()
    while S != 1:
        (S, cRef) = search_points2(imTgt, imRef, cTgt, CRef, N, S, store)
    return (cTgt, cRef) # Return the motion vector



# Should be using S = p/2 + (p&1)
def LogarithmicSearch2D(imTgt, imRef, ptTgt, N, S=8):
    """ ptTgt is the upper left pixel of the Macro bock in the target """

    # Given the block edge length, N, we can determine the center.
    # Granted, N is likely even, so we can't select an absolute center
    # in that case.

    if (N & 1) == 1:
        return LS2D_odd(imTgt, imRef, ptTgt[0], ptTgt[1], N, S)
    return LS2D_even(imTgt, imRef, ptTgt[0], ptTgt[1], N, S)

