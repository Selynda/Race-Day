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

# Open a text file to receive output and make sure it is empty

outFile = open('C:/Users/sgnol/Documents/projects/race_day/data/Southland_pdf.txt', 'a+')
outFile.seek(0)
outFile.truncate()

x = 0

while x <= pageCount-1:


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
# First loop to clean up empty lines at beginning of PDF file
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

        fileLine = fileLine.replace(" ","")
        
        if fileLine[:1] != "\n":            # test for not empty line to signal found data
            isEmptyLine = False
#====================================================================================

# Once you reach the first valid line of data start looking for a specfic
# pattern of "Track Record:" Once found look for "Red" and this will signify 
# the start of a post postion and begin # a new line
    
    z = 0
    postNumber = 0
    isLastPostPosition = False

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

# append to working line (assembleLine)

        assembleLine = assembleLine + fileLine

# Look for signals to slice and dice
# Signal 1: Track Record: Signals start of post positions
# Signal 2b: NO GREYHOUND IN THIS POST POSITION signals end of post position
# Signal 2a: Best Time: Signals end of post position
# Signal 3: SELECTIONS Signals end of race data

# Signal 1

        if assembleLine.find("Track Record:") >= 0:   

        # Look for post 1 color Red. If found slice line and write out
        # Then reset line and keep going

            if "Red " in assembleLine[assembleLine.find("Track Record:"):len(assembleLine)]:
                outFile.write(assembleLine[:assembleLine.find("Red ")] + "\n") 
                assembleLine = assembleLine[assembleLine.find("Red "):len(assembleLine)]


# Signal 2a

        if assembleLine.find("Best Time:") >= 0:

        # Increment post number

            postNumber += 1

        # See if next post color is on the same line. If it is, slice line and rebuild assembleLine with left over line.
        # CAUTION: Need to search for post color within 25 positions of Best Time just in case the color is used in the
        # dogs name

        # Each line writes the post position prior to it's occurance. For example: When Ylw/Blk is encountered that means
        # the end of the Orange post has been found and is written

            if "Blue " in assembleLine[assembleLine.find("Best Time:"):(assembleLine.find("Best Time:")+25)]:
                outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[:assembleLine.find("Blue")] + "\n")
                assembleLine = assembleLine[assembleLine.find("Blue"):len(assembleLine)] 

            elif "Silver " in assembleLine[assembleLine.find("Best Time:"):(assembleLine.find("Best Time:")+25)]:
                outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[:assembleLine.find("Silver ")] + "\n")
                assembleLine = assembleLine[assembleLine.find("Silver "):len(assembleLine)]    

            elif "Green " in assembleLine[assembleLine.find("Best Time:"):(assembleLine.find("Best Time:")+25)]:
                outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[:assembleLine.find("Green ")] + "\n")
                assembleLine = assembleLine[assembleLine.find("Green "):len(assembleLine)]

            elif "Black " in assembleLine[assembleLine.find("Best Time:"):(assembleLine.find("Best Time:")+25)]:
                outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[:assembleLine.find("Black ")] + "\n")
                assembleLine = assembleLine[assembleLine.find("Black "):len(assembleLine)]    

            elif "Yellow " in assembleLine[assembleLine.find("Best Time:"):(assembleLine.find("Best Time:")+25)]:
                outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[:assembleLine.find("Yellow ")] + "\n")
                assembleLine = assembleLine[assembleLine.find("Yellow"):len(assembleLine)]    

            elif "Orange " in assembleLine[assembleLine.find("Best Time:"):(assembleLine.find("Best Time:")+25)]:
                outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[:assembleLine.find("Orange ")] + "\n")
                assembleLine = assembleLine[assembleLine.find("Orange "):len(assembleLine)]    

            elif "Ylw/Blk " in assembleLine[assembleLine.find("Best Time:"):(assembleLine.find("Best Time:")+25)]:
                outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[:assembleLine.find("Ylw/Blk ")] + "\n")
                assembleLine = assembleLine[assembleLine.find("Ylw/Blk "):len(assembleLine)]  

            elif "Ylw/Blk" in assembleLine[0:7]:
                outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[0:(assembleLine.find("Best Time:")+25)] + "\n")
                isLastPostPosition = True
                assembleLine = ""
                isEndOfRace = True  

# Signal 2b

        elif assembleLine.find("NO GREYHOUND IN THIS POST POSITION") >= 0:
            postNumber += 1
            outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[0:assembleLine.find("NO GREYHOUND IN THIS POST POSITION ") + 34] + "\n")
            assembleLine = assembleLine[len("NO GREYHOUND IN THIS POST POSITION "): len(assembleLine)]

            if isLastPostPosition == True:
                assembleLine = ""
                isEndOfRace = True

# Signal 3

        # if isLastPostPosition == True and assembleLine.find("SELECTIONS "):
        #     outFile.write(str(raceNumber) + "\t" + str(postNumber) + "\t" + assembleLine[:assembleLine.find("SELECTIONS ")] + "\n")
        #     assembleLine = ""
        #     isEndOfRace = True             
        

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