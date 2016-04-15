from . import MAD


def xMAD(N, ptO, ptR, imTgt, imRef):
    return MAD.MAD_img(N, ptO, MAD.uleft(ptR, N), imTgt, imRef)


def xMAD2(N, ptO, ptR, imTgt, imRef):
    return MAD.MAD_img(N, ptO, MAD.uleft2(ptR, N), imTgt, imRef)


def detectOOB(dims, pt, N):
    """
    Takes the image dimensions [img.size or (width, height)],
    and a points [(y, x)]. This function returns True if the
    MacroBlock originating at the point is outside of the
    image bounds; False otherwise.
    """
    # Use the top_left pixel as bound since center point
    # is wonky in the even case.
    if (N & 1) == 0:
        top_left = MAD.uleft2(pt, N)
    else:
        top_left = MAD.uleft(pt, N)
    # Only 4 values need to be verified:
    #  Left-most X:
    #    Checks for going off the left side of the image.
    #  Top-most Y:
    #    Checks for going off the top of the image.
    #  Bottom-most Y:
    #    Checks for going off the bottom of the image.
    #  Right-most X:
    #    Checks for going off the right side of the image.
    return ((top_left[0] < 0)
            or (top_left[1] < 0)
            or ((top_left[1] + N) >= dims[0])
            or ((top_left[0] + N) >= dims[1]))

