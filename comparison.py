import argparse
from xml.dom import minidom
from difflib import SequenceMatcher
import Levenshtein

# --------- #
# Functions #
# --------- #
def getContour(meidoc):
    ncs = meidoc.getElementsByTagName("nc")
    
    loc1 = int(ncs[0].getAttribute('loc'))
    contour = []
    
    for nc in ncs:
        loc2 = int(nc.getAttribute('loc'))
        contourval = loc2 - loc1
        contour.append(contourval)
        # Update loc1 value to the current position
        loc1 = loc2

    return contour


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Levenshtein distance between two given files')
    parser.add_argument('file1', help='name of the first file (no extension or path needed)')
    parser.add_argument('file2', help='namme of the second file (no extension or path needed)')
    args = parser.parse_args()

    # ---------- #
    # Document A #
    # ---------- #
    #meidoc_A = minidom.parse("MEI_outfiles/01_Aquit_82441_AQUIT.mei")
    meidoc_A = minidom.parse("../GABCtoMEI/MEI_outfiles/MEI_intermedfiles/" + args.file1 +".mei")
    contour_A = getContour(meidoc_A)

    # ---------- #
    # Document B #
    # ---------- #
    #meidoc_B = minidom.parse("MEI_outfiles/02_Square_85041_SQUARE.mei")
    meidoc_B = minidom.parse("../GABCtoMEI/MEI_outfiles/MEI_intermedfiles/" + args.file2 +".mei")
    contour_B = getContour(meidoc_B)

    Levenshtein.distance(contour_A, contour_B)

    print(contour_A)
    print(contour_B)

    for i in range(0, max(len(contour_A),len(contour_B))):
        if (i < len(contour_B)):
            print(contour_A[i], contour_B[i], Levenshtein.distance(contour_A[:i+1], contour_B[:i+1]))
        else:
            print(contour_A[i], None, Levenshtein.distance(contour_A[:i+1], contour_B[:i+1]))
