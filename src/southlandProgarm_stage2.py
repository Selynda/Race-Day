
# List of post colors

postColors = []
postColors = ["Red", "Blue", "Silver", "Green", "Black", "Yellow", "Orange", "Ylk/Blk"]

# Race date patterns to look for

raceDate = []
raceDate = ["01/","02/","03/","04/","05/","06/","07/","08/","09/","10/","11/","12/"]

# File being worked on

inFile = open("C:/Users/sgnol/Documents/projects/race_day/data/southland_pdf.txt", "r")

# Output file with final product

outFile = open("C:/Users/sgnol/Documents/projects/race_day/data/southland.txt", 'a+')
outFile.seek(0)
outFile.truncate()

# working variables

assembleLine = ""
isEndOfFile = False
color = ""


while isEndOfFile == False:

    fileLine = inFile.readline()

    if fileLine[0:15] in postColors:
        print (fileLine[0:15])
        isEndOfFile = True
