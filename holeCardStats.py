#this program runs stats on hole card combos.  For example if you want to figure out the top 15% of starting hands so you
#can only put money in 15% of the pots you see.
import cards
import os, os.path
import handAnalyzer

class Hand():
    def __init__(self):
        pass
    
numOpps = int(raw_input("Number of opponents: "))
hands = []
hA = handAnalyzer.HandAnalyzer()
deck = cards.Deck()
holeCards = hA.combos(deck.asList(), 2)

#get the probs from the directories
for cards in holeCards:
    #get a new deck and select two hole cards (a new permutation)
    cardA = cards[0]
    cardB = cards[1]
    valueA = cardA.value
    suitA = cardA.suit
    valueB = cardB.value
    suitB = cardB.suit
    
    #setup the file reading stuff
    dir1 = "holecards/" + str(valueA) + suitA + str(valueB) + suitB + "/"
    dir2 = "holecards/" + str(valueB) + suitB + str(valueA) + suitA + "/"
    file = "opps" + str(numOpps) + ".txt"
    
    #try to read the files(one for each permutation of the hand) and total the wins and losses
    wins = 0
    losses = 0
    
    if (os.path.isfile(dir1 + file)):
        f = open(dir1 + file, 'r')
        lines = f.readlines()
        wins += int(lines[0])
        losses += int(lines[1])
        f.close()
        
    if (os.path.isfile(dir2 + file)):
        f = open(dir2 + file, 'r')
        lines = f.readlines()
        wins += int(lines[0])
        losses += int(lines[1])
        f.close()
        
    total = wins + losses
    hand = Hand()
    hand.cards = cards
    hand.wins = wins
    hand.losses = losses
    hand.total = total
    hand.prob = float(wins)/float(total)
    hands.append(hand)
        
#now sort the hands
for n in range(len(hands)):
    hi = n
    for i in range(n+1, len(hands)):
        if hands[i].prob > hands[hi].prob: hi = i
    if (hi != n):
        #swap hands[n] with hands[hi]
        swap = hands[n]
        hands[n] = hands[hi]
        hands[hi] = swap
    
print ""
print "hole card combo's = " + str(len(hands)) #make sure you have 1326 and nothing got fucked up above..

percentHands = float(raw_input("What percentage of hands do you want to play(as decimal, i.e. 0.15)?"))
numHands = int(round(percentHands * len(hands)))
print "numHands = " + str(numHands)

for n in range(numHands):
    hand = hands[n]
    line = str(hand.prob)
    line += " " + str(hand.cards[0].value) + hand.cards[0].suit
    line += " " + str(hand.cards[1].value) + hand.cards[1].suit
    print line
    
#now find the worst prob you can play
minProb = hands[numHands - 1].prob
print ""
print "The minimum probability you should play is about " + str(minProb)
print ""


    
