#Project Pocket Aces (AA)

import direct.directbase.DirectStart
from pandac.PandaModules import *
from pandac.PandaModules import ActorNode, CollisionHandlerEvent, CollisionHandlerGravity, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionTraverser, BitMask32, CollisionRay, NodePath
from pandac.PandaModules import CollisionHandlerQueue,CollisionRay
from pandac.PandaModules import Filename
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode
from pandac.PandaModules import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math, time
from pandac.PandaModules import Material
from pandac.PandaModules import VBase4
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenImage import OnscreenImage
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from pandac.PandaModules import WindowProperties
from pandac.PandaModules import TransparencyAttrib


class Deck():        
    def __init__(self):
        self.suits = ["h","d","s","c"]
        self.cards = []
        for suit in self.suits:
            for v in range(2,15):
                card = Card()
                card.suit = suit
                card.value = v
                fileName = ""
                fileName += str(v)
                fileName += suit
                card.nodePath = loader.loadModel("models/" + fileName)
                card.nodePath.setScale(0.5)
                #collide = loader.loadModel("models/card_collide")
                #collide.setScale(0.5)
                #collide.reparentTo(card.nodePath)
                #collide.setPythonTag("card", card)
                #card.cardCollider = collide.find("**/card_collider")
                card.cardCollider = card.nodePath.attachNewNode(CollisionNode('card_collider'))
                card.cardCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))
                #card.cardCollider.setPos(0,0,1)
                card.cardCollider.setPythonTag("card", card)
                self.cards.append(card)
                card.cardCollider.show()
                
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
        '''
        self.twoCount = 4
        self.threeCount = 4
        self.fourCount = 4
        self.fiveCount = 4
        self.sixCount = 4
        self.sevenCount = 4
        self.eightCount = 4
        self.nineCount = 4
        self.tenCount = 4
        self.jackCount = 4
        self.queenCount = 4
        self.kingCount = 4
        self.aceCount = 4
        '''

class Card():
    #a card
    def __init__(self):
        pass

class Hand():
    #The current hand being played
    def __init__(self):
        self.gameState = 0  #1 = dealing, 2 = betting, 0 = other
        self.gameStage = 0  #stepping through the stages of dealing and betting
        self.players = []
        self.cards = []

class Player():
    #players at the table, including me (set me to True in that case)
    def __init__(self):
        self.ID = ""
        self.chips = 0
        self.site = ""
        self.isMe = False
        self.cards = []
        self.position = 0
        self.nodePath = None
    
class Game(DirectObject):
    #the poker simulation
    def __init__(self):
        #setup the table
        self.table = loader.loadModel("models/table")
        self.positions = []
        pos01 = self.table.find("**/player01")
        self.positions.append(pos01)
        pos02 = self.table.find("**/player02")
        self.positions.append(pos02)
        pos03 = self.table.find("**/player03")
        self.positions.append(pos03)
        pos04 = self.table.find("**/player04")
        self.positions.append(pos04)
        pos05 = self.table.find("**/player05")
        self.positions.append(pos05)
        pos06 = self.table.find("**/player06")
        self.positions.append(pos06)
        pos07 = self.table.find("**/player07")
        self.positions.append(pos07)
        pos08 = self.table.find("**/player08")
        self.positions.append(pos08)
        pos09 = self.table.find("**/player09")
        self.positions.append(pos09)
        pos10 = self.table.find("**/player10")
        self.positions.append(pos10)
        
        #setup game related variables
        self.deck = Deck()
        self.players = []
        self.playerCount = 0
        
        self.me = Player()
        self.me.isMe = True
        self.players.append(self.me)
        self.playerCount += 1
        
        self.hand = Hand()
        
        self.activePlayer = None
        self.dealer = None
        self.smallBlind = None
        self.bigBlind = None
        self.gameType = 0 #0 = limit, 1 = pot limit, 2 = no limit
        self.smallBet = 0
        self.bigBet = 0
        
        self.selectedCard = None
        self.hoveredCard = None
        self.pickingEnabled = False
        
        self.cardQueue = []
        self.actionQueue = []
        
        #temperary setup of some players(later this will be done manually from within the program
        #might want to consider using config files for various games.
        for p in range(5):
            player = Player()
            self.players.append(player)
            self.playerCount += 1
            
        for p in range(6):
            self.players[p].nodePath = self.positions[p]
        
        #setup keyboard controls
        self.keyMap = {"c":0,"b":0,"f":0,"a":0,"r":0,"p":0,"t":0,"s":0,"d":0,"h":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,
                       "8":0,"9":0,"0":0,"j":0,"q":0,"k":0}
        self.accept("escape",sys.exit)
        self.accept("c-up",self.setKey, ["c",1])#check,call,clubs
        self.accept("b-up",self.setKey, ["b",1])#bet, raise
        self.accept("f-up",self.setKey, ["f",1])#fold
        self.accept("r-up",self.setKey, ["r",1])#remove player
        self.accept("p-up",self.setKey, ["p",1])#player menu
        self.accept("t-up",self.setKey, ["t",1])
        self.accept("s-up",self.setKey, ["s",1])#start, spades
        self.accept("d-up",self.setKey, ["d",1])#diamonds
        self.accept("h-up",self.setKey, ["h",1])#hearts
        self.accept("2-up",self.setKey, ["2",1])#2-9 are 2-9 cards
        self.accept("3-up",self.setKey, ["3",1])
        self.accept("4-up",self.setKey, ["4",1])
        self.accept("5-up",self.setKey, ["5",1])
        self.accept("6-up",self.setKey, ["6",1])
        self.accept("7-up",self.setKey, ["7",1])
        self.accept("8-up",self.setKey, ["8",1])
        self.accept("9-up",self.setKey, ["9",1])
        self.accept("0-up",self.setKey, ["0",1])#10 card
        self.accept("j-up",self.setKey, ["j",1])#jack
        self.accept("q-up",self.setKey, ["q",1])#queen
        self.accept("k-up",self.setKey, ["k",1])#king
        self.accept("a-up",self.setKey, ["a",1])#ace
        
        #setup light
        alight = AmbientLight("ambientLight")
        alight.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        alightNP = render.attachNewNode(alight)

        dlight = DirectionalLight("directionalLight")
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.8, 0.8, 0.8, 1))
        dlightNP = render.attachNewNode(dlight)

        render.clearLight()
        render.setLight(alightNP)
        render.setLight(dlightNP)
        
        #setup the camera
        base.disableMouse()
        base.camera.reparentTo(self.table)
        base.camera.setPos(0,0,20)
        #base.camera.setHpr(0,180,0)
        base.camera.lookAt(self.table)
        base.camera.setPos(2,0,25)
        
        #add tasks to task manager
        taskMgr.add(self.update, "updateTask")
        
        #setup the collision stuff for mouse picking
        base.cTrav = CollisionTraverser()
        base.cTrav.showCollisions(render)
        self.collisionHandler = CollisionHandlerEvent()
        
        self.pickerNode = CollisionNode('mouseRayCN')
        self.pickerNP = base.camera.attachNewNode(self.pickerNode)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        base.cTrav.addCollider(self.pickerNP, self.collisionHandler)
        self.pickerNP.show()

        self.collisionHandler.addInPattern('%fn-into-%in')
        self.collisionHandler.addOutPattern('%fn-out-%in')
        self.accept('mouseRayCN-into-card_collider', self.eventIn)
        self.accept('mouseRayCN-out-card_collider', self.eventOut)
        
        self.accept('mouse1', self.mousePick, ['down'])
        #self.accept('mouse1-up', self.mousePick, ['up'])

        #setup the card picking area, and some collision stuff for the cards
        for card in self.deck.cards:
            #print str(card.value) + " " + card.suit
            collumn = 0
            if (card.suit == "d"): collumn = 1   
            if (card.suit == "c"): collumn = 2
            if (card.suit == "s"): collumn = 3
            card.nodePath.reparentTo(self.table)
            card.nodePath.setPos(collumn+7,card.value-7 - 1,0)
            collider = card.cardCollider
            base.cTrav.addCollider(collider, self.collisionHandler)
            
    def mousePick(self, status):
        if self.pickingEnabled:
            print "pickingEnabled"
            if status == 'down':
                self.selectedCard = self.hoveredCard
                print "click"
        else: print "picking NOT enabled"
                
    def eventIn(self, entry):
        print "in"
        self.hoveredCard = entry.getIntoNodePath().getPythonTag("card")
        self.hoveredCard.setScale(1)
        self.hoveredCard.setColor(2,2,2,1)
        #self.selectedCard = card
        self.pickingEnabled = True
        
    def eventOut(self, entry):
        print "out"
        self.hoveredCard.setScale(0.5)
        self.hoveredCard.setColor(1,1,1,1)
        self.hoveredCard = None
        self.pickingEnabled = False
        
    def factorial(self, value):
        total = value
        for n in range(value - 1, 1, -1):
            total *= n
        return total
            
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def getCard(self):
        #this actually needs to prompt the user for input so you can select your cards
        rand = random.randint(0, self.deck.totalCount - 1)
        card = self.deck.cards.pop(rand)
        
        #now that you have your card, update the counters in the deck
        v = card.value
        s = card.suit
        self.deck.valueCount[v] -= 1
        if (s == "h"): self.deck.heartsCount -= 1
        if (s == "d"): self.deck.diamondsCount -= 1
        if (s == "s"): self.deck.spadesCount -= 1
        if (s == "c"): self.deck.clubsCount -= 1
        
        return card
    
    def getBack(self):
        card = Card()
        card.nodePath = loader.loadModel("models/back")
        card.nodePath.setScale(0.5)
        return card
    
    def update(self, task):
        #update the mouse
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mpos.getX(),mpos.getY())

        if (self.keyMap["call"]!=0): 
            print "check/call"
            self.keyMap["call"] = 0
        
        #take keyboard input and update the game
        if (self.hand.gameStage == 0):
            #setup stage.  add players, change limits, etc
            if (self.keyMap["start"]!=0):
                self.hand.gameStage = 1
            
        if (self.hand.gameStage == 1):
            #deal players their 2 cards each
            for p in self.players:
                if p.isMe == True:
                    card1 = self.getCard()
                    card2 = self.getCard()
                    card1.nodePath.reparentTo(p.nodePath)
                    card2.nodePath.reparentTo(p.nodePath)
                    card1.nodePath.setPos(0,0,0)
                    card2.nodePath.setPos(1,0,0)
                else:
                    card1 = self.getBack()
                    card1.nodePath.reparentTo(p.nodePath)
                    card1.nodePath.setPos(0,0,0)
                    card2 = self.getBack()
                    card2.nodePath.reparentTo(p.nodePath)
                    card2.nodePath.setPos(1,0,0)
            
            self.hand.gameStage = 2
                    
        if (self.hand.gameStage == 2):
            #pre-flop betting
            pass
            
        if (self.hand.gameStage == 3):
            #deal the flop
            pass
        
        if (self.hand.gameStage == 4):
            #betting
            pass
        
        if (self.hand.gameStage == 5):
            #deal the 4th card (4th street)
            pass
        
        if (self.hand.gameStage == 6):
            #betting
            pass
        
        if (self.hand.gameStage == 7):
            #deal the 5th and final card
            pass
        
        if (self.hand.gameStage == 8):
            #betting
            pass
        
        if (self.hand.gameStage == 9):
            #Showdown if at least 2 players are left
            pass
        
        return Task.cont
    
game = Game()
run()



