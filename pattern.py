# printing pattern 
# ****
# ***
# **
# *

for row in range(4, 0, -1):    #start,stop and step
    for col in range(row):     #how many stars to print in each row 
        print("*", end="")     #print star in the same line
    print()