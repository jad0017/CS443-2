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


# Get the upper left pixel of an odd-edge length
# block when given the center point.
# [ - - - - - - - - - ]
# [ - - - - - - - - - ]
# [ - - - - - - - - - ]
# [ - - - x x x - - - ]
# [ - - - x C x - - - ]
# [ - - - x x x - - - ]
# [ - - - - - - - - - ]
# [ - - - - - - - - - ]
# [ - - - - - - - - - ]
def uleft(pt, N):
    Nd2 = N / 2
    return (pt[0] - Nd2, pt[1] - Nd2)


# Get the upper left pixel of an even-edge length
# block when given the center point.
# Note: The center point is the upper left of the
# 2x2 center block
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

