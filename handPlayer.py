#This program plays random games with each possible set of hole cards, with every number of opponents from 1 to 9
#It stores the results so that the probability of winning with any given hole cards can be known pre-flop.
import random

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
        
class HandPlayer():
    def __init__(self):
        self.hA = handAnalyzer.HandAnalyzer()
        self.handsPlayed = 0
        
    def getCard(self, cards):
        num = len(cards)
        rand = random.randint(0,num-1)
        return cards.pop(rand)
    
    def play(self, holeCards, shared, deck, numOpps):
        #print "Playing hands..."
        #print ""
        
        numHands = 1000
        
        wins = 0
        losses = 0
        
        for h in range(numHands):
            #if (h % 1000) == 0: print h
            
            #reset the deck for a new game
            cardList = deck[:]
            
            #setup me and get my hole cards
            me = Player()
            me.holeCards = holeCards
            
            #setup opponents            
            opps = []
            for n in range(numOpps):
                opp = Player()
                opp.holeCards.append(self.getCard(cardList))
                opp.holeCards.append(self.getCard(cardList))
                opps.append(opp)
                
            #setup shared cards
            sharedCards = shared[:]
            neededSC = 5 - len(sharedCards)
            for n in range(neededSC):
                sharedCards.append(self.getCard(cardList))

            #get my hand rank
            myCards = me.holeCards + sharedCards #7 cards
            me.rank = self.hA.getBestHand(myCards)

            #get opponents' hand ranks
            for opp in opps:
                oppCards = opp.holeCards + sharedCards
                opp.rank = self.hA.getBestHand(oppCards)

            #compare hands
            win = True
            for opp in opps:
                if opp.rank > me.rank: win = False
            if win: wins += 1
            else: losses += 1
        
        #print "wins = " + str(wins)
        #print "losses = " + str(losses)
        winProb = (float(wins)/float(wins + losses))
        #print winProb
        return winProb