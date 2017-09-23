
# In my artificial intelligence class, we had an interesting discussion about the Monty Hall problem.
# During that discussion, I became curious about if Monty Hall's odds change as the probability of a person
# switching doors changes. I wrote this program to do some analysis.

#Probabilty that the person will switch
switch = 1

print "Likelihood of Switch =", "{0:.0f}%".format(switch * 100)

print "#############Random Monty Hall###############"

prob = 1.0/3.0

monty = switch * prob + (1-switch) * (1 - prob)
print "Monty wins", "{0:.0f}%".format(monty * 100), "of the time."


print "#############Forced Monty Hall###############"

print "If person picks spot before car:"
monty = (1 - switch)
print "Monty wins", "{0:.0f}%".format(monty * 100), "of the time."

print "If person picks spot of car:"
monty = switch
print "Monty wins", "{0:.0f}%".format(monty * 100), "of the time."

print "If person picks spot after car:"
monty = (1 - switch)
print "Monty wins", "{0:.0f}%".format(monty * 100), "of the time."

print
split = ((1 - switch) + switch)/2.0
print "Second turn split = ", "{0:.0f}%".format(split* 100)

print
monty1 = prob * (1-switch)
print "Monty wins by first turn scenario", "{0:.0f}%".format(monty1 * 100), "of the time."
monty2 = prob*switch + prob *(1-switch)
print "Monty wins by second turn scenario", "{0:.0f}%".format(monty2 * 100), "of the time."

print
total = monty1 + monty2
print "Monty wins", "{0:.0f}%".format(total * 100), "overall."









