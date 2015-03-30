#test.py was originally just written to test the handAnalyzer and handPlayer modules, but is now the main program

import cards
import handAnalyzer
import handPlayer
import time
import sys
import os, os.path

import psyco
psyco.full()

handAnalyzer = handAnalyzer.HandAnalyzer()
handPlayer = handPlayer.HandPlayer()

myCards = []
sharedCards = []
deck = cards.Deck()
players = 8
opps = 8
bet = 0.0
pot = 0.0
prob = 0.0
EV = 0.0
roundsPlayed = 0

def printTable():
    print ""
    line = "hole cards: "
    for card in myCards:
        line += str(card.value) + card.suit + " "
    print line
    print ""
    
    line = "shared cards: "
    for card in sharedCards:
        line += str(card.value) + card.suit + " "
    print line
    print ""
    
    line = "players: " + str(players)
    line += ", opps: " + str(opps)
    line += ", IP: " + str(1.0 / float(opps + 1))
    line += ", TP: " + str((1.0 / float(opps + 1) * 1.51)) + " to "
    line += str((1.0 / float(opps + 1) * 1.57))
    print line
    print ""
    
    line = "bet: " + str(bet)
    line += ", pot: " + str(pot)
    if (bet > 0): line += ", pot/bet: " + str(pot/bet)
    print line
    print ""
    
    line = "prob: " + str(prob)
    EV = (prob * pot) - bet
    line += ", EV: " + str(EV)
    line += ", " + str(roundsPlayed * 1000) + " hands"
    print line
    print ""
    
def playHands():
    prob = handPlayer.play(myCards, sharedCards, deck.asList(), opps)
    roundsPlayed = 1
    
go = True
while (go):
    printTable()
    print "o) number of opponents in hand still"
    print "n) number of opponents at table (for quicker table reset)"
    print "h) hole cards"
    print "s) add shared cards"
    print "b) bet size (how much I have to bet(call) to stay in the hand)"
    print "p) pot size (how much I stand to win if I win)"
    print "r) run the odds!"
    print "m) run more odds!"
    print "c) clear the hand for the next round"
    print "q) quit"
    input = raw_input("[Menu]>")
    
    if (input == "q"): go = False
    if (input == "c"):
        myCards = []
        sharedCards = []
        opps = players
        deck = cards.Deck()
        bet = 0.0
        pot = 0.0
        prob = 0.0
        EV = 0.0
        roundsPlayed = 0
    if (input == "o"): opps = int(raw_input("# of opponents still in hand: "))
    if (input == "n"): 
        players = int(raw_input("# of opponents at table: "))
        if (opps > players): opps = players
    if (input == "h"):
        print "Hole cards:"
        myCards = []
        myCards.append(deck.getCard())
        myCards.append(deck.getCard())
        
        #now check for the hole cards in the database
        valueA = myCards[0].value
        valueB = myCards[1].value
        suitA = myCards[0].suit
        suitB = myCards[1].suit
        dir1 = "holecards/" + str(valueA) + suitA + str(valueB) + suitB + "/"
        dir2 = "holecards/" + str(valueB) + suitB + str(valueA) + suitA + "/"
        file = "opps" + str(opps) + ".txt"
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
        if total > 0:
            roundsPlayed = total / 1000
            prob = float(wins) / float(total)
        else:        
            prob = handPlayer.play(myCards, sharedCards, deck.asList(), opps)
            roundsPlayed = 1
        
    if (input == "s"):
        if (len(sharedCards) == 0):
            sharedCards.append(deck.getCard())
            sharedCards.append(deck.getCard())
            sharedCards.append(deck.getCard())
        else:
            sharedCards.append(deck.getCard())
        prob = handPlayer.play(myCards, sharedCards, deck.asList(), opps)
        roundsPlayed = 1
    if (input == "b"): bet = float(raw_input("Bet to stay in: "))
    if (input == "p"): pot = float(raw_input("Pot to win: "))
    if (input == "r"):
        if (len(sharedCards) < 4):
            prob = handPlayer.play(myCards, sharedCards, deck.asList(), opps)
        else:
            prob = handPlayer.play(myCards, sharedCards, deck.asList(), opps)
            #prob = handAnalyzer.runOdds(myCards, sharedCards, deck.asList(), opps)
        roundsPlayed = 1
    if (input == "m"):
        probs = prob * roundsPlayed
        newProb = handPlayer.play(myCards, sharedCards, deck.asList(), opps)
        roundsPlayed += 1
        probs += newProb
        prob = probs / roundsPlayed
        
        