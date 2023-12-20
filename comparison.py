import argparse
import csv
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
    parser.add_argument('-file1', help='name of the first file (no extension or path needed)')
    parser.add_argument('-file2', help='namme of the second file (no extension or path needed)')
    parser.add_argument('-csvfile', help='csv file listing all the MEI Neumes files to compare', default=None)
    args = parser.parse_args()

    # CSV file containing the list of the files to cmpare
    if(args.csvfile):
        pass

    # Two files to compare
    else:
        # First file
        #### TO DO: Eventually substitute by "MEI_outfiles," this would mean to translate pitches to contour for square notation files
        meidoc_A = minidom.parse("../GABCtoMEI/MEI_outfiles/MEI_intermedfiles/" + args.file1 + ".mei")
        contour_A = getContour(meidoc_A)
        print(contour_A)

        # Second file
        #### TO DO: Eventually substitute by "MEI_outfiles," this would mean to translate pitches to contour for square notation files
        meidoc_B = minidom.parse("../GABCtoMEI/MEI_outfiles/MEI_intermedfiles/" + args.file2 + ".mei")
        contour_B = getContour(meidoc_B)
        print(contour_B)

        # Calculate Levenshtein distance
        Levenshtein.distance(contour_A, contour_B)
        # Print the results
        for i in range(0, max(len(contour_A),len(contour_B))):
            if (i < len(contour_A) and i < len(contour_B)):
                print(contour_A[i], contour_B[i], Levenshtein.distance(contour_A[:i+1], contour_B[:i+1]))
            elif (i >= len(contour_A) and i < len(contour_B)):
                print(None, contour_B[i], Levenshtein.distance(contour_A[:i+1], contour_B[:i+1]))
            elif (i < len(contour_A) and i >= len(contour_B)):
                print(contour_A[i], None, Levenshtein.distance(contour_A[:i+1], contour_B[:i+1]))
            # else: doesn't happen
