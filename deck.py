#object oriented poker game: Ronan Gleeson, 10/06/2020
from __future__ import print_function
import random
# from math import log10, floor
import math
from operator import attrgetter
import unittest


#global variables
numPlayers = 20
finalScores = []

# classes for game
class Card:
    def __init__(self, value, num, suit):
        self.value = value
        self.num = num
        self.suit = suit

    def show(self):
        print("{} of {}".format(self.num, self.suit))


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]:
            for num in range(2, 15):
                if (num == 11):
                    self.cards.append(Card(num, "Jack", suit))
                elif (num == 12):
                    self.cards.append(Card(num, "Queen", suit))
                elif (num == 13):
                    self.cards.append(Card(num, "King", suit))
                elif (num == 14):
                    self.cards.append(Card(num, "Ace", suit))
                else:
                    self.cards.append(Card(num, num, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def show(self):
        for c in self.cards:
            c.show()

    def drawCard(self):
        return self.cards.pop()


class CommunityCards:
    def __init__(self):
        self.burnedCards = []
        self.communityCards = []

    def showBurned(self):
        for card in self.burnedCards:
            card.show()

    def showCommunity(self):
        for card in self.communityCards:
            card.show()


class Player:
    def __init__(self, num):
        self.playerNumber = num
        self.hand = []
        self.bestFiveCards = []
        self.score = 0
        self.numSpades = 0
        self.numHearts = 0
        self.numClubs = 0
        self.numDiamonds = 0

    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def showHand(self):
        for card in self.hand:
            card.show()


class Dealer:
    def __init__(self):
        self.dealerHand = []

    #dealer should draw card from deck (append it to his hand)
    def takeCard(self, deck):
        self.dealerHand.append(deck.drawCard())

    def showHand(self):
        for card in self.dealerHand:
            card.show()

    def deal(self, player):
        player.hand.append(self.dealerHand.pop())

    def burn(self, community):
        community.burnedCards.append(self.dealerHand.pop())

    def flip(self, community):
        community.communityCards.append(self.dealerHand.pop())


# methods to support gameplay (i.e. sorting and scoring)
def getLowestValue(player):
    lowest = min(player.hand, key=attrgetter("value"))
    # print("lowest value")
    print("lowest value: {lowest.value}")

def sortHand(player):
    player.hand = sorted(player.hand, key=attrgetter("value"))
    # print("\n")
    # player.showHand()

def sortBestCards(player):
    player.bestFiveCards = sorted(player.bestFiveCards, key=attrgetter("value"))


def determineHand(player):
    straightFlush(player)


def straightFlush(player):
    straightFlush = False
    flush = False
    straight = False
    straightIndicies = []
    flushIndicies = []


    # FLUSH
    # determine if there is a flush
    spadeCounter = 0
    heartCounter = 0
    clubCounter = 0
    diamondCounter = 0
    for i in range(len(player.hand)):

        # get the count of each suit in the hand
        if player.hand[i].suit == "Spades":
            spadeCounter += 1
        elif player.hand[i].suit == "Hearts":
            heartCounter += 1
        elif player.hand[i].suit == "Clubs":
            clubCounter += 1
        elif player.hand[i].suit == "Diamonds":
            diamondCounter += 1

        # determine which suit has the flush and get the indicies of the relevant cards
        if spadeCounter >= 5:
            flush = True
            for i in range(len(player.hand)):
                if player.hand[i].suit == "Spades":
                    flushIndicies.append(i)
        elif heartCounter >= 5:
            flush = True
            for i in range(len(player.hand)):
                if player.hand[i].suit == "Hearts":
                    flushIndicies.append(i)
        elif clubCounter >= 5:
            flush = True
            for i in range(len(player.hand)):
                if player.hand[i].suit == "Clubs":
                    flushIndicies.append(i)
        elif diamondCounter >= 5:
            flush = True
            for i in range(len(player.hand)):
                if player.hand[i].suit == "Diamonds":
                    flushIndicies.append(i)
        
        if flush == True:
            for i in range(len(flushIndicies)):
                player.bestFiveCards.append(player.hand[flushIndicies[i]])
            player.score += 100000
    

    # STRAIGHT
    # determine if there is a straight
    # hand is sorted so just need to check for 5 consecuitive numbers
    counter = 0
    highestCounter = 0
    for i in range(len(player.hand) - 1):
        if (player.hand[i].value == player.hand[i + 1].value - 1):
            counter += 1
            straightIndicies.append(i)
            if counter >= 5:
                straight = True
                player.score += 10000
            if counter > highestCounter:
                highestCounter = counter
        else:
            counter = 0
            if straight == False:
                straightIndicies = []
        
        if straight == True and flush == False:
            for i in range(len(straightIndicies)):
                player.bestFiveCards.append(player.hand[straightIndicies[i]])
                player.bestFiveCards = player.bestFiveCards[-5:]


    # STRAIGHT FLUSH
    # if there is both a straight and a flush in a hand, need to check if it is also a straight flush
    # easiest way to do this is just check if the cards which make up the flush are a straight
    # only nessecary to check if there is already a flush and a straight
    straightFlushCounter = 0
    straightFlushIndicies = []
    if straight == True and flush == True:
        for i in range(len(flushIndicies) - 1):
            if (player.hand[flushIndicies[i]].value == player.hand[flushIndicies[i + 1]].value - 1):
                straightFlushCounter += 1
                straightFlushIndicies.append(i)

                if straightFlushCounter >= 5:
                    straightFlush = True
                    player.score += 100000000

            else:
                straightFlushCounter = 0
                if straightFlush == False:
                    straightFlushIndicies = []
    
    
    if straightFlush == True:
        player.bestFiveCards = []
        for i in range(len(straightFlushIndicies)):
            player.bestFiveCards.append(player.hand[straightFlushIndicies[i]])
        if len(player.bestFiveCards > 5):
            player.bestFiveCards = player.bestFiveCards[-5:]

    else:
        player.bestFiveCards = player.bestFiveCards[-5:]
    
            
    # print("------------")
    # print("Straight Flush: " + str(straightFlush))
    # print("Flush: " + str(flush))
    # print("Straight: " + str(straight))
    
    kinds(player)
        

# determine if there is a hand based on matches (i.e. four of a kind, full house, etc.)
def kinds(player):
    straightOrFlush = False
    if len(player.bestFiveCards) >= 5:
        straightOrFlush = True
    fourOfAKind = False
    fullHouse = False
    threeOfAKind = False
    twoPair = False
    twoOfAKind = False
    
    # flag is used to make sure three of a kind is not interpreted as both two of a kind AND three of a kind
    flag = False

    pairIndicies = []

    counter = 0
    for i in range(len(player.hand) - 1):
        if player.hand[i].value == player.hand[i + 1].value:
            counter += 1
            if counter == 3:
                fourOfAKind = True
                pairIndicies = []
                pairIndicies.append(i - 2)
                pairIndicies.append(i - 1)
                pairIndicies.append(i)
                pairIndicies.append(i + 1)
                player.score += 10000000
            elif counter == 2:
                threeOfAKind = True
                pairIndicies.append(i + 1)
                player.score += 1000
                if flag == False:
                    twoOfAKind = False
                    flag = True
            elif counter == 1:
                if twoOfAKind == True:
                    twoPair = True
                    flag = True
                    pairIndicies.append(i)
                    pairIndicies.append(i + 1)
                    player.score += 100
                else:
                    twoOfAKind = True
                    pairIndicies.append(i)
                    pairIndicies.append(i + 1)
                    player.score += 10
        else:
            counter = 0
    if twoOfAKind == True and threeOfAKind == True:
        fullHouse = True
        player.score += 1000000

    # print("+++++++++++++")
    # for i in range(len(pairIndicies)):
    #     print(pairIndicies[i])

    if straightOrFlush == False:
        pairIndicies.reverse()
        if fourOfAKind == True:
            for i in range(len(pairIndicies)):
                player.bestFiveCards.append(player.hand[pairIndicies[i]])
            for i in range(len(pairIndicies)):
                player.hand.pop(pairIndicies[i])
            player.bestFiveCards.insert(0, player.hand[-1])
        elif fullHouse == True:
            # need to organize the full house by (2K, 3K), making sure to use the best possible 2K (as there can be multiple)
            # we are starting with 7 cards (players hand) and trying to get it down to the best 5 (full house with trips and best pair)
            for i in range(len(pairIndicies)):
                player.bestFiveCards.append(player.hand[pairIndicies[i]])
            
                tripsStartingIndex = 0
                for j in range(len(player.bestFiveCards) - 2):
                    if player.bestFiveCards[j].value == player.bestFiveCards[j + 1].value and player.bestFiveCards[j].value == player.bestFiveCards[j + 2].value:
                        tripsStartingIndex = j

                # there exists the possibilty of a 7 card full house (three of a kind + two pair)
                # these conditionals arrange the full house properly if this occurs
                if len(player.bestFiveCards) == 7:
                    # if trips are first 3 cards in hand
                    if tripsStartingIndex == 0:
                        player.bestFiveCards = player.bestFiveCards[5:] + player.bestFiveCards[:3]
                    # trips are in middle of hand
                    elif tripsStartingIndex == 2:
                        player.bestFiveCards = player.bestFiveCards[5:] + player.bestFiveCards[2:5]
                    # trips are at end
                    elif tripsStartingIndex == 4:
                        player.bestFiveCards = player.bestFiveCards[2:]
                # else, handle full house normally (three of a kind + two of a kind)
                elif len(player.bestFiveCards) == 5:
                    if tripsStartingIndex == 0:
                        player.bestFiveCards = player.bestFiveCards[3:] + player.bestFiveCards[:3]
                    


        elif threeOfAKind == True:
            for i in range(3):
                player.bestFiveCards.append(player.hand[pairIndicies[i]])
            for i in range(3):
                player.hand.pop(pairIndicies[i])
            player.bestFiveCards.insert(0, player.hand[-1])
            player.bestFiveCards.insert(0, player.hand[-2])
        elif twoPair == True:
            for i in range(4):
                player.bestFiveCards.append(player.hand[pairIndicies[i]])
            for i in range(4):
                player.hand.pop(pairIndicies[i])
            sortBestCards(player)
            player.bestFiveCards.insert(0, player.hand[-1])
        elif twoOfAKind == True:
            for i in range(2):
                player.bestFiveCards.append(player.hand[pairIndicies[i]])
            for i in range(2):
                player.hand.pop(pairIndicies[i])
            player.bestFiveCards.insert(0, player.hand[-1])
            player.bestFiveCards.insert(0, player.hand[-2])
            player.bestFiveCards.insert(0, player.hand[-3])
        else:
            for i in range(5):
                player.bestFiveCards.append(player.hand[i + 2])


        # print("*******!!!!!!!!!******")
        for i in range(len(player.bestFiveCards)):
            player.bestFiveCards[i].show()
        print("*******!!!!!!!!!******")


    # print("Four of a kind: " + str(fourOfAKind))
    # print("Full house: " + str(fullHouse))
    # print("Three of a kind: " + str(threeOfAKind))
    # print("Two of a kind: " + str(twoOfAKind))
    # print("Two pair: " + str(twoPair))
    # print("Score: " + str(player.score))
    # print("-------------")
        
        

# round players score to most significant digit (all that matters is their 5 best cards score)
def roundScores(player):
    if player.score != 0:
        if player.score >= 10 and player.score < 100:
            player.score = 10
        if player.score >= 100 and player.score < 1000:
            player.score = 100
        if player.score >= 1000 and player.score < 10000:
            player.score = 1000
        if player.score >= 10000 and player.score < 100000:
            player.score = 10000
        if player.score >= 100000 and player.score < 1000000:
            player.score = 100000
        if player.score >= 1000000 and player.score < 10000000:
            player.score = 1000000
        if player.score >= 10000000 and player.score < 100000000:
            player.score = 10000000
        if player.score >= 100000000 and player.score < 1000000000:
            player.score = 100000000


# compare scores to determine a winner
def determineWinner(players):
    highestScore = -1
    winnersIndex = []
    for i in range(len(players)):
        if players[i].score > highestScore:
            highestScore = players[i].score
            winnersIndex = []
            winnersIndex.append(players[i].playerNumber)
        elif players[i].score == highestScore:
            winnersIndex.append(players[i].playerNumber)
    if len(winnersIndex) == 1:
        print("The winner is: Player " + str(players[winnersIndex[0]].playerNumber), end="")
        if players[winnersIndex[0]].score == 0:
            print(" with a HIGH CARD")
        elif players[winnersIndex[0]].score == 10:
            print(" with TWO OF A KIND")
        elif players[winnersIndex[0]].score == 100:
            print(" with TWO PAIR")
        elif players[winnersIndex[0]].score == 1000:
            print(" with THREE OF A KIND")
        elif players[winnersIndex[0]].score == 10000:
            print(" with a STRAIGHT")
        elif players[winnersIndex[0]].score == 100000:
            print(" with a FLUSH")
        elif players[winnersIndex[0]].score == 1000000:
            print(" with a FULL HOUSE")
        elif players[winnersIndex[0]].score == 10000000:
            print(" with FOUR OF A KIND")
        elif players[winnersIndex[0]].score == 100000000:
            print(" with a STRAIGHT FLUSH")
    
    # if the length of winners is greater than one, there is a tie and it must be solved
    else:
        print("-tie-")
        tyingScore = players[winnersIndex[0]].score

        # STRAIGHT FLUSH tie-breaker
        if tyingScore == 100000000:
            highestCard = 0
            tyingIndex = []
            # only have to check the highest card among tying players
            # if only one person has the highest card
            for i in range(len(winnersIndex)):
                if players[winnersIndex[i]].bestFiveCards[-1].value > highestCard:
                    highestCard = players[winnersIndex[i]].bestFiveCards[-1].value
                    tyingIndex = []
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
                elif players[winnersIndex[i]].bestFiveCards[-1].value == highestCard:
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
            if (len(tyingIndex) == 1):
                print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + "with a STRAIGHT FLUSH")
            else:
                print("There is a tie between", end='')
                for i in range(len(tyingIndex)):
                    if i + 1 == len(tyingIndex):
                        print(" Player " + str(players[tyingIndex[i]].playerNumber), end='')
                    else:
                        print(" Player " + str(players[tyingIndex[i]].playerNumber) + ",", end='')
                print(" with a STRAIGHT FLUSH")    
            


        # FLUSH tie-breaker
        if tyingScore == 100000:
            highestCurrentCard = 0
            tyingIndex = []
            # loop through 5 times to check every card
            for i in range(5):
                for j in range(len(winnersIndex)):
                    if players[winnersIndex[j]].bestFiveCards[-(i + 1)].value > highestCurrentCard:
                        highestCurrentCard = players[winnersIndex[j]].bestFiveCards[-(i + 1)].value
                        tyingIndex = []
                        tyingIndex.append(players[winnersIndex[j]].playerNumber)
                    elif players[winnersIndex[j]].bestFiveCards[-(i + 1)].value == highestCurrentCard:
                        tyingIndex.append(players[winnersIndex[j]].playerNumber)
                # if there is one player with the highest card, they are the winner
                # else, shorten the winners index to the remaining players and loop again
                if len(tyingIndex) == 1:
                    print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with a FLUSH")
                    winnersIndex = tyingIndex
                    break
                else:
                    winnersIndex = tyingIndex
            if len(winnersIndex) > 1:
                print("There is a tie between", end='')
                for i in range(len(winnersIndex)):
                    if i + 1 == len(winnersIndex):
                        print(" Player " + str(players[winnersIndex[i]].playerNumber), end='')
                    else:
                        print(" Player " + str(players[winnersIndex[i]].playerNumber) + ",", end='')
                print(" with a FLUSH") 

            


        # STRAIGHT tie-breaker
        if tyingScore == 10000:
            highestCard = 0
            tyingIndex = []
            # only have to check the highest card among tying players
            # if only one person has the highest card
            for i in range(len(winnersIndex)):
                if players[winnersIndex[i]].bestFiveCards[-1].value > highestCard:
                    highestCard = players[winnersIndex[i]].bestFiveCards[-1].value
                    tyingIndex = []
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
                elif players[winnersIndex[i]].bestFiveCards[-1].value == highestCard:
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
            if (len(tyingIndex) == 1):
                print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + "with a STRAIGHT")
            else:
                print("There is a tie between", end='')
                for i in range(len(tyingIndex)):
                    if i + 1 == len(tyingIndex):
                        print(" Player " + str(players[tyingIndex[i]].playerNumber), end='')
                    else:
                        print(" Player " + str(players[tyingIndex[i]].playerNumber) + ",", end='')
                print(" with a STRAIGHT")        





        # FOUR OF A KIND tie-breaker
        if tyingScore == 10000000:
            highestPairValue = 0
            tyingIndex = []
            for i in range(len(winnersIndex)):
                if players[winnersIndex[i]].bestFiveCards[-1].value > highestPairValue:
                    highestPairValue = players[winnersIndex[i]].bestFiveCards[-1].value
                    tyingIndex = []
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
                elif players[winnersIndex[i]].bestFiveCards[-1].value == highestPairValue:
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
            if len(tyingIndex) == 1:
                print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with FOUR OF A KIND")
            else:
                winnersIndex = []
                winnersIndex = tyingIndex
                tyingIndex = []
                highestRemainingCard = 0
                for i in range(len(winnersIndex)):
                    if players[winnersIndex[i]].bestFiveCards[-5].value > highestRemainingCard:
                        highestRemainingCard = players[winnersIndex[i]].bestFiveCards[-5].value
                        tyingIndex = []
                        tyingIndex.append(players[winnersIndex[i]].playerNumber)
                    elif players[winnersIndex[i]].bestFiveCards[-5].value > highestRemainingCard:
                        tyingIndex.append(players[winnersIndex[i]].playerNumber)
                if len(tyingIndex) == 1:
                    print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with FOUR OF A KIND")
                else:
                    print("There is a tie between", end='')
                    for i in range(len(winnersIndex)):
                        if i + 1 == len(winnersIndex):
                            print(" Player " + str(players[winnersIndex[i]].playerNumber), end='')
                        else:
                            print(" Player " + str(players[winnersIndex[i]].playerNumber) + ",", end='')
                    print(" with FOUR OF A KIND")                    


        # FULL HOUSE tie-breaker
        if tyingScore == 1000000:
            highestTripValue = 0
            tyingIndex = []
            for i in range(len(winnersIndex)):
                if players[winnersIndex[i]].bestFiveCards[-1].value > highestTripValue:
                    highestTripValue = players[winnersIndex[i]].bestFiveCards[-1].value
                    tyingIndex = []
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
                elif players[winnersIndex[i]].bestFiveCards[-1].value == highestTripValue:
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
            if len(tyingIndex) == 1:
                print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with a FULL HOUSE")
            else:
                winnersIndex = []
                winnersIndex = tyingIndex
                tyingIndex = []
                highestPairValue = 0
                for i in range(len(winnersIndex)):
                    if players[winnersIndex[i]].bestFiveCards[-4].value > highestPairValue:
                        highestPairValue = players[winnersIndex[i]].bestFiveCards[-4].value
                        tyingIndex = []
                        tyingIndex.append(players[winnersIndex[i]].playerNumber)
                    elif players[winnersIndex[i]].bestFiveCards[-5].value > highestPairValue:
                        tyingIndex.append(players[winnersIndex[i]].playerNumber)
                if len(tyingIndex) == 1:
                    print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with a FULL HOUSE")
                else:
                    print("There is a tie between", end="")
                    for i in range(len(winnersIndex)):
                        if i + 1 == len(winnersIndex):
                            print(" Player " + str(players[winnersIndex[i]].playerNumber), end="")
                        else:
                            print(" Player " + str(players[winnersIndex[i]].playerNumber) + ",", end="")
                    print(" with a FULL HOUSE") 

        
        
        # THREE OF A KIND tie-breaker
        if tyingScore == 1000:
            highestPairValue = 0
            tyingIndex = []
            for i in range(len(winnersIndex)):
                if players[winnersIndex[i]].bestFiveCards[-1].value > highestPairValue:
                    highestPairValue = players[winnersIndex[i]].bestFiveCards[-1].value
                    tyingIndex = []
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
                elif players[winnersIndex[i]].bestFiveCards[-1].value == highestPairValue:
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
            if len(tyingIndex) == 1:
                print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with THREE OF A KIND")
            else:
                winnersIndex = []
                winnersIndex = tyingIndex
                tyingIndex = []
                j = 4
                while j <= 5:
                    highestRemainingCardValue = 0
                    for i in range(len(winnersIndex)):
                        if players[winnersIndex[i]].bestFiveCards[-j].value > highestRemainingCardValue:
                            highestRemainingCardValue = players[winnersIndex[i]].bestFiveCards[-j].value
                            tyingIndex = []
                            tyingIndex.append(players[winnersIndex[i]].playerNumber)
                        elif players[winnersIndex[i]].bestFiveCards[-j].value == highestRemainingCardValue:
                            tyingIndex.append(players[winnersIndex[i]].playerNumber)
                    if len(tyingIndex) == 1:
                        print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with THREE OF A KIND")
                        quit()
                    else:
                        winnersIndex = []
                        winnersIndex = tyingIndex
                        tyingIndex = []
                        j += 1

                if len(winnersIndex) > 1:
                    print("There is a tie between", end="")
                    for i in range(len(winnersIndex)):
                        if i + 1 == len(winnersIndex):
                            print(" Player " + str(players[winnersIndex[i]].playerNumber), end="")
                        else:
                            print(" Player " + str(players[winnersIndex[i]].playerNumber) + ",", end="")
                    print(" with THREE OF A KIND")

        # TWO PAIR tie-breaker
        if tyingScore == 100:
            # a tie exists if two players have the same high pair
            highestPairValue = 0
            tyingIndex = []
            for i in range(len(winnersIndex)):
                if players[winnersIndex[i]].bestFiveCards[-1].value > highestPairValue:
                    highestPairValue = players[winnersIndex[i]].bestFiveCards[-1].value
                    tyingIndex = []
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
                elif players[winnersIndex[i]].bestFiveCards[-1].value == highestPairValue:
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
            if len(tyingIndex) == 1:
                print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with TWO PAIR")
            else:
                # now check second pair to see if a tie still exists
                # reset indicies to repeat process
                winnersIndex = []
                winnersIndex = tyingIndex
                tyingIndex = []
                highestSecondPair = 0
                for i in range(len(winnersIndex)):
                    if players[winnersIndex[i]].bestFiveCards[-3].value > highestSecondPair:
                        highestSecondPair = players[winnersIndex[i]].bestFiveCards[-3].value
                        tyingIndex = []
                        tyingIndex.append(players[winnersIndex[i]].playerNumber)
                    elif players[winnersIndex[i]].bestFiveCards[-1].value == highestSecondPair:
                        tyingIndex.append(players[winnersIndex[i]].playerNumber)
                if len(tyingIndex) == 1:
                    print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with TWO PAIR")
                # if not, a tie still exists and must be settled by the final card in the hand
                else:
                    winnersIndex = []
                    winnersIndex = tyingIndex
                    tyingIndex = []
                    highestFinalCard = 0
                    for i in range(len(winnersIndex)):
                        if players[winnersIndex[i]].bestFiveCards[-5].value > highestFinalCard:
                            highestFinalCard = players[winnersIndex[i]].bestFiveCards[-3].value
                            tyingIndex = []
                            tyingIndex.append(players[winnersIndex[i]].playerNumber)
                        elif players[winnersIndex[i]].bestFiveCards[-5].value == highestFinalCard:
                            tyingIndex.append(players[winnersIndex[i]].playerNumber)
                    if len(tyingIndex) == 1:
                        print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with TWO PAIR")
                        quit()
                    else:
                        print("There is a tie between", end="")
                        for i in range(len(tyingIndex)):
                            if i + 1 == len(tyingIndex):
                                print(" Player " + str(players[tyingIndex[i]].playerNumber), end="")
                            else:
                                print(" Player " + str(players[tyingIndex[i]].playerNumber) + ",", end="")
                        print(" with TWO PAIR")

        # TWO OF A KIND tie-breaker
        if tyingScore == 10:
            highestPairValue = 0
            tyingIndex = []
            for i in range(len(winnersIndex)):
                if players[winnersIndex[i]].bestFiveCards[-1].value > highestPairValue:
                    highestPairValue = players[winnersIndex[i]].bestFiveCards[-1].value
                    tyingIndex = []
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
                elif players[winnersIndex[i]].bestFiveCards[-1].value == highestPairValue:
                    tyingIndex.append(players[winnersIndex[i]].playerNumber)
            if len(tyingIndex) == 1:
                print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with TWO OF A KIND")
            else:
                winnersIndex = []
                winnersIndex = tyingIndex
                tyingIndex = []
                j = 3
                while j <= 5:
                    highestRemainingCardValue = 0
                    for i in range(len(winnersIndex)):
                        if players[winnersIndex[i]].bestFiveCards[-j].value > highestRemainingCardValue:
                            highestRemainingCardValue = players[winnersIndex[i]].bestFiveCards[-j].value
                            tyingIndex = []
                            tyingIndex.append(players[winnersIndex[i]].playerNumber)
                        elif players[winnersIndex[i]].bestFiveCards[-j].value == highestRemainingCardValue:
                            tyingIndex.append(players[winnersIndex[i]].playerNumber)
                    if len(tyingIndex) == 1:
                        print("The winner is: Player " + str(players[tyingIndex[0]].playerNumber) + " with TWO OF A KIND")
                        quit()
                    else:
                        winnersIndex = []
                        winnersIndex = tyingIndex
                        tyingIndex = []
                        j += 1

                if len(winnersIndex) > 1:
                    print("There is a tie between", end="")
                    for i in range(len(winnersIndex)):
                        if i + 1 == len(winnersIndex):
                            print(" Player " + str(players[winnersIndex[i]].playerNumber), end="")
                        else:
                            print(" Player " + str(players[winnersIndex[i]].playerNumber) + ",", end="")
                    print(" with TWO PAIR")
            

# start the actual game here
def playGame():

    # instatiate objects for game
    deck = Deck()
    community = CommunityCards()
    dealer = Dealer()
    players = []
    for i in range(numPlayers):
        players.append(Player(i))


    # play a hand of poker
    # first shuffle
    deck.shuffle()

    # deal to players
    for i in range(numPlayers * 2):
        dealer.takeCard(deck)
        dealer.deal(players[i % numPlayers])

    # burn & turn (flop)
    dealer.takeCard(deck)
    dealer.burn(community)
    for i in range(3):
        dealer.takeCard(deck)
        dealer.flip(community)
    # community.showCommunity()

    # burn & turn (turn)
    for i in range(2):
        dealer.takeCard(deck)
        if i % 2 == 0:
            dealer.burn(community)
        else:
            dealer.flip(community)
    # community.showCommunity()

    # burn & turn (river)
    for i in range(2):
        dealer.takeCard(deck)
        if i % 2 == 0:
            dealer.burn(community)
        else:
            dealer.flip(community)
    # community.showCommunity()


    # no need for community anymore, each players hand is now their 7 unique-ish cards
    # move cards from community to players hands
    for i in range(numPlayers):
        for j in range(len(community.communityCards)):
            players[i].hand.append(community.communityCards[j])


    # sort hands (makes it easier for scoring)
    for i in range(numPlayers):
        sortHand(players[i])

    # print("-----reset----")

    # for i in range(len(players)):
    #     print("Player " + str(i) + " Hand:")
    #     players[i].showHand()

    # determine what hand each player has and assign relevant score
    for i in range(len(players)):
        determineHand(players[i])

    # for i in range(len(players)):
    #     print(players[i].score)

    # print("--------------")

    for i in range(len(players)):
        roundScores(players[i])

    for i in range(len(players)):
        print(players[i].score)

    determineWinner(players)

    


def main():
    playGame()

main()
