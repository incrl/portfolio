#!/usr/bin/env python

# I made a Christmas present for my family one year of the SpotIt. I replaced the game images
# with pictures of people in my family. Since I had a lot of family members (if you include nephews, nieces, and in-laws),
# I was wondering how many pictures I could have per card. I wrote this program to determine that.
# I also realized that you could only have a number that is one more than a prime number. Just an interesting fact.

import numpy as np

def test_matches(cards):
	current1 = []
	current2 = []
	for card1 in cards:
		for card2 in cards:
			if card1 == card2:
				continue
			count = 0
			for i in card1:
				for j in card2:
					if i == j:
						count = count + 1
			if count>1:
				print "Error: Multiple Matches", card1, card2
			if count<1:
				print "Error: No Match", card1, card2
		
		
def main(args):
    n = 6 # Number of Symbols of Card
    
    m = n - 1 # Intermediate Calculation
    
    num_cards = m**2 + m + 1
    
    cards = []
    
    first_card = np.arange(1,n+1,1) 
    cards.append(first_card.tolist())
    
    for i in range(1,m+1):
        offset = i*m
        temp = first_card + offset
        temp[0] = 1
        cards.append(temp.tolist())
    
    for i in range(0, num_cards-n):
        new_card = []
        
        new_card.append(i/m + 2)
		
        for j in range (0, m):
            new_card.append((i+(i/m)*j)%m + m*(j+1) + 2) 
		
        cards.append(new_card)
	
    for i in range(0,num_cards):
        print cards[i]
    
    print "Testing..."
    
    test_matches(cards)
    
    print "Done"
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
