# -*- coding: utf-8 -*-

import PyPDF2

# Initialize variables used to write new lines to output file

pageCount = 0
lineCount = 0
assembleLine = ""
postNumber = 0
raceNumber = 0

# Bring in the PDF file as a binary to be converted

inFile = open("C:/Users/sgnol/Downloads/sat eve 9-15-program.pdf", "rb")

# Convert the binary file into a readable file

pdfFile = PyPDF2.PdfFileReader(inFile)

# Open a text file to receive output and make sure it is empty

outFile = open('C:/Users/sgnol/Downloads/Southland2.txt', 'a+')
outFile.seek(0)
outFile.truncate()

# Open a work file to use when reading text

workFile = open('C:/Users/sgnol/Downloads/workfile.txt', 'w')


# Get the number of pages in the text file. 
# This will set race number and the limit for the outer loop count
# CAUTION: The pages start with 0 so race number will be page # + 1

#pageCount = pdfFile.numPages
x = 0
while x <= pageCount:
    
# Using the page number, bring in the first page. Write it to a working
# file so you can read line-by-line
    
    pdfPage = pdfFile.getPage(x)
    textFile = pdfPage.extractText()
    workFile.write(textFile)
    workFile.close()

# Re-open the work file and prepare to read line-by-line. The start of the 
# file is a bunch of empty lines. Iterate through them until you get to 
# first row of actual data
    
    workFile = open('C:/Users/sgnol/Downloads/workfile.txt', 'r')
    
# Calculate the race number and set default signal for empty line and EOF
    
    raceNumber = x + 1
    isEmptyLine = True
    isEndOfFile = False
    
    y = 0                                       
    
    assembleLine = ""
    
    while isEmptyLine == True:
        
        fileLine = workFile.readline()
        if fileLine == "":                      # Check for end of file
            isEndOfFile = True
            break
        
        y+= 1
        if y > 100:                             # safety measure to prevent never-ending loop
            break
        
        lineCount += 1
        
        assembleLine = fileLine.replace(" ","")
        
        if assembleLine[:1] != "\n":
            isEmptyLine = False
            
# Once you reach the first valid line of data start looking for a specfic
# pattern of Kennel:. This will signify the start of a post postion and begin
# a new line
    
    z = 0
    
    while isEndOfFile == False:
        
        fileLine = workFile.readline()
        
        if fileLine == "":
            isEndOfFile = True
            if assembleLine != "":          # write last line if it exists
                outFile.write(assembleLine)
            break
            
        lineCount += 1
                
        if fileLine.find("Kennel:") >= 0:   # Found first pattern in post
 
            postNumber += 1
                
# Write out anything that may already be in the assembleLine then clear it
# as start building the next line to write
            
            if assembleLine != "":          
                outFile.write(assembleLine + "\n")
                assembleLine = ""
                assembleLine = str(lineCount) + "\t" + str(raceNumber) + "\t" + str(postNumber) + "\t"
 
           
        assembleLine = assembleLine + fileLine.replace("\n","")


        z += 1
        if z >= 300:
            break
            
# Next page of pgm

    x += 1
    
# Done. Close all files and exit program
 
inFile.close()
outFile.close()
workFile.close()

