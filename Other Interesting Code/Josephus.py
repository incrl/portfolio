#!/usr/bin/env python

# This is code I wrote to solve the famous Josephus problem in mathematics.
# I wanted to verify that the mathematical prediction matches the actual result for large numbers.

import time

def main(args):
    n = 30 # Number of Men
    
    sleep_time = 0.5
    
    men = range(1,n+1)
    
    # Calculate Largest Power of 2
    a = 0
    for i in range(1, n+1):
		if (2**i > n):
			break
		a = i
    
    k = n - 2**a
    
    predict = 2*k + 1
	
    
    print "Starting Set:", men
    
    print "Prediction:", predict, "survives"
    
    time.sleep(1)
    
    print "Begin Killing..."
    
    time.sleep(0.5)
    
    for i in range(0,n-1):
		spot = 0
		killspot = spot+1
		print men[spot], "kills", men[killspot]
		del men[killspot]
		# Move the killer to the back of the line
		men.append(men[spot])
		del men[spot]
		time.sleep(sleep_time)
		
    
    
    print men[0], "survives!"
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
