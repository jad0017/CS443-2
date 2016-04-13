from PIL import Image


def idiff(p1, p2):
    if p1 > p2:
        return p1 - p2
    return p2 - p1

def MAD_rel(C, R):
    """ Assumption:  C and R are the same dimensions. """
    d = 0
    for i in range(len(C)):
        for j in range(len(C[0])):
            d += idiff(C[i][j], R[i][j])
    return float(d) / float(len(C) * len(C))



def MAD_img(N, ptC, ptR, C, R):
    d = 0
    for i in range(N):
        C_i = i + ptC[0]
        R_i = i + ptR[0]
        for j in range(N):
            C_j = j + ptC[1]
            R_j = j + ptR[1]
            Cpx = C.getpixel((C_i, C_j))
            Rpx = R.getpixel((R_i, R_j))
            d += idiff(Cpx, Rpx)
    return float(d) / float(N * N)


def uleft(pt, N):
    Nd2 = N / 2
    return (pt[0] - Nd2, pt[1] - Nd2)


# TODO: Factor in edges of image
def search_points(imTgt, imRef, ptO, ptC, N, S):
    (center_i, center_j) = ptC
    points = [
        (center_i - S, center_j), # Above the macro block
        (center_i + S, center_j), # Below the macro block
        (center_i, center_j - S), # Left of the macro block
        (center_i, center_j + S), # Right of the macro block
    ]
    sidx = -1
    ptOL = uleft(ptO, N)
    sweight = MAD_img(N, ptOL, uleft(ptC, N), imTgt, imRef)
    for x in range(len(points)):
        w = MAD_img(N, ptOL, uleft(points[x], N), imTgt, imRef)
        # Check if minimum
        if w < sweight:
            sweight = w
            sidx = x
    if sidx == -1:
        S = S / 2
    return (S, points[sidx])


def LS2D_odd(imTgt, imRef, md_i, md_j, N, S):
    Nd2 = N / 2
    cTgt = (md_i + Nd2, md_j + Nd2)
    cRef = (cTgt[0], cTgt[1])
    while S != 1:
        (S, cRef) = search_points(imTgt, imRef, cTgt, CRef, N, S)
    return (cTgt, cRef) # Return the motion vector


# [ - - - - - - - - - - ]
# [ - - - - - - - - - - ]
# [ - - - - - - - - - - ]
# [ - - - x x x x - - - ]
# [ - - - x C c x - - - ]
# [ - - - x c c x - - - ]
# [ - - - x x x x - - - ]
# [ - - - - - - - - - - ]
# [ - - - - - - - - - - ]
# [ - - - - - - - - - - ]
def uleft2(pt, N):
    Nd2 = (N / 2) - 1
    return (pt[0] - Nd2, pt[1] - Nd2)


# TODO: Factor in edges of image
def search_points2(imTgt, imRef, ptO, ptC, N, S):
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
    ptOL = uleft2(ptO, N)
    sweight = MAD_img(N, ptOL, uleft2(ptC, N), imTgt, imRef)
    for x in range(len(points)):
        w = MAD_img(N, ptOL, uleft2(points[x], N), imTgt, imRef)
        # Check if minimum
        if w < sweight:
            sweight = w
            sidx = x
    if sidx == -1:
        S = S / 2
    return (S, points[sidx])



def LS2D_even(imTgt, imRef, md_i, md_j, N, S):
    Nd2 = (N / 2) - 1
    cTgt = (md_i + Nd2, md_j + Nd2)
    cRef = (cTgt[0], cTgt[1])
    while S != 1:
        (S, cRef) = search_points2(imTgt, imRef, cTgt, CRef, N, S)
    return (cTgt, cRef) # Return the motion vector



# Should be using S = p/2 + (p&1)
def LogarithmicSearch2D(imTgt, imRef, ptTgt, N, S=8):
    """ ptTgt is the upper left pixel of the Macro bock in the target """

    # Given the block edge length, N, we can determine the center.
    # Granted, N is likely even, so we can't select an absolute center
    # in that case.

    if (N & 1) == 1:
        return LS2D_odd(imTgt, imRef, ptTgt[0], ptTgt[1], N, p, S)
    return LS2D_even(imTgt, imRef, ptTgt[0], ptTgt[1], N, p, S)

