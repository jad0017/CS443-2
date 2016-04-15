from . import MAD

# Get the upper left pixel of an odd-edge length
# block when given the center point.
#
# For Odd blocks:
# [ - - - - - - - - - ]
# [ - - - - - - - - - ]
# [ - - - - - - - - - ]
# [ - - - x x x - - - ]
# [ - - - x C x - - - ]
# [ - - - x x x - - - ]
# [ - - - - - - - - - ]
# [ - - - - - - - - - ]
# [ - - - - - - - - - ]
#
# For Even blocks:
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
def uleft_from_center(pt, N):
    Nd2 = (N / 2) - int((N & 1) == 0)
    return (pt[0] - Nd2, pt[1] - Nd2)


def center_from_uleft(pt, N):
    Nd2 = (N / 2) - int((N & 1) == 0)
    return (pt[0] + Nd2, pt[1] + Nd2)


def xMAD(N, ptO, ptR, imTgt, imRef):
    return MAD.MAD_img(N, ptO, uleft_from_center(ptR, N), imTgt, imRef)


def detectOOB(dims, pt, N):
    """
    Takes the image dimensions [img.size or (width, height)],
    and a points [(y, x)]. This function returns True if the
    MacroBlock originating at the point is outside of the
    image bounds; False otherwise.
    """
    # Use the top_left pixel as bound since center point
    # is wonky in the even case.
    top_left = uleft_from_center(pt, N)
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

