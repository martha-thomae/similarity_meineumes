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


# ---------- #
# Document A #
# ---------- #
#meidoc_A = minidom.parse("MEI_outfiles/01_Aquit_82441_AQUIT.mei")
meidoc_A = minidom.parse("MEI_outfiles/MEI_intermedfiles/01_Aquit_82441.mei")
contour_A = getContour(meidoc_A)
# contour = [-2, -2, -1, -3, -2, 0, 1, 0, -2, -1, -1, -1, -3, -2, -3, 0, 0, 2, 3, 1, 0, 1, 0, -1, 1, 2, 1, 0, 1, 0, 0, 0, 0, 1, 2, 1, 0, 0, 1, 2, 3, 2, 2, 1, 1, 2, 3, 2, 0, 1, 0, -1, 0, 1, 0, 0, -2, -1, -2, -3, -2, -2, -3, -2, -1, -1, -1, -3, 0, 1, 0, -1, 0, 1, 0, -2, 0, -1, -1, -1, -2]

# pattern = [-2, -2, -1, -3]
# SequenceMatcher(None, pattern, contour_A).ratio()
# --> 0.09411764705882353 (bad, even though the pattern is there)

# ---------- #
# Document B #
# ---------- #
#meidoc_B = minidom.parse("MEI_outfiles/02_Square_85041_SQUARE.mei")
meidoc_B = minidom.parse("MEI_outfiles/MEI_intermedfiles/02_Square_85041.mei")
contour_B = getContour(meidoc_B)

Levenshtein.distance(contour_A, contour_B)

print(contour_A)
# [0, 0, 1, -2, 1, 2, 1, -1, -2, 1, 0, 0, -2, 1, -1, 3, 0, 2, 1, -2, -1, 1, -1, -1, 2, 1, -1, -1, 1, -1, 0, 0, 0, 1, 1, -1, -1, 0, 1, 1, 1, -1, 0, -1, 0, 1, 1, -1, -2, 1, -1, -1, 1, 1, -1, 0, -2, 1, -1, -1, 1, 0, -1, 1, 1, 0, 0, -2, 3, 1, -1, -1, 1, 1, -1, -2, 2, -1, 0, 0, -1]
print(contour_B)
# [1, 0, 1, -2, 1, 2, 1, -1, -2, 1, 0, -2, 1, -1, 3, 0, 2, 1, -2, -1, 1, -1, -1, 2, 1, -1, -1, 1, -1, 0, 0, 0, 2, 1, -2, -1, 1, 1, 1, -1, 0, -1, 0, 1, 1, -1, -2, 1, -1, -1, 1, 1, -1, -2, 1, -1, -1, 1, 0, -1, 1, 1, 0, -2, 3, 1, -1, -1, 1, 1, 0, -1, -2, 2, -1, 0, 0, -1]

for i in range(0, max(len(contour_A),len(contour_B))):
	print(contour_A[i], contour_B[i], contour_A[i] == contour_B[i])

for i in range(0, max(len(contour_A),len(contour_B))):
	if (i < len(contour_B)):
		print(contour_A[i], contour_B[i], Levenshtein.distance(contour_A[:i+1], contour_B[:i+1]))
	else:
		print(contour_A[i], None, Levenshtein.distance(contour_A[:i+1], contour_B[:i+1]))

# 0 0 0
# 0 0 0
# 1 1 0
# -2 -2 0
# 1 1 0
# 2 2 0
# 1 1 0
# -1 -1 0
# -2 -2 0
# 1 1 0
# 0 0 0
# 0 -2 1
# -2 1 2
# 1 -1 2
# -1 3 2
# 3 0 2
# 0 2 2
# 2 1 2
# 1 -2 2
# -2 -1 2
# -1 1 2
# 1 -1 2
# -1 -1 2
# -1 2 2
# 2 1 2
# 1 -1 2
# -1 -1 2
# -1 1 2
# 1 -1 2
# -1 0 2
# 0 0 2
# 0 0 2
# 0 2 2
# 1 1 2
# 1 -2 3
# -1 -1 3
# -1 1 4
# 0 1 5
# 1 1 5
# 1 -1 5
# 1 0 6
# -1 -1 6
# 0 0 6
# -1 1 6
# 0 1 6
# 1 -1 6
# 1 -2 6
# -1 1 6
# -2 -1 6
# 1 -1 6
# -1 1 6
# -1 1 6
# 1 -1 6
# 1 -2 6
# -1 1 6
# 0 -1 7
# -2 -1 8
# 1 1 8
# -1 0 8
# -1 -1 8
# 1 1 8
# 0 1 8
# -1 0 8
# 1 -2 8
# 1 3 8
# 0 1 8
# 0 -1 9
# -2 -1 10
# 3 1 10
# 1 1 10
# -1 0 10
# -1 -1 10
# 1 -2 10
# 1 2 10
# -1 -1 10
# -2 0 10
# 2 0 10
# -1 -1 10
# 0 None 9
# 0 None 8
# -1 None 7
