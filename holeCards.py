#This program plays random games with each possible set of hole cards, with every number of opponents from 1 to 9
#It stores the results so that the probability of winning with any given hole cards can be known pre-flop.
import random
import os, os.path
import sys
import cards
import handAnalyzer
import time

import psyco
psyco.full()

class Player():
    def __init__(self):
        self.holeCards = []
        self.rank = 0
        self.bestHand = []

def getCard(cards):
    num = len(cards)
    rand = random.randint(0,num-1)
    return cards.pop(rand)

hA = handAnalyzer.HandAnalyzer()

print "Hole Card Simulator v0.1"
print ""
numHands = int(raw_input("How many hands per hole card permutation? "))
numOpps = int(raw_input("Number of opponents: "))

for a in range(52):
    for b in range(51):
        wins = 0
        losses = 0
        deck = cards.Deck()
        cardList = deck.asList()
        cardA = cardList.pop(a)
        cardB = cardList.pop(b)
        valueA = cardA.value
        suitA = cardA.suit
        valueB = cardB.value
        suitB = cardB.suit
        print str(valueA) + suitA + " " + str(valueB) + suitB
        dir = "holecards/" + str(valueA) + suitA + str(valueB) + suitB + "/"
        file = "opps" + str(numOpps) + ".txt"
        start = time.time()
        for h in range(numHands):
            if (h % 1000) == 0: print h
            #get a new deck
            deck = cards.Deck()
            cardList = deck.asList()
            
            #setup me and get my hole cards
            me = Player()
            me.holeCards.append(cardList.pop(a))
            me.holeCards.append(cardList.pop(b))
            
            #setup opponents            
            opps = []
            for n in range(numOpps):
                opp = Player()
                opp.holeCards.append(getCard(cardList))
                opp.holeCards.append(getCard(cardList))
                opps.append(opp)
                
            #setup shared cards
            sharedCards = []
            for n in range(5):
                sharedCards.append(getCard(cardList))

            #get my hand rank
            myCards = me.holeCards + sharedCards #7 cards
            me.rank = hA.getBestHand(myCards)
            '''
            print "my rank = " + me.rank.name + " " + str(me.rank.rankTotal)
            for card in me.rank.hand:
                    print str(card.value) + card.suit
            print ""
            '''
            #get opponents' hand ranks
            for opp in opps:
                oppCards = opp.holeCards + sharedCards
                opp.rank = hA.getBestHand(oppCards)
                '''
                print "opp rank = " + opp.rank.name + " " + str(opp.rank.rankTotal)
                for card in opp.rank.hand:
                    print str(card.value) + card.suit
                print ""
                '''
            #compare hands
            win = True
            #print "me " + str(me.rank.rankTotal)
            for opp in opps:
                #print "opp" + str(opp.rank.rankTotal)
                if opp.rank > me.rank: win = False
                
            if win: wins += 1
            else: losses += 1
        end = time.time()
        print "Total time = " + str(end - start)
        
        print ""
        print "Results for " + str(valueA) + suitA + " " + str(valueB) + suitB 
        print "wins = " + str(wins)
        print "losses = " + str(losses)
        print str(float(wins)/float(wins + losses) * 100) + "%"
        print ""
        
        #check to see if the directory for this hole card permutation exists yet
        if not os.path.exists(dir):
            os.makedirs(dir)

        #Now try to open an existing log file and get the stats
        oldWins = 0
        oldLosses = 0
        
        if (os.path.isfile(dir + file)):
            f = open(dir + file, 'r')
            lines = f.readlines()
            oldWins = int(lines[0])
            oldLosses = int(lines[1])
            f.close()
            
        #update the total wins and losses
        wins += oldWins
        losses += oldLosses
        lines = []
        lines.append(str(wins) + "\n")
        lines.append(str(losses) + "\n")
        
        #Now write the new stats
        f = open(dir + file, 'w')
        f.writelines(lines)