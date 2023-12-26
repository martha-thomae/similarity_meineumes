import argparse
import csv
from xml.dom import minidom
from difflib import SequenceMatcher
from minineedle import needle, smith, core

# --------- #
# Functions #
# --------- #
def getContour(meidoc):
    ncs = meidoc.getElementsByTagName("nc")
    
    loc1 = int(ncs[0].getAttribute('loc'))
    contour = []
    syltexts = []
    
    for nc in ncs:
        loc2 = int(nc.getAttribute('loc'))
        contourval = loc2 - loc1
        contour.append(contourval)
        # Update loc1 value to the current position
        loc1 = loc2

        syllable = nc.parentNode.parentNode
        syl = syllable.getElementsByTagName('syl')[0]
        sylchild = syl.firstChild
        if(sylchild):
            syltext = sylchild.nodeValue
        else:
            syltext = None
        syltexts.append(syltext)

    return contour, syltexts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Levenshtein distance between two given files')
    parser.add_argument('-file1', help='name of the first file (no extension or path needed)')
    parser.add_argument('-file2', help='namme of the second file (no extension or path needed)')
    parser.add_argument('-csvfile', help='csv file listing all the MEI Neumes files to compare', default=None)
    args = parser.parse_args()

    # CSV file containing the list of the files to compare
    if(args.csvfile):
        all_entries = []
        with open(args.csvfile, encoding='utf-8-sig') as csvfile:
            csv_content = csv.reader(csvfile, delimiter=';', quotechar='\n')
            for row in csv_content:
                all_entries.append(row)
        csvfile.close()
        print(all_entries)

        for row in all_entries:
            meidoc_A = minidom.parse("../GABCtoMEI/MEI_outfiles/MEI_intermedfiles/" + row[0] + ".mei")
            contour_A, syltexts_A = getContour(meidoc_A)
            meidoc_B = minidom.parse("../GABCtoMEI/MEI_outfiles/MEI_intermedfiles/" + row[1] + ".mei")
            contour_B, syltexts_B = getContour(meidoc_B)
            #### TO DO: Eventually substitute by "MEI_outfiles," this would mean to translate pitches to contour for square notation files

            # Calculate alignment
            alignment = needle.NeedlemanWunsch(contour_A, contour_B)
            alignment.gap_character = "_"
            # Print the results
            print(row[0], "|", row[1], "|", "SCORE: " + str(alignment.get_score()), "|", "IDENTITY % OF ALIGNMENT: " + str(alignment.get_identity()))
            print()
            print(alignment)

            difference = 0
            matches = 0
            alig1, alig2 = alignment.get_aligned_sequences()
            for i in range(0, len(alig1)):
                if (alig1[i] == alig2[i]):
                    # match
                    matches += 1
                else:
                    # mismatch or indel
                    difference += 1
            print("MATCHES: " + str(matches))
            print("DIFFERENCES: " + str(difference))
            print()


    # Two files to compare
    else:
        # First file
        meidoc_A = minidom.parse("../GABCtoMEI/MEI_outfiles/MEI_intermedfiles/" + args.file1 + ".mei")
        contour_A, syltexts_A = getContour(meidoc_A) #print(contour_A)
        # Second file
        meidoc_B = minidom.parse("../GABCtoMEI/MEI_outfiles/MEI_intermedfiles/" + args.file2 + ".mei")
        contour_B, syltexts_B = getContour(meidoc_B) #print(contour_B)
        #### TO DO: Eventually substitute by "MEI_outfiles," this would mean to translate pitches to contour for square notation files

        # Calculate alignment
        alignment = needle.NeedlemanWunsch(contour_A, contour_B)
        alignment.gap_character = "_"
        # Print the results
        print(args.file1, "|", args.file2, "|", "SCORE: " + str(alignment.get_score()), "|", "IDENTITY % OF ALIGNMENT: " + str(alignment.get_identity()))
        print()
        print(alignment)

        difference = 0
        matches = 0
        alig1, alig2 = alignment.get_aligned_sequences()
        for i in range(0, len(alig1)):
            if (alig1[i] == alig2[i]):
                # match
                matches += 1
            else:
                # mismatch or indel
                difference += 1
        print("MATCHES: " + str(matches))
        print("DIFFERENCES: " + str(difference))
