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
        C_i = i + ptC[1]
        R_i = i + ptR[1]
        for j in range(N):
            C_j = j + ptC[0]
            R_j = j + ptR[0]
            Cpx = C.getpixel((C_i, C_j))
            Rpx = R.getpixel((R_i, R_j))
            d += idiff(Cpx, Rpx)
    return float(d) / float(N * N)



