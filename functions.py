import random

def amountOfPlayers():
    while True:
        try:
            # Hoeveel spelers
            amount = int(input("How many players? "))
            if amount > 4:
                print("Sorry you can only play with 4 players at the same time.")
            elif amount <= 1:
                print("Sorry you can only play this game with 2 or more players.")
            else:
                return amount
        except:
            # Error bericht
            print("Please enter a valid number")

def creatingDeck():
    defaultCards = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    specialCards = ["skip", "reverse", "draw 2", "wild card", "wild draw 4 card"]
    colors = ["blue", "green", "red", "yellow"]

    tempDeck = []
    tempSpecialDeck = []

    for card in defaultCards:
        for color in colors:
            tempDeck.append(f"{color} {card}")

    for card in specialCards[:3]:
        for color in colors:
            tempSpecialDeck.append(f"{color} {card}")

    for card in range(2):
        tempSpecialDeck += (specialCards[-2:])

    deck = tempDeck + tempDeck[:-4] + tempSpecialDeck + tempSpecialDeck
    random.shuffle(deck)

    return deck
    
def handingOutCards(amount, deck):
    players = []

    # De aantal spelers aanmaken met hun dek
    for i in range(amount):
        players.append({f"Player": i+1, "Deck": [], "Score": 0})

    # Kaarten uitdelen 
    for i in range(len(players)):
        for x in range(7):
            players[i]["Deck"].append(deck[0])
            del deck[0]
    
    return players, deck

def piles(deck):
    discardPile = []
    discardPile.append(deck[1])
    deck.pop(0)

    return deck, discardPile
        
def canPlay(currentCard, selectedCardInt, currentPlayer):
    if currentPlayer["Deck"][selectedCardInt].split()[0] == currentCard.split()[0] or currentPlayer["Deck"][selectedCardInt].split()[1] == currentCard.split()[1]:
        print("Correct color")
        return True
    elif selectedCardInt.split()[1] in ("draw", "card"):
        print("Correct color")
        return True
    else:
        return False

def drawCard(currentPlayer, drawPile):
    lst = []
    lst.append(drawPile[0])
    del drawPile[0]
    currentPlayer["Deck"] + lst

    return currentPlayer, drawPile

def specialCardMoves(currentPlayer, selectedCardInt, currentPlayerIndex, drawPile, discardPile, players):
    if currentPlayer["Deck"][selectedCardInt].split()[1] in ("skip"):
        currentPlayerIndex = (currentPlayerIndex + 2) % len(players)
        discardPile.append(currentPlayer["Deck"][selectedCardInt])
        currentPlayer["Deck"].pop([selectedCardInt])
    elif currentPlayer["Deck"][selectedCardInt].split()[1] in ("draw", "2", "draw 2"):
        players.reverse()
    
    return currentPlayer, currentPlayerIndex, drawPile, discardPile, players

def turns(players, deck, discardPile):
    playAgain = True
    drawPile = deck.copy()
    while playAgain:
        specialCards = ["skip", "reverse", "draw 2", "wild card", "wild draw 4 card"]
        currentPlayerIndex = 0
        turns = True

        while turns:
            currentCard = discardPile[-1]
            currentPlayer = players[currentPlayerIndex]
            print(f"\nPlayer's {currentPlayer['Player']} turn.")
            print(f"Current card: {currentCard}")
            print("Your deck:")

            # Kijken wie als uitgespeeld heeft
            if currentPlayer["Deck"] == []:
                turns = False
                currentPlayer["Score"] += 1
                for i in range(len(players)):
                    for x in range(7):
                        players[i]["Deck"].append(deck[0])
                        del deck[0]
                print(players)

            # Als iemand 5 punten heeft heeft hij hele game gewonnen
            for score in players:
                if score["Score"] == 5:
                    print(f"Player {score['Score']} has won the game")

            # De dek uitprinten van de speler die aan de beurt is
            for number, card in enumerate(currentPlayer["Deck"]):
                print(number+1, "| ", card)

            try:
                # Bepalen welk kaart hij wilt
                selectedCardInt = int(input("\nEnter the number of the card you want to play or type '99' to draw a card "))
                selectedCardInt -= 1

                # Speciale kaart
                if currentPlayer["Deck"][selectedCardInt].split()[1] in specialCards:
                    print("Special card detected!", currentPlayer["Deck"][selectedCardInt])
                    if canPlay(currentCard, selectedCardInt, currentPlayer):
                        discardPile.append(currentPlayer["Deck"][selectedCardInt])
                        currentPlayer["Deck"].pop(selectedCardInt)
                        currentPlayerIndex = (currentPlayerIndex + 1) % len(players)
                    else:
                        print("Invalid input. Please enter a valid number.")

                # Error bericht
                elif selectedCardInt < 0 or selectedCardInt >= len(currentPlayer["Deck"]):
                    print("Invalid input. Please enter a valid number.")

                # Als hij kaart wilt pakken
                elif selectedCardInt == 99:
                    currentPlayer, drawPile = drawCard(currentPlayer, drawPile)
                    currentPlayerIndex = (currentPlayerIndex + 1) % len(players)

                # Normale kaart
                else:
                    print("Regular card detected!") 
                    if canPlay(currentCard, selectedCardInt, currentPlayer):
                        discardPile.append(currentPlayer["Deck"][selectedCardInt])
                        currentPlayer["Deck"].pop(selectedCardInt)
                        currentPlayerIndex = (currentPlayerIndex + 1) % len(players)
                    else:
                        print("Invalid input. Please enter a valid number.")
            except:
                print("Invalid input. Please enter a valid number.")