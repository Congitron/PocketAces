#Project Pocket Aces (AA)
#Command line version
import sys

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

class Player():
    #players at the table, including me (set me to True in that case)
    def __init__(self):
        self.ID = ""
        self.chips = 1000
        self.site = ""
        self.isMe = False
        self.cards = []
        self.position = 0
        self.hasCards = False
        self.bet = 0
    
class Game():
    #the poker simulation
    def __init__(self):
        #setup the hand
        self.gameStage = 0  #stepping through the stages of dealing and betting
        self.subStage = 0   #some stages have multiple parts (for multi-key inputs, etc)
        self.players = []   #all the player instances
        for n in range(11): self.players.append(None)
        self.playerCount = 0
        self.seats = []
        for n in range(11): self.seats.append(False)
        self.sharedCards = []
        self.inHand = []
        for n in range(11): self.inHand.append(False)
        
        #setup game related variables
        self.deck = Deck()
        
        self.activePlayer = 0
        self.dealerPos = 0
        self.smallBlindPos = 1
        self.bigBlindPos = 2
        self.gameType = 0 #0 = limit, 1 = pot limit, 2 = no limit
        self.smallBet = 10.00
        self.bigBet = 20.00
        self.smallBlind = 5.00
        self.bigBlind = 10.00
        self.pot = 0.00
        self.bet = 0.00
        
    def nextHand():
        #reset a bunch of variables so you can start the next hand
        #all players are back in the hand
        #new deck
        #reset stages
        #pot is 0
        #move dealer button, blind positions, etc
        #activeplayer
        pass
    
    def factorial(self, value):
        total = value
        for n in range(value - 1, 1, -1):
            total *= n
        return total
            
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
        
        if s == "h": s = "H"
        if s == "d": s = "D"
        if s == "c": s = "C"
        if s == "s": s = "S"
        
        #update the deck's counters
        self.deck.valueCount[v] -= 1
        if (s == "H"): self.deck.heartsCount -= 1
        if (s == "D"): self.deck.diamondsCount -= 1
        if (s == "S"): self.deck.spadesCount -= 1
        if (s == "C"): self.deck.clubsCount -= 1
        self.deck.totalCount -= 1
        
        #make a card object and return it
        card = Card()
        card.value = v
        card.suit = s
        
        return card
    
    def printDeck(self):
        #print the counters in the deck object
        pass
    
    def printTable(self):
        #print out the table for reference
        print "SHARED CARDS"
        cards = ""
        for n in range(len(self.sharedCards)):
            card = self.sharedCards[n]
            v = ""
            if card.value == "11": v = "J"
            elif card.value == "12": v = "Q"
            elif card.value == "13": v = "K"
            elif card.value == "14": v = "A"
            else: v = str(card.value)
            cards += v + card.suit + " "
        print cards
        print
                                
        print "PLAYERS"
        for n in range(11):
            if (self.inHand[n]):
                line = "pos: " + str(n)
                p = self.players[n]
                if (p.hasCards):
                    line += " cards: "
                    if (p.isMe):
                        #hole card 1
                        v = p.cards[0].value
                        if v < 11: cards = str(v)
                        else:
                            if v == 11: cards = "J"
                            if v == 12: cards = "Q"
                            if v == 13: cards = "K"
                            if v == 14: cards = "A"
                        cards += p.cards[0].suit + " "
                        #hole card 2
                        v = p.cards[1].value
                        if v < 11: cards += str(v)
                        else:
                            if v == 11: cards += "J"
                            if v == 12: cards += "Q"
                            if v == 13: cards += "K"
                            if v == 14: cards += "A"
                        cards += p.cards[1].suit
                        line += cards
                    else: line += "?? ??"
                if (p.isMe): line += " M"
                if self.dealerPos == n: line += " D"
                if self.smallBlindPos == n: line += " o"
                if self.bigBlindPos == n: line += " oo"
                line += " bet: $" + str(p.bet)
                line += " chips: $" + str(p.chips)
                print line
        print ""
        if self.pot > 0:
            potOdds = str(self.pot/self.bet)
        else: potOdds = "N/A"
        print "Bet: $" + str(self.bet) + " Pot: $" + str(self.pot) + " Pot Odds (Pot/Bet): " + potOdds
        print ""
            
    def nextPlayer(self,n):
        #get the next player at the table (since not all positions are always occupied it's not just n+1)
        go = True
        while (go):
            n += 1
            if n > 9: n = 0
            if (self.inHand[n]): go = False
        return n
    
    def bettingRound(self, lastBet):
        #this function is used for all rounds of betting (they all work the same)
        #lastBet is the last player that has bet, or the dealer, etc (player before the active player)
        
        '''
        ***NOTE: you need to add code at the beginning of this function to catch a heads up game and play
        ***it slightly differently
        '''
        
        '''
        ***NOTE: You need to catch situations where everyone but one player folds so the remaining player
        ***wins by default and the hand is over sending it back to stage 0 and resetting the hand
        '''
        
        
        aPPos = self.nextPlayer(lastBet) #aP = active player, who is first to act
        
        go = True
        while (go):
            aP = self.players[aPPos]
            self.printTable()
            print "Betting:"
            print "Active Player: Position " + str(aPPos)
            if aP.isMe: 
                print "THIS IS ME!"
                if (aP.bet < self.bet):
                    dif = self.bet - aP.bet
                    print "pot odds for call: " + str((self.pot + dif)/dif)
            action = raw_input("(c)Check/Call, (r)Bet/Raise, or (f)Fold:")
            if action == "c":
                dif = self.bet - aP.bet
                aP.chips -= dif
                aP.bet += dif
                self.pot += dif
                if aPPos == lastBet: go = False
            if action == "r":
                bet = int(raw_input("Total bet (call + raise):"))
                while (bet < self.bet): bet = int(raw_input("NOT ENOUGH: "))
                self.bet = bet
                bet -= aP.bet
                aP.chips -= bet
                aP.bet += bet
                self.pot += bet
                lastBet = aPPos
            if action == "f":
                self.inHand[aPPos] = False
            aPPos = self.nextPlayer(aPPos)
            
        print "Betting complete."
        print ""
    
    def run(self):        
        #Stage 0: setup
        if (self.gameStage == 0):
            print "STAGE 0"
            go = True
            while (go):
                self.printTable()
                print "p) add player"
                print "m) add me"
                print "d) dealer position"
                print "g) go!"
                print "q) quit"
                
                input = raw_input(">")
                if (input == "q"): sys.exit()
                if (input == "g"): 
                    go = False
                    self.gameStage = 1
                if (input == "p"):
                    pos = int(raw_input("Enter opponent's position: "))
                    #setup the player
                    player = Player()
                    self.seats[pos] = True
                    self.inHand[pos] = True
                    player.position = pos       #***Might be an unnecessary variable***
                    self.players[pos] = player
                    self.playerCount += 1
                if (input == "m"):
                    pos = int(raw_input("My position: "))
                    self.me = Player()
                    self.me.isMe = True
                    self.me.position = pos
                    self.seats[pos] = True
                    self.inHand[pos] = True
                    self.players[pos] = self.me
                    self.playerCount += 1
                if (input == "d"):
                    pos = int(raw_input("Dealer position: "))
                    self.dealerPos = pos
                    if self.playerCount > 2:
                        self.smallBlindPos = self.nextPlayer(self.dealerPos)
                    else:
                        self.smallBlindPos = self.dealerPos
                    self.bigBlindPos = self.nextPlayer(self.smallBlindPos)
                    
        #Stage 1: blinds and hole cards
        if (self.gameStage == 1):
            #blinds
            print "STAGE 1"
            
            self.players[self.smallBlindPos].chips -= self.smallBlind
            self.players[self.smallBlindPos].bet = self.smallBlind
            self.players[self.bigBlindPos].chips -= self.bigBlind
            self.players[self.bigBlindPos].bet = self.bigBlind
            self.pot += self.smallBlind + self.bigBlind
            self.bet = self.bigBlind
            
            #get my cards
            print "MY HOLE CARDS "
            self.me.cards.append(self.getCard())
            self.me.cards.append(self.getCard())
            
            #set all players to having cards for the printTable()
            for n in range(11):
                if (self.inHand[n]): self.players[n].hasCards = True
                
            #print the table on the screen
            self.printTable()
            
            #go to stage 2(betting)
            self.gameStage = 2
                    
        #Stage 2: betting on hole cards
        if (self.gameStage == 2):
            #pre-flop betting
            print "STAGE 2"
            
            #bettingRound takes the last player to bet/raise, in this case the big blind.
            self.bettingRound(self.bigBlindPos)
            self.gameStage = 3
            
        if (self.gameStage == 3):
            #deal the flop
            print "STAGE 3"
            self.sharedCards.append(self.getCard())
            self.sharedCards.append(self.getCard())
            self.sharedCards.append(self.getCard())
        
            self.gameStage = 4
            
        if (self.gameStage == 4):
            #betting
            print "STAGE 4"
            self.bettingRound(self.dealerPos)
            
            self.gameStage = 5
        
        if (self.gameStage == 5):
            #deal the 4th card (4th street)
            print "STAGE 5"
            self.sharedCards.append(self.getCard())
        
            self.gameStage = 6
            
        if (self.gameStage == 6):
            #betting
            print "STAGE 6"
            self.bettingRound(self.dealerPos)
            
            self.gameStage = 7
        
        if (self.gameStage == 7):
            #deal the 5th and final card
            print "STAGE 7"
            self.sharedCards.append(self.getCard())
            
            self.gameStage = 8
        
        if (self.gameStage == 8):
            #betting
            print "STAGE 8"
            self.bettingRound(self.dealerPos)
            
            self.gameStage = 9
        
        if (self.gameStage == 9):
            #Showdown if at least 2 players are left
            print "STAGE 9"
            
            print "here we have the showdown..."
            self.nextHand()
            self.gameStage = 0
            
game = Game()
game.run()



