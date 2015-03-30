#the deck and cards

class Deck():        
    def __init__(self):
        self.suits = ["h","d","s","c"]
        card = Card()
        self.hearts = []
        self.hearts.append(card)
        self.hearts.append(card)
        self.diamonds = []
        self.diamonds.append(card)
        self.diamonds.append(card)
        self.clubs = []
        self.clubs.append(card)
        self.clubs.append(card)
        self.spades = []
        self.spades.append(card)
        self.spades.append(card)
        for suit in self.suits:
            for v in range(2,15):
                card = Card()
                card.suit = suit
                card.value = v
                fileName = ""
                fileName += str(v)
                fileName += suit
                if (suit == "h"): self.hearts.append(card)
                if (suit == "d"): self.diamonds.append(card)
                if (suit == "c"): self.clubs.append(card)
                if (suit == "s"): self.spades.append(card)
                
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

class Card():
    #a card
    def __init__(self):
        pass        