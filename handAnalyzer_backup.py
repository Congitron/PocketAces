#Hand analysis algorithms for determining which hands you can make and which hands your opponents might have.
import cards
import time
import psyco
psyco.full()

class Rank():
    def __init__(self):
        self.rankP = 0  #Primary Rank (High Card = 0, 1 Pair = 1, 2 Pair = 2...Straight Flush = 8
        self.rankS = 0  #Secondary Rank (To differentiate hands of same rankP.  Highest card, value of pair, etc..)
        self.rankT = 0  #Tertiary Rank (One more level of differentiation for more accuracy)
        self.rankTotal = 0  #The overall rank score of this hand (based on rankP, rankS, and rankT)
        self.name = ""  #the name of this hand, i.e. "Full House", "High Cards"...
        self.hand = []  #the cards in this hand
        self.prob = 0.0 #probability of winning vs the opponent's rank list
    
class HandAnalyzer():
    def __init__(self):
        #Hand ranks by array index
        #0 high card
        #1 1 pair
        #2 2 pair
        #3 3 of a kind
        #4 straight
        #5 flush
        #6 full house
        #7 4 of a kind
        #8 straight flush
        
        self.myHands = []       #seven card combos(to send to getBestHand)
        self.myRanks = []       #analyzed hands(ranks) reduced to 5 cards each(best hand)
        self.oppHands = []      #same for opps
        self.oppRanks = []
        
    def analyzeHand(self, hand):
        #This is the analyze function to call when you have 5 KNOWN cards to send it (a poker hand)
        #It will figure out what your best hand is with these cards, and rank it
        self.hand = hand
        
        self.tempHands = []     #store the best hand from each algorithm and then send the best overall to the master list
        self.tempRanks = []
        
        topRank = Rank()        #the best hand
        
        #find the possible hands
        flushRank = self.flush()
        straightRank = self.straight()
        matchRank = self.matches()
        
        if flushRank.rankTotal > topRank.rankTotal: topRank = flushRank
        if straightRank.rankTotal > topRank.rankTotal: topRank = straightRank
        if matchRank.rankTotal > topRank.rankTotal: topRank = matchRank
        
        #now look for a straight flush
        if flushRank.rankP > 0 and straightRank.rankP > 0:
            topRank = Rank()
            rankP = 8
            rankS = flushRank.rankS
            rankT = flushRank.rankT
            rankName = "Straight Flush"
            rankTotal = rankP * 196
            rankTotal += rankS * 14
            rankTotal += rankT
            topRank.rankP = rankP
            topRank.rankS = rankS
            topRank.rankT = rankT
            topRank.name = rankName
            topRank.rankTotal = rankTotal
        
        #if rankP is 0 then it's just a high card, so get its rankS and rankT
        if topRank.rankP == 0: topRank = self.highCard()
        
        return topRank
    
    def flush(self):
        #This flush algorithm is for determining if you have a flush, given a 5 card hand.  In other words, you 
        #need to send this function 5 KNOWN cards (a hand)
        flush = False
        card = self.hand[0]
        s = card.suit
        if self.hand[1].suit == s and self.hand[2].suit == s and self.hand[3].suit == s and self.hand[4].suit == s: flush = True
        
        rank = Rank()   #create a new rank object
        
        if flush: 
            rankP = 5   #primary rank
            rankS = 0   #secondary rank
            for card in self.hand:
                if card.value > rankS: 
                    rankS = card.value
            rankT = 0   #tertiary rank
            for card in self.hand:
                if card.value > rankT and card.value != rankS:
                    rankT = card.value
            rank.rankP = rankP
            rank.rankS = rankS
            rank.rankT = rankT
            rankTotal = rankP * 196
            rankTotal += rankS * 14
            rankTotal += rankT
            rank.rankTotal = rankTotal
            rank.name = "Flush"
        
        return rank
    
    def straight(self):
        #find a straight
        values = []
        for n in range(15): values.append(False)
        for card in self.hand: values[card.value] = True
        straight = False
        n = 2
        go = True
        while (n < 11 and go):
            if values[n]:
                if (values[n+1] and values[n+2] and values[n+3] and values[n+4]): straight = True
                go = False
            n += 1
        rank = Rank()   #create a new rank object
        
        if straight:
            rankP = 4   #primary rank
            rankS = 0   #secondary rank
            for card in self.hand:
                if card.value > rankS: 
                    rankS = card.value
            rankT = 0   #tertiary rank
            for card in self.hand:
                if card.value > rankT and card.value != rankS:
                    rankT = card.value
            rank.rankP = rankP
            rank.rankS = rankS
            rank.rankT = rankT
            rankTotal = rankP * 196
            rankTotal += rankS * 14
            rankTotal += rankT
            rank.rankTotal = rankTotal
            rank.name = "Straight"
            
        return rank
    
    def matches(self):
        #find all matches
        pair = []
        for n in range(15): pair.append(False)
        threeOAK = []
        for n in range(15): threeOAK.append(False)
        fourOAK = []
        for n in range(15): fourOAK.append(False)
        checked = []
        for n in range(15): checked.append(False)
        
        for n in range(5): #for each card in the hand
            v = self.hand[n].value
            if checked[v] == False:
                count = 1
                for x in range(5): #check the other cards
                    if x != n:
                        if self.hand[x].value == v: count += 1
                if count == 2: pair[v] = True
                if count == 3: threeOAK[v] = True
                if count == 4: fourOAK[v] = True                    
                checked[v] = True
        
        #now that you have the matches recorded, just count them
        #if you have 2 pairs, then your hand is two pair, etc..
        twoCount = 0
        threeCount = 0
        fourCount = 0
        for n in pair: 
            if n == True: twoCount += 1
        for n in threeOAK: 
            if n == True: threeCount += 1
        for n in fourOAK: 
            if n == True: fourCount += 1
        
        #now look for the best hand it can make
        rankP = 0
        rankS = 0
        rankT = 0
        rankTotal = 0
        rankName = ""
        if twoCount == 1: 
            rankP = 1      #one pair
            rankS = 0
            for n in range(2,15):
                if pair[n] == True: rankS = n #the secondary is the value of the paired cards
            rankT = 0
            for card in self.hand:
                if card.value > rankT and card.value != rankS:
                    rankT = card.value #rankT is the highest non-paired card (the kicker)
            rankName = "1 Pair"
        if twoCount == 2: 
            rankP = 2      #two pair
            rankS = 0
            for n in range(2,15):
                if pair[n] == True and n > rankS: rankS = n #get the highest pair
            rankT = 0
            for n in range(2,15):
                if pair[n] == True and n != rankS: rankT = n #the lower pair is rankT
            rankName = "2 Pair"
        if threeCount == 1: 
            rankP = 3    #3oak
            rankS = 0
            for n in range(2,15):
                if threeOAK[n] == True: rankS = n #rankS is the value that got 3oak
            rankT = 0
            for card in self.hand:
                if card.value > rankT and card.value != rankS:
                    rankT = card.value #rankT is the high card that's not in the 3oak
            rankName = "3 OAK"
        if threeCount == 1 and twoCount == 1: 
            rankP = 6  #full house
            rankS = 0
            for n in range(2,15):
                if threeOAK[n] == True: rankS = n #the 3oak is the rankS
            rankT = 0
            for n in range(2,15):
                if pair[n] == True: rankT = n #the pair is the rankT
            rankName = "Full House"
        if fourCount == 1: 
            rankP = 7     #4oak
            rankS = 0
            for n in range(2,15):
                if fourOAK[n] == True: rankS = n #rankS is the 4oak value
            rankT = 0
            for card in self.hand:
                if card.value != n:
                    rankT = card.value #there's only 5 cards, so the only card left is rankT
            rankName = "4 OAK"
        
        #calculate rankTotal
        rankTotal = rankP * 196
        rankTotal += rankS * 14
        rankTotal += rankT
        
        #create a new rank object
        rank = Rank()   
        rank.rankP = rankP
        rank.rankS = rankS
        rank.rankT = rankT
        rank.rankTotal = rankTotal
        rank.name = rankName
        
        return rank
        
        
    def highCard(self):
        rank = Rank()
        rankS = 0
        for card in self.hand:
            if card.value > rankS: rankS = card.value
        rankT = 0
        for card in self.hand:
            if card.value > rankT and card.value != rankS:
                rankT = card.value
    
        #calculate rankTotal
        rankTotal = rankS * 14
        rankTotal += rankT
        rank.rankTotal = rankTotal
        rank.rankS = rankS
        rank.rankT = rankT
        rank.name = "High Card"
        
        return rank
    
    def factorial(self, value):
        total = value
        for n in range(value - 1, 1, -1):
            total *= n
        return total
    
    def combos(self, list, r):
        n = len(list)
        limit = []
        for x in range(r):
            l = (n - r) + x
            limit.append(l)
            
        #now find the combos
        combos = []
        comboIndices = []
        comboItems = []
        for x in range(r): comboIndices.append(x) #get list of indices for combo
        for x in range(r): comboItems.append(list[x]) #get list of items for combo
        go = True
        while (go):
            for x in range(r):
                comboItems[x] = list[comboIndices[x]] #make the new combo
            newList = comboItems[:]
            combos.append(newList) #add the last combo created
            
            #now iterate
            c = r - 1
            i = False
            while (c > -1 and comboIndices[c] == limit[c]): c -= 1
            if (c < 0): go = False
            if (go):
                comboIndices[c] += 1
                if c < (r-1):
                    for x in range(c + 1, r):
                        z = x - c #how many columns up from c
                        comboIndices[x] = comboIndices[c] + z
                    
        return combos
        
    def getBestHand(self, cards):
        #cards is expected to be a list of 7 cards
        hands = self.combos(cards, 5)     #get a list of all possible 5 card hands
        topRank = Rank()
        bestHand = []
        for hand in hands:
            rank = self.analyzeHand(hand)
            if rank.rankTotal > topRank.rankTotal: 
                topRank = rank
                topRank.hand = hand[:]
            
        #topRank.hand = bestHand #return the hand too, so you know which of the 21 hands was best
            
        return topRank
            
    def runOdds(self, myCards, sharedCards, deck, opps):
        #myCards = my hole cards; sharedCards = shared cards on table; deck = deck.asList(); opps = number of opponents in hand
        
        print "getting my 7 card combos"
        #first, get my list of 7 card combos
        unknowns = 5 - len(sharedCards)
        combos = self.combos(deck, unknowns)
        self.myHands = []
        for combo in combos:
            cards = myCards + sharedCards + combo
            self.myHands.append(cards)
        
        print "getting my ranks"
        #now rank my hands
        self.myRanks = []
        for hand in self.myHands:
            self.myRanks.append(self.getBestHand(hand))
            
        print "getting opp combos"
        #get opponents' 7 card combos
        unknowns = 7 - len(sharedCards)
        combos = self.combos(deck, unknowns)
        self.oppHands = []
        for combo in combos:
            cards = sharedCards + combo
            self.oppHands.append(cards)
            
        print "getting opp ranks"
        #now rank opp hands
        self.oppRanks = []
        start = time.time()
        for hand in self.oppHands:
            self.oppRanks.append(self.getBestHand(hand))
        end = time.time()
        print str(end - start)
        
        #Now, for every rank of mine(self.myRanks), find its odds of winning by comparing it to every
        #rank the opponent has.  Then add up all my odds(each multiplied by it's chance of happening).
        #That's my total chance to win the hand(the sum of 
        #the chance of each hand happening * its chance to beat the opponent).
        print "calculating rank odds"
        for myRank in self.myRanks:
            wins = 0
            losses = 0
            for oppRank in self.oppRanks:
                if myRank.rankTotal > oppRank.rankTotal: wins += 1
                if myRank.rankTotal < oppRank.rankTotal: losses += 1
            
            #now wer're going to look for the odds of all opponents losing
            #that's the odds of our hand winning
            probList = []
            numCards = len(deck)
            for n in range(opps):
                prob = float(wins)/float(wins + losses) #prob of me winning is prob of them losing
                probList.append(prob)
                
                #now we have to update the odds for the next opponent
                wins -= 1
                combosToRemove = (numCards - 1) + (numCards - 2)
                combosToRemove -= 1 #for the one win we already got rid of
                numCards -= 2 #for the two cards removed by this opponent
                winsToRemove = (float(wins)/float(wins + losses)) * combosToRemove
                lossesToRemove = (float(losses)/float(wins + losses)) * combosToRemove
                wins -= winsToRemove
                losses -= lossesToRemove
                if (winsToRemove + lossesToRemove) != combosToRemove: 
                    print "Combo removal not equal.  Wins: " + str(winsToRemove) + " Losses: " + str(lossesToRemove) + " Combos: " + str(combosToRemove)
            
            totalProb = probList[0]
            if len(probList) > 1:
                for n in range(1,len(probList)):
                    totalProb *= probList[n]
            
            myRank.prob = totalProb
            
        #Now add up all your probabilities
        totalProb = 0.0
        chance = 1.0 / float(len(self.myRanks))
        for myRank in self.myRanks:
            totalProb += chance * myRank.prob
                            
        return totalProb