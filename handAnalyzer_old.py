#Hand analysis algorithms for determining which hands you can make and which hands your opponents might have.
import cards

class HandAnalyzer():
    def __init__(self):
        self.handProbs = [] #a list of probabilities for getting each hand rank
        for n in range(9): self.handProbs.append(0.0)
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
        oneCard = []
        for n in range(15): oneCard.append(0.0)
        twoCards = []
        for n in range(15): twoCards.append(0.0)
        threeCards = []
        for n in range(15): threeCards.append(0.0)
        fourCards = []
        for n in range(15): fourCards.append(0.0)
                
    def analyze(self, isMe, myCards, sharedCards, deck, opps):
        #start by finding the total numbers of known and unknown cards
        self.unknowns = 5 - len(sharedCards)
        self.knowns = sharedCards
        self.deck = deck
        self.opps = opps
        self.isMe = isMe
        
        if (isMe):
            self.knowns += myCards
        else:
            self.unknowns += 2 #start with one opponent, multiply at end for more than one
        
        #now determine the likelihood of different hands
        self.flush()
        self.straight()
        #self.matches()
        
    def analyzeHand(self, hand):
        #This is the analyze function to call when you have 5 KNOWN cards to send it (a poker hand)
        #It will figure out what your best hand is with these cards, and rank it
        self.hand = hand
        self.flush()
        self.straight()
        self.matches()
    
    def flush2(self):
        #This is a less efficient algorithm for finding a flush when given 5 known cards (a typical poker hand)
        suits = ["h","d","c","s"]
        flush = False
        rank = 0
        for s in suits:
            if flush == False:
                count = 0
                rank = 0
                for card in self.hand:
                    if card.suit == s: 
                        count += 1
                        if (card.value > rank): rank = card.value
                if count == 5: flush = True
    
    def flush(self):
        #This flush algorithm is for determining if you have a flush, given a 5 card hand.  In other words, you 
        #need to send this function 5 KNOWN cards (a hand)
        flush = False
        card = self.hand[0]
        s = card.suit
        if self.hand[1].suit == s and self.hand[2].suit == s and self.hand[3].suit == s and self.hand[4].suit == s: flush = True
        rank = 0
        for card in self.hand: 
            if card.value > rank: 
                rank = card.value
            
    def flush3(self):
        #This flush algorithm is for use when you have unknown cards. It calculates the PROBABILITY
        #of getting a flush.
        suits = ["h","d","c","s"]
        probs = {}
        for s in suits:
            count = 0
            for card in self.knowns:
                if card.suit == s: count += 1
            if (count + self.unknowns) < 5: probs[s] = 0.0 #no chance of flush
            elif count >= 5: probs[s] = 1.0 #already have a flush
            else:
                needed = 5 - count
                #find how many ways to get the needed cards from the ones still in the deck
                cardsLeft = 0
                if s == "h": cardsLeft = self.deck.heartsCount
                if s == "d": cardsLeft = self.deck.diamondsCount
                if s == "c": cardsLeft = self.deck.clubsCount
                if s == "s": cardsLeft = self.deck.spadesCount
                
                flushCombos = self.factorial(cardsLeft) / (self.factorial(cardsLeft - needed) * self.factorial(needed))
                extraCards = self.unknowns - needed     #extra tries to draw the cards
                deckLeft = self.deck.totalCount - needed     #how many cards left in the deck to choose from
                for n in range(extraCards):
                    flushCombos *= (deckLeft - n)
                totalCombos = self.factorial(self.deck.totalCount) / (self.factorial(self.deck.totalCount - self.unknowns) * self.factorial(self.unknowns))
                probs[s] = float(flushCombos) / float(totalCombos)              
        
        #Now add up the probabilities of getting a flush with each suit.  That's the total probability of getting a flush.
        totalProbs = 0.0
        for s in suits:
            totalProbs += probs[s]
        
        self.handProbs[5] = totalProbs
    
    def straight(self):
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
        if straight:
            rank = n+4
            print "straight: " + str(rank)
                
    def straight2(self):
        #create a list of card values we already have
        values = []
        for n in range(15): values.append(False)
        for card in self.knowns: values[card.value] = True
        combos = []     #combos of cards that would help you make a straight
        
        #look for all possible straights starting with 2-6 and ending with 10-A
        for n in range(2,11,1):
            count = 0            #cards in a row so far
            uk = self.unknowns   #unknown cards we have left for possibly filling in the missing parts of the straight
            i = n
            neededValues = []
            while (count < 5):
                print i
                if (values[i] == False): 
                    neededValues.append(i)
                    uk -= 1
                count += 1
                i += 1
            if (count >= 5 and uk >= 0): #got a possible straight
                combos.append(neededValues)
            print ""
        print combos
        #Now we need to eliminate duplicate entries for the same card combo
        noDupes = []
        for i in combos:
            if i not in noDupes:
                noDupes.append(i)
        print noDupes
        #***NOTE*** If you have a combo in your list with 0 entries that means you already have a straight
        #in your known cards!  So your odds are 100%.  Check for this!!!****
        
    def matches(self):
        #find all matches
        pair = []
        for n in range(15): pair.append(False)
        threeOAK = []
        for n in range(15): threeOAK.append(False)
        fourOAK = []
        for n in range(15): fourOAK.append(False)
        
        for n in range(5): #for each card in the hand
            v = self.hand[n].value
            count = 1
            for x in range(5): #check the other cards
                if x != n:
                    if self.hand[n].value == v: count += 1
            if count == 2: pair[v] = True
            if count == 3: threeOAK[v] = True
            if count == 4: fourOAK[v] = True
            print count
            
                     
    
    def factorial(self, value):
        total = value
        for n in range(value - 1, 1, -1):
            total *= n
        return total
    
    def combos(self, list, r):
        n = len(list)
        limit = []
        y = n - (r-1)
        for x in range(r):
            limit.append(n-y)
            y -= 1

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
        