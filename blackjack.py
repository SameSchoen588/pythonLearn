import random
import collections
import time

# GLOBAL VARIABLES

# deck of cards - suits are irrelevant in blackjack
deck_of_cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "1", "J", "Q", "K",
                 "A", "2", "3", "4", "5", "6", "7", "8", "9", "1", "J", "Q", "K",
                 "A", "2", "3", "4", "5", "6", "7", "8", "9", "1", "J", "Q", "K",
                 "A", "2", "3", "4", "5", "6", "7", "8", "9", "1", "J", "Q", "K"
                 ]
# deque of deck after shuffle
dq = collections.deque([])

# fictional monetary value of the user
winnings = 0
# amount being bet for current round
bet = 50
# record stats
wins = 0
losses = 0
ties = 0

# functionality variables
first_turn = True
# if the game is still going
game_in_progress = True
# if the round is still going
round_in_progress = True
# current draw -- Your, Dealer's, Your Split's
current_player = "Dealer's"

# lists of cards in each hand
player = []
split = []
dealer = []

# list of score or scores if hand includes an Ace
dealer_score = []
player_score = []
split_score = []

# dictionaries of each seat at the table
dealer_dict = {
    "seat": "dealer",
    "score": 0,
    "status": "active"
}
player_dict = {
    "seat": "player",
    "score": 0,
    "status": "active"
}
split_dict = {
    "seat": "split",
    "score": 0,
    "status": "inactive"
}

round_feedback = "This tells the player how the round ended"


# method play the game of blackjack
def play_game():
    display_rules()
    while game_in_progress:
        new_round()


# method start new round of blackjack
def new_round():
    place_bet()
    shuffle_deck()
    deal()
    while round_in_progress:
        display_game()
        adjust_score()
        check_game_status()
    another_round()


# method to restart global round variables
def restart():
    # restarting global variables to original values
    global dq
    global first_turn
    global round_in_progress
    global current_player
    global player
    global split
    global dealer
    global player_score
    global split_score
    global dealer_score
    global player_dict
    global split_dict
    global dealer_dict

    dq = collections.deque([])
    first_turn = True
    round_in_progress = True
    current_player = "Dealer's"
    player = []
    split = []
    dealer = []
    dealer_score = []
    player_score = []
    split_score = []
    dealer_dict = {
        "seat": "dealer",
        "score": 0,
        "status": "active"
    }
    player_dict = {
        "seat": "player",
        "score": 0,
        "status": "active"
    }
    split_dict = {
        "seat": "split",
        "score": 0,
        "status": "inactive"
    }


# method display game rules if asked
def display_rules():
    console_space()
    print("Blackjack Rules:")
    print("")
    print("_The goal of blackjack is to beat the dealer's hand"
          " without going over 21.")
    print("_All face cards are worth 10.")
    print("_Aces can be worth either 1 or 11.")
    print("_Each player will start with 2 random cards.")
    print("_One of the dealer's cards will be hidden until the end "
          "of the game.")
    print("_There are two options each turn:")
    print("__1) HIT -- You will be given another card.")
    print("__2) STAND -- You hold your total and end your turn.")
    print("_The dealer cannot 'STAND' unless they have 17 or more.")
    print("_The player does not have a minimum to 'STAND'.")
    print("_If your cards exceed 21 you 'BUST'.")
    print("_If you are dealt 21 to begin with, you have 'BLACKJACK!'")
    print("_If you get 'BLACKJACK' you win 1.5x the amount of your"
          " bet.")
    print("_If you are dealt two of the same card, you have the "
          "option to 'SPLIT'.")
    print("_A 'SPLIT' allows you to play two hands at the same time, "
          "but it will double your bet .")
    print("_A tie is called a 'PUSH' and no money is lost or awarded.")
    print("_This version of Blackjack will be played with a single "
          "deck of normal playing cards.")
    print("_When prompted to do so, you may choose your bet ranging from "
          "$50 to $200.")
    print("_You may not increase your bet during a round.")
    # can split up to 3 times (have 4 hands)
    # add in other computer players (3 players and 1 dealer is the standard)
    console_space()


# method spacing within console
def console_space():
    print("")
    print("###########################################################")
    print("")


# method construct a visual card
def print_card(card):
    x = card

    if x == "1":
        print(" ____")
        print("|10  |")
        print("|    |")
        print("|____|")

    elif x == "?":
        print(" ____")
        print("|><><|")
        print("|<><>|")
        print("|><><|")

    else:
        print(" ____")
        print("|" + x + "   |")
        print("|    |")
        print("|____|")


# method displays where the game is currently at
def display_game():
    global dealer
    global player
    global split

    print("Dealers cards: ")
    for i in range(len(dealer)):
        if i == 0:
            if round_in_progress:
                print_card("?")
            else:
                print_card(dealer[i])
        else:
            print_card(dealer[i])

    print("Your cards: ")
    for i in range(len(player)):
        print_card(player[i])

    if len(split) != 0:
        print("Your Split's cards: ")
        for i in range(len(split)):
            print_card(split[i])


# method for first turn
def handle_split_option():
    global player
    global player_dict

    selection = input("[j]HIT -- [k]STAND -- [l]SPLIT -- [i]game rules")
    # validate the selection
    valid = False
    while not valid:
        while selection not in ["j", "k", "l", "i"]:
            selection = input("[j]HIT -- [k]STAND -- [l]SPLIT -- [i]game rules")
        if selection == "j":
            valid = True
            print("player: 'HIT ME'")
            hit(player)
        if selection == "k":
            valid = True
            player_dict["status"] = "stand"
            print("player: 'STAND'")
        if selection == "l":
            valid = True
            print("player: 'SPLIT'")
            create_split()
        if selection == "i":
            display_rules()
            display_game()
            selection = input("[j]HIT -- [k]STAND -- [l]SPLIT")

    time.sleep(1)


# method to take turns
def handle_turn():
    global current_player
    global first_turn
    global player
    global split

    change_turn()

    # if it is a players turn
    if current_player == "Your" or current_player == "Your Split's":
        # check if the player has the option to make a split hand
        if first_turn and player[0] == player[1]:
            handle_split_option()
        else:
            # get the current player
            if current_player == "Your":
                pass_in = player
            else:
                pass_in = split

            # player selection
            selection = input("[j]HIT -- [k]STAND -- [i]game rules")

            # validate the selection
            valid = False
            while not valid:
                while selection not in ["j", "k", "i"]:
                    selection = input("Please select one of the following: "
                                      "[j]HIT -- [k]STAND -- [i]game rules")
                if selection == "j":
                    valid = True
                    print("player: 'HIT ME'")
                    hit(pass_in)
                if selection == "k":
                    valid = True
                    print("player: 'STAND'")
                    if pass_in == player:
                        player_dict["status"] = "stand"
                    else:
                        split_dict["status"] = "stand"
                if selection == "i":
                    display_rules()
                    display_game()
                    selection = input("[j]HIT -- [k]STAND")

        time.sleep(1)
        console_space()
    else:
        algorithm()


# method to change turn
def change_turn():
    global current_player
    global split_dict
    global player_dict
    global dealer_dict

    next_turn = True

    if current_player == "Your":
        if split_dict["status"] == "active":
            current_player = "Your Split's"
        else:
            if dealer_dict["status"] == "active":
                current_player = "Dealer's"
            elif player_dict["status"] == "active":
                current_player = "Your"
            else:
                next_turn = False
                check_game_status()
    elif current_player == "Your Split's":
        if dealer_dict["status"] == "active":
            current_player = "Dealer's"
        elif player_dict["status"] == "active":
            current_player = "Your"
        elif split_dict["status"] == "active":
            current_player = "Your Split's"
        else:
            next_turn = False
            check_game_status()
    else:
        if player_dict["status"] == "active":
            current_player = "Your"
        else:
            if split_dict["status"] == "active":
                current_player = "Your Split's"
            elif dealer_dict["status"] == "active":
                current_player = "Dealer's"
            else:
                next_turn = False
                check_game_status()

    if next_turn:
        # display changes to console
        console_space()
        print(current_player + " turn")


# method place bet
def place_bet():
    global bet

    # have user place their bet
    placed = input("Place your bet: [h]50 -- [j]100 -- [k]150 -- [l]200")

    # validate the users input
    valid = False
    while not valid:
        while placed not in ["h", "j", "k", "l"]:
            placed = input("Please select an amount to bet: [h]50 -- [j]100 -- [k]150 -- [l]200")
        if placed == "h":
            valid = True
            bet = 50
        if placed == "j":
            valid = True
            bet = 100
        if placed == "k":
            valid = True
            bet = 150
        if placed == "l":
            valid = True
            bet = 200

    # let the user know their standing
    console_space()
    print("Your current winnings: " + str(winnings))
    print("You are going to bet " + str(bet) + " for this round")
    console_space()


# method shuffle the deck
def shuffle_deck():
    global deck_of_cards

    # shuffle the order of the deck_of_cards
    random.shuffle(deck_of_cards)

    # iterate through the deck of cards and place into a deque
    for i in range(52):
        dq.append(deck_of_cards[i][0])

    # sleep to make somewhat realistic
    print("shuffling in progress...")
    time.sleep(3)

    console_space()


# method deal each hand
def deal():
    # deal first four cards
    for i in range(4):
        x = dq.pop()
        # every other card dealt to two players
        if i == 0 or i == 2:
            player.append(x)
        if i == 1 or i == 3:
            dealer.append(x)


# method hit selected
def hit(hand):
    global player
    global dealer
    global split

    # next card of deck
    x = dq.pop()

    # add card to the hand that called it
    if hand == player:
        player.append(x)
    elif hand == dealer:
        dealer.append(x)
    else:
        split.append(x)


# method split
def create_split():
    global current_player
    global split_dict
    global player

    # restart turns
    current_player = "Dealer's"

    # split_dict status is active
    split_dict["status"] = "active"

    # pull second player card
    card = player[1]

    # remove card from player
    player.pop(1)
    hit(player)

    # put card in split hand
    split.append(card)
    hit(split)


# method to adjust scores
def adjust_score():
    global dealer_score
    global player_score
    global split_score
    global dealer
    global player
    global split

    # restart scores
    dealer_score.clear()
    player_score.clear()
    split_score.clear()

    # calculate values of each hand
    dealer_score = calculate_value(dealer)
    player_score = calculate_value(player)
    split_score = calculate_value(split)


# method to calculate value of a hand
def calculate_value(hand):
    # score variables
    score = 0
    score2 = 0
    scores = []

    # add up card values
    for card in hand:
        if card == "A":
            score2 += 11
            score += 1
        elif card in ["1", "J", "Q", "K"]:
            score += 10
        else:
            score += int(card)

    # add score(s) to list of score(s)
    scores.append(score)
    # if an ace was in their hand
    if score2 != 0:
        score2 = score2 + score - 1
        # add second score
        scores.append(score2)

    # return a list containing one or two scores
    return scores


def check_game_status():
    global player_dict
    global dealer_dict
    global split_dict
    global player_score
    global dealer_score
    global split_score
    global round_feedback

    game_status = 0
    busts = 0
    stands = 0
    twenty_ones = 0
    still_need = True

    # check how many hands of cards there are for this round
    if split_dict["status"] == "inactive":
        hands = 2
    else:
        hands = 3

    # if someone has 21
    if 21 in dealer_score:
        round_feedback = "Dealer has BLACKJACK"
        twenty_ones += 1
        game_status = 2
    if 21 in player_score:
        round_feedback = "You have BLACKJACK!"
        twenty_ones += 1
        still_need = False
        game_status = 4
    if hands == 3 and 21 in split_score:
        round_feedback = "Your Split hand has BLACKJACK!"
        game_status = 1
        if still_need:
            twenty_ones += 1

    # call update_dictionary method
    diction = update_dictionary(dealer_score)
    if diction["status"] == "busted":
        dealer_dict["status"] = diction["status"]
    dealer_dict["score"] = diction["score"]
    # call update_dictionary method
    diction = update_dictionary(player_score)
    if diction["status"] == "busted":
        player_dict["status"] = diction["status"]
    player_dict["score"] = diction["score"]
    if hands == 3:
        diction = update_dictionary(split_score)
        if diction["status"] == "busted":
            split_dict["status"] = diction["status"]
        split_dict["score"] = diction["score"]

    # notify if someone stand
    if dealer_dict["status"] == "stand":
        round_feedback = "Dealer hand: STAND"
        print("Dealer hand: STAND")
        stands += 1
    if player_dict["status"] == "stand":
        round_feedback = "Player hand: STAND"
        print("Player hand: STAND")
        stands += 1
    if hands == 3 and split_dict["status"] == "stand":
        round_feedback = "Split hand: STAND"
        print("Split hand: STAND")
        stands += 1

    # notify if someone bust
    if dealer_dict["status"] == "busted":
        round_feedback = "Dealer hand: BUSTED"
        print("Dealer hand: BUSTED")
        busts += 1
        game_status = 1
    if player_dict["status"] == "busted":
        round_feedback = "Player hand: BUSTED"
        print("Player hand: BUSTED")
        busts += 1
        if hands == 3:
            if split_dict["status"] == "busted":
                game_status = 2
        else:
            game_status = 2

    if hands == 3 and split_dict["status"] == "busted":
        round_feedback = "Split hand: BUSTED"
        print("Split hand: BUSTED")
        busts += 1

    # tie if multiple have 21
    if twenty_ones > 1:
        game_status = 3

    # tie if everyone bust
    if busts == hands:
        game_status = 3

    # if everyone stand
    if stands == hands:
        s = split_dict["score"]
        d = dealer_dict["score"]
        p = player_dict["score"]
        if d > p and d > s:
            game_status = 2
        if p > d or s > d:
            game_status = 1
        if p == d or s == d:
            game_status = 3

    # interpret check_game_status
    update_game_status(game_status)


# method to interpret check_game_status
def update_game_status(status):
    global round_in_progress
    global winnings
    global wins
    global losses
    global ties
    global player_dict
    global dealer_dict
    global split_dict
    global bet
    global round_feedback

    if status > 0:
        display_game()
        round_in_progress = False
        # inform player if round has been won
        if status == 1:
            console_space()
            print(round_feedback)
            print("You Won This Round!")
            if player_dict["score"] > split_dict["score"]:
                print("Score: " + str(player_dict["score"]) + "-" + str(dealer_dict["score"]))
            else:
                print("Score: " + str(split_dict["score"]) + "-" + str(dealer_dict["score"]))
            # add win stats
            wins += 1
            winnings += bet
        # inform player if round has been lost
        elif status == 2:
            console_space()
            print(round_feedback)
            print("The Dealer won this round")
            if player_dict["score"] > split_dict["score"]:
                print("Score: " + str(player_dict["score"]) + "-" + str(dealer_dict["score"]))
            else:
                print("Score: " + str(split_dict["score"]) + "-" + str(dealer_dict["score"]))
            # add loss stats
            losses += 1
            if split_dict["status"] != "inactive":
                winnings -= bet * 2
            else:
                winnings -= bet
        # inform player if round has been tied
        elif status == 3:
            console_space()
            print(round_feedback)
            print("This round ended in a tie")
            print("Score: " + str(dealer_dict["score"]) + "-" + str(dealer_dict["score"]))
            # add tie stat
            ties += 1
        # blackjack pays more
        elif status == 4:
            console_space()
            print(round_feedback)
            print("You Won This Round!")
            print("Score: " + str(player_dict["score"]) + "-" + str(dealer_dict["score"]))
            # add win stats
            wins += 1
            winnings += bet * 1.5
        display_game()
        console_space()
    else:
        handle_turn()


# method to update dictionary variables
def update_dictionary(scores_list):
    # dictionary variable
    diction = {
        "score": 0,
        "status": "active"
    }

    # check if there are multiple scores
    if len(scores_list) == 2:
        # check which score is closer to 21 without going over
        score2 = scores_list.pop()
        score1 = scores_list.pop()
        # if both scores bust
        if score1 > 21 and score2 > 21:
            diction["status"] = "busted"
            diction["score"] = 0
        # else if only one of the scores bust
        elif score2 > 21:
            diction["score"] = score1
        elif score1 > 21:
            diction["score"] = score2
        # else both scores are under 21
        else:
            if score1 > score2:
                diction["score"] = score1
            else:
                diction["score"] = score2
    else:
        score = scores_list.pop()
        if score > 21:
            diction["status"] = "busted"
            diction["score"] = 0
        else:
            diction["score"] = score

    # return the dictionary
    return diction


# method to handle if player wants to play another round
def another_round():
    # using global variable
    global game_in_progress

    print("Would you like to play another round?")
    option = input("[j]YES -- [k]NO")
    # validate the users input
    valid = False
    while not valid:
        while option not in ["j", "k"]:
            option = input("Play again?: [j]YES -- [k]NO")
        if option == "j":
            valid = True
            game_in_progress = True
            restart()
        if option == "k":
            valid = True
            game_in_progress = False
            console_space()
            print("Your Final Winnings: $" + str(winnings))
            print("You left the table with a " + str(wins) + "-" + str(losses) + "-" + str(ties) + " record.")
            console_space()
            print("Credits:")
            print("Developed by Travis Schoen")
            print("Developed in python programming language 2019")


# method dealer algorithm
def algorithm():
    global dealer_dict
    global player_dict
    global split_dict

    # sleep to make somewhat realistic
    print("dealer thinking...")
    time.sleep(4)

    # pull current scores
    d = dealer_dict["score"]
    p = player_dict["score"]
    s = split_dict["score"]

    # stand if score is 17 or more and better than player and split hand
    if d > 16 and d > p and d > s:
        print("dealer: 'STAND'")
        dealer_dict["status"] = "stand"
    else:
        print("dealer: 'HIT'")
        hit(dealer)

    time.sleep(1)
    console_space()


play_game()
