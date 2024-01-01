from random import shuffle


def getValue(card):
        '''
        Name       : getValue
        Parameters : (Tuple[String, String]) card := The card to get the value of 
        Return     : (int) The integer value of the suit
        Purpose    : Get the value of the card given
        Notes      : Assumes that the A is 11
        '''
        rank = card[1]
        if rank == 'J' or rank == 'Q' or rank == 'K':
                return 10
        elif rank == 'A':
                return 11
        else: 
                return int(rank)

def isHit():
        '''
        Name       : getHit
        Parameters : None
        Return     : (bool) Returns true if hitting, false if checking
        Purpose    : Gets the player input from user if hitting
        Notes      : If the input is not hit or check, it will keep asking;
                     Not a pure function, as it deals with user input
        '''
        print("Hit or Check:")
        inputValue = input().lower()
        if inputValue == "hit":
                return True
        elif inputValue == "check":
                return False
        else:
                return isHit()

def getHandTotal(hand):
        '''
        Name       : getHandTotal
        Parameters : List[Tuple[String, String]] hand := List of the cards that the user has in their hand
        Return     : (int) The total sum, trying to stay under 21 if possible (using the A's to reduce hand)
        Purpose    : Gets the value of the hand that is being played
        '''
        handValues = [getValue(card) for card in hand]
        return reduceHandTotal(handValues, 21)

def reduceHandTotal(handValues, maxSize):
        '''
        Name       : reduceHandTotal
        Parameters : (List[int]) handValues := The values of the current cards; assumes unreduced aces are 11;
                     (int)       maxSize    := The total size that the hand can currently go up to
        Return     : (int) The total sum that is maximally maxSize, or the minimum over maxSize if it is impossible to be under maxSize
        Purpose    : Finds the best possible sum for the given hand
        '''
        
        totalSum  = sum(handValues)
        if (len(handValues) == 0):
                return totalSum
        
        if totalSum <= maxSize:
                return totalSum
        else: # Check if the first value is an Ace to reduce, then go along
                firstVal = handValues[0]
                if firstVal == 11:
                        return 1 + reduceHandTotal(handValues[1:], maxSize - 1)
                else:
                        return firstVal + reduceHandTotal(handValues[1:], maxSize - firstVal)

def getHand(deck, hit):
        return addCard([], deck, hit)

def addCard(currHand, deck, hit):
        print([getValue(card) for card in currHand], ":", getHandTotal(currHand))
        if (getHandTotal(currHand) >= 21 or not hit(currHand)):
                return currHand, deck
        return addCard(currHand + [deck[0]], deck[1:], hit)
        
def playBlackJack():
        deck = [(suit, rank) for suit in ['S', 'C', 'D', 'H'] for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]
        shuffle(deck)

        print("Player:")
        playerHand, afterPlayerDeck = getHand(deck, lambda hand: isHit())
        print("Dealer:")
        dealerHand, afterDealerDeck = getHand(afterPlayerDeck, lambda hand: getHandTotal(hand) < 16)

        playerScore = getHandTotal(playerHand)
        dealerScore = getHandTotal(dealerHand)

        print("---------------")
        print(playerHand, ":", playerScore)
        print(dealerHand, ":", dealerScore)

        playerAfterBust = -1 if playerScore > 21 else playerScore 
        dealerAfterBust = -1 if dealerScore > 21 else dealerScore 

        if playerAfterBust > dealerAfterBust:
                print("Player Won!")
        elif dealerAfterBust > playerAfterBust:
                print("Dealer Won!")
        else:
                print("The scores were tied!")

playBlackJack()