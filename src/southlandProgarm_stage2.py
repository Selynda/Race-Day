
# List of post colors

postColors = []
postColors = ["Red", "Blue", "Silver", "Green", "Black", "Yellow", "Orange", "Ylk/Blk"]

# working variables

assembleLine = ""

# File being worked on

workFile = open("C:/Users/sgnol/Documents/projects/race_day/data/southland.txt, "r")

# Output file with final product

outFile = open('C:/Users/sgnol/Documents/projects/race_day/data/southland.txt', 'a+')
outFile.seek(0)
outFile.truncate()
