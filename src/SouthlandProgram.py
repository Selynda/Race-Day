# -*- coding: utf-8 -*-

import PyPDF2
#===============================================================================
# Initialization
#===============================================================================

# Variables used to write new lines to output file

pageCount = 0
lineCount = 0
assembleLine = ""
postNumber = 0
raceNumber = 0

# List of post colors

postColors = []
postColors = ["Red", "Blue", "Silver", "Green", "Black", "Yellow", "Orange", "Ylk/Blk"]

#===============================================================================
# Bring in PDF file and convert to readable text file
# Capture number of pages for use in looping controls
#===============================================================================

# Bring in the PDF file as a binary to be converted

inFile = open("C:/Users/sgnol/Documents/projects/race_day/data/sat eve 9-15-program.pdf", "rb")

# Convert the binary file into a readable file

pdfFile = PyPDF2.PdfFileReader(inFile)

# Get the number of pages in the text file. # This will set race number and the limit for the outer loop count
# CAUTION: PAGE COUNTS ARE ZERO-INDEXED

pageCount = pdfFile.numPages
print ("Page Count = " + str(pageCount))

# Open a text file to receive output and make sure it is empty

outFile = open('C:/Users/sgnol/Documents/projects/race_day/data/Southland.txt', 'a+')
outFile.seek(0)
outFile.truncate()

x = 0
while x <= pageCount-1:

    print ("page number = " + str(x))

# Using the page number, bring                    x the first page. Write it to a working
# file so it can be read line-b                   xline
    
    pdfPage = pdfFile.getPage(x)

    textFile = pdfPage.extractText()

    workFile = open('C:/Users/sgnol/Documents/projects/race_day/data/workfile.txt', 'w')
    workFile.seek(0)
    workFile.truncate()
    workFile.write(textFile)
    workFile.close()

# Re-open the work file and prepare to read line-by-line. 
# 
# The start of the file is a bunch of empty lines. Iterate through them until you get to 
# first row of actual data
    
    workFile = open('C:/Users/sgnol/Documents/projects/race_day/data/workfile.txt', 'r')
    
# Calculate the race number and set default signal for empty line and EOF
    
    raceNumber = x + 1
    isEmptyLine = True
    isEndOfFile = False
    
    y = 0                                       
    
    assembleLine = ""

#====================================================================================
# First loop to clean of empty lines at beginning of PDF file
#====================================================================================
    while isEmptyLine == True:
        
        fileLine = workFile.readline()
        if fileLine == "":                      # Check for end of file
            isEndOfFile = True
            break
        
        y+= 1
        if y > 500:                             # safety measure to prevent never-ending loop
            break
        
        lineCount += 1

# Although the lines appear as empty lines, they are actually filled
# with a bunch of blank spaces prior to the CRLF. Replace all of them 
# with a empty value so the line can be read as an empty line.

        assembleLine = fileLine.replace(" ","")
        
        if assembleLine[:1] != "\n":            # test for not empty line to signal found data
            isEmptyLine = False
#====================================================================================

# Once you reach the first valid line of data start looking for a specfic
# pattern of "Track Record:" Once found look for "Red" and this will signify 
# the start of a post postion and begin # a new line
    
    z = 0
    postNumber = 0
#====================================================================================
# Second loop to slice and dice the text line
#====================================================================================    
    while isEndOfFile == False:
        
        fileLine = workFile.readline()
        
        if fileLine == "":                      # test for EOF
            isEndOfFile = True
            if assembleLine != "":              # write last line if it exists
                outFile.write(assembleLine)
            break
            
        lineCount += 1                          # count lines read
        
# clean up special characters in the middle of the line

        fileLine = fileLine.replace("\n","")        # new line
        fileLine = fileLine.replace(chr(188),".25") # 1/4
        fileLine = fileLine.replace(chr(189),".5")  # 1/2
        fileLine = fileLine.replace(chr(190),".75") # 3/4

# Find the pattern that starts a race. This is usually "Track Record:". This will be 
# followed by the record (if it exists) which is then followed by the first post
# color of "Red". This signals the start of the first post position.
#   Example: Track Record: <dag's name>, 99.99 mm/dd/yyy Red

# The end of a post position is signaled by "Best Time:" or EOF if post position is empty
# at time of race.
#   Example: Best Time: 99.99 Blue or Best Time:  Blue

        if fileLine.find("Track Record:") >= 0:   # Found first pattern in race                
        # if fileLine.find("Kennel:") >= 0:   # Found first pattern in post

# Write out anything that may already be in the assembleLine then clear it
# and start building the next line to write
           
            assembleLine = ""

# Start slicing and dicing the lines until EOF is reached
# First step after finding Track Record is to find 1st post color of Red

# If post color found on same line, then slice the line and write out
# part with Track Record: as its own line. Keep remaining part of line
# that starts with Red. If post color is not on the same line then
# write the line with no slicing

           
            if fileLine.find("Red") >= 0:
                outFile.write(fileLine[0:fileLine.find("Red")]) + "\n"
                assembleLine = fileLine[fileLine.find("Red"):len(fileLine)]
            else:
                outFile.write(str(raceNumber) + "\t" + "0" + "\t" + fileLine + "\n")
                
            isEndOfRace = False

            while isEndOfRace == False:

                fileLine = workFile.readline()
                if fileLine == "":
                    if assembleLine != "":
                        outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                    
                    endofRace = True
                    break

                fileLine = fileLine.replace("\n","")        # new line
                fileLine = fileLine.replace(chr(188),".25") # 1/4
                fileLine = fileLine.replace(chr(189),".5")  # 1/2
                fileLine = fileLine.replace(chr(190),".75") # 3/4
              
# Look for Best Time: This signals the end of the data for all post position unless there
# is no entry for that post position.

#   Logic:
#   If next post color is on the same line then line has to be sliced and next post
#       position prepared for assembly
#   If not on the same line then
#       then read next line and post color will be there
#       If post is empty, slice for empty post position
#           If last post position, then break loop and start next race


#   If post color is found but post is empty, then slice that color and read next line

                if fileLine.find("Best Time:") >= 0:

                    postNumber += 1

                    if "Blue" in fileLine[fileLine.find("Best Time:"):(fileLine.find("Best Time:")+25)]:
                        assembleLine = assembleLine + fileLine[0:fileLine.find("Blue")]
                        outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                        assembleLine = fileLine[fileLine.find("Blue"):len(fileLine)] 

                    elif "Silver" in fileLine[fileLine.find("Best Time:"):(fileLine.find("Best Time:")+25)]:
                        assembleLine = assembleLine + fileLine[0:fileLine.find("Silver")]
                        outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                        assembleLine = fileLine[fileLine.find("Silver"):len(fileLine)]    

                    elif "Green" in fileLine[fileLine.find("Best Time:"):(fileLine.find("Best Time:")+25)]:
                        assembleLine = assembleLine + fileLine[0:fileLine.find("Green")]
                        outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                        assembleLine = fileLine[fileLine.find("Green"):len(fileLine)]    

                    elif "Black" in fileLine[fileLine.find("Best Time:"):(fileLine.find("Best Time:")+25)]:
                        assembleLine = assembleLine + fileLine[0:fileLine.find("Black")]
                        outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                        assembleLine = fileLine[fileLine.find("Black"):len(fileLine)]    

                    elif "Yellow" in fileLine[fileLine.find("Best Time:"):(fileLine.find("Best Time:")+25)]:
                        assembleLine = assembleLine + fileLine[0:fileLine.find("Yellow")]
                        outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                        assembleLine = fileLine[fileLine.find("Yellow"):len(fileLine)]    

                    elif "Orange" in fileLine[fileLine.find("Best Time:"):(fileLine.find("Best Time:")+25)]:
                        assembleLine = assembleLine + fileLine[0:fileLine.find("Orange")]
                        outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                        assembleLine = fileLine[fileLine.find("Orange"):len(fileLine)]    

                    elif "Ylw/Blk" in fileLine[fileLine.find("Best Time:"):(fileLine.find("Best Time:")+25)]:
                        assembleLine = assembleLine + fileLine[0:fileLine.find("Ylw/Blk")]
                        outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                        assembleLine = fileLine[fileLine.find("Ylw/Blk"):len(fileLine)]  

                        if assembleLine.find("SELECTIONS ") >= 0:
                            assembleLine = assembleLine[0:assembleLine.find("SELECTIONS ")]
                            postNumber += 1
                            outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                            assembleLine = ""
                            isEndOfRace = True  
  
                else:

                    if fileLine.find("SELECTIONS ") >= 0:
                        assembleLine = assembleLine + fileLine[0:fileLine.find("SELECTIONS ")]
                        outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine + "\n")
                        assembleLine = ""
                        isEndOfRace = True

                    else:

                        assembleLine = assembleLine + fileLine



        # assembleLine = str(lineCount) + "\t" + str(raceNumber) + "\t" + str(postNumber) + "\t"
       


        z += 1                                      # safety valve-loop count to prevent never-ending loop
        if z >= 300:
            break
            
# Next page of pgm

    x += 1
    assembleLine = ""


# Done. Close all files and exit program
 
inFile.close()
outFile.close()
workFile.close()