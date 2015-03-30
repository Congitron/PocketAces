hands = [1,20,2,4,5,18,11]

print str(hands)

#now sort the hands
for n in range(len(hands)):
    hi = n
    for i in range(n+1, len(hands)):
        if hands[i] > hands[hi]: hi = i
    if (hi != n):
        #swap hands[n] with hands[hi]
        swap = hands[n]
        hands[n] = hands[hi]
        hands[hi] = swap
    
print str(hands)