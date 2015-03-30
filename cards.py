#the deck and cards
import psyco
psyco.full()

class Card():
    #a card
    def __init__(self):
        pass        
    
class Deck():        
    def __init__(self):
        self.suits = ["h","d","c","s"]
        self.hearts = []
        for n in range(15): self.hearts.append(True)
        self.diamonds = []
        for n in range(15): self.diamonds.append(True)
        self.clubs = []
        for n in range(15): self.clubs.append(True)
        self.spades = []
        for n in range(15): self.spades.append(True)
        
                
        #maintain counters for quicker probability calculations
        self.totalCount = 52
        
        self.heartsCount = 13
        self.diamondsCount = 13
        self.clubsCount = 13
        self.spadesCount = 13
        
        self.valueCount = []
        self.valueCount.append(0)
        self.valueCount.append(0)
        for v in range(14):
            self.valueCount.append(4)
    
    def getCard(self):
        #get user input about the card
        v = raw_input("Value: ")
        s = raw_input("Suit: ")
        
        #modify keyboard input a little        
        if v == "j": v = 11
        elif v == "q": v = 12
        elif v == "k": v = 13
        elif v == "a": v = 14
        else: v = int(v)
    
        #update the deck's counters
        self.valueCount[v] -= 1
        if (s == "h"): 
            self.heartsCount -= 1
            self.hearts[v] = False
        if (s == "d"): 
            self.diamondsCount -= 1
            self.diamonds[v] = False
        if (s == "s"): 
            self.spadesCount -= 1
            self.spades[v] = False
        if (s == "c"): 
            self.clubsCount -= 1
            self.clubs[v] = False
        self.totalCount -= 1
        
        #make a card object and return it
        card = Card()
        card.value = v
        card.suit = s
        
        return card
    
    def asList(self):
        cards = []
        for v in range(2, 15):
            if self.hearts[v]:
                card = Card()
                card.value = v
                card.suit = "h"
                cards.append(card)
            if self.diamonds[v]:
                card = Card()
                card.value = v
                card.suit = "d"
                cards.append(card)
            if self.clubs[v]:
                card = Card()
                card.value = v
                card.suit = "c"
                cards.append(card)
            if self.spades[v]:
                card = Card()
                card.value = v
                card.suit = "s"
                cards.append(card)
        return cards
        