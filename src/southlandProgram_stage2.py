
# List of post colors

# postColors = []
# postColors = ["Red", "Blue", "Silver", "Green", "Black", "Yellow", "Orange", "Ylk/Blk"]


postColors = {}
postColors = {"Red", "Blue", "Silver", "Green", "Black", "Yellow", "Orange", "Ylk/Blk"}

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

linePrefix = ""
assembleLine = ""
isEndOfFile = False
color = ""
x = 0


while isEndOfFile == False:

    fileLine = inFile.readline()
    if fileLine == "":
        isEndOfFile = True
        break

    linePrefix = ""

    searchLine = fileLine[0:15]

    color = postColors.intersection(set(searchLine))
    print (searchLine + " " + str(postColors.intersection(set(searchLine))))

   
    # if searchLine.find("Red") >= 0:
    #     linePrefix = fileLine[0:(fileLine.find("Red")+3)] + "\t"

    # if searchLine.find("Blue") >= 0:
    #     linePrefix = fileLine[0:(fileLine.find("Blue")+4)] + "\t"

    # if searchLine.find("Silver") >= 0:
    #     linePrefix = fileLine[0:(fileLine.find("Silver")+6)] + "\t"

    # if searchLine.find("Green") >= 0:
    #     linePrefix = fileLine[0:(fileLine.find("Green")+5)] + "\t"

    # if searchLine.find("Black") >= 0:
    #     linePrefix = fileLine[0:(fileLine.find("Black")+5)] + "\t"

    # if searchLine.find("Yellow") >= 0:
    #     linePrefix = fileLine[0:(fileLine.find("Yellow")+6)] + "\t"
    
    # if searchLine.find("Orange") >= 0:
    #     linePrefix = fileLine[0:(fileLine.find("Orange")+6)] + "\t"
    
    # if searchLine.find("Ylw/Blk") >= 0:
    #     linePrefix = fileLine[0:(fileLine.find("Ylw/Blk")+7)] + "\t"       

# Search for date pattern

    





    # x += 1
    # if x >= 8:
    #     isEndOfFile = True
    #     break