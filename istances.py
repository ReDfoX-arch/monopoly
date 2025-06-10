# LIBRARIES
import numpy as np
import matplotlib.pyplot as plt
import various_func as vfn
import random
import sys
from prop_and_loc import loc_list, prop_list, dict_by_color, properties, locations, community_chest_cards, chance_cards

# CLASSES
# Class that represents the board of the game
class Table:
    def __init__(self, num_players):
        self.players = [None] * num_players
        self.turn = 0
        self.current_pl = self.pl_turn()
        self.prop_dict = {key: None for key in prop_list}   # first element for each prop is the owner, second the houses owned
        self.monopoly_tokens = [
            "Top Hat",
            "Thimble",
            "Boot",
            "Battleship",
            "Scottie Dog",
            "Cat",
            "Wheelbarrow",
            "Iron"
            ]
        self.total_money = 0
        self.max_cash = 20580   # max cash available

    def pl_turn(self):
        return self.players[self.turn % len(self.players)]
    
    def next_turn(self):
        self.turn += 1
        self.current_pl = self.pl_turn()

    def new_house(self, prop):
        self.prop_dict[prop][1] += 1  

    def kill_player(self, player):
        print(f"{player.name} has gone bankrupt and is eliminated from the game.")
        self.players.remove(player)
        for color, properties in player.owned.items():
            for prop in properties:
                self.prop_dict[prop] = None
        # bye bye space cowboy ...    
    
    def check_inflation(self):
        self.total_money = 0    # Reset the total money amount and proceed to count if bank finished the cash available
        for player in self.players:
            self.total_money += player.balance
    
    def whos_winner(self):
        winner = ""
        balance = 0
        for player in self.players:
            new_bal = player.balance
            if  new_bal > balance:
                winner = player.name
                balance = new_bal

        print(f"\n{winner} wins the game at turn {self.turn}, with a final MONOPOLY of {balance} $\n")

# Function that initializes the players and the board, given the number of players
def init_player(num_pl, ROI_type):
    
    TestArray = list()
    board = Table (num_players=num_pl)  # initialize the board

    # Class that represents a player
    class Player:
        def __init__(self, name):
            self.name = name
            self.balance = 1500
            self.owned = {      
                "brown": [],
                "light blue": [],
                "pink": [],
                "orange": [],
                "red": [],
                "yellow": [],
                "green": [],
                "blue": [],
                "railroad": [],
                "utility": []
            }
            self.location = loc_list[0] # "Start"
            self.position = 0

        def turn(self):
            print(f"""\n**********
{board.turn} turn
**********
                  """)
            print(f"{self.name}'s turn: (balance = {self.balance})")
            dice1 = random.randint(1, 6)        # draw phase
            dice2 = random.randint(1, 6)
            print(f"{self.name} rolled {dice1} and {dice2}")    # roll the dice
            self.check_if_pass_go(dice1, dice2)     # check if the player passed go and assigns the money
            self.position = (self.position + (dice1 + dice2)) % 40  # update the position
            self.location = loc_list[self.position]     # update the location
            print(f"{self.name} moved to {self.location}")
            self.prop_types()   # check the type of the location and apply the effects
            self.houses()       # check if we want to build some houses for our props
            if self.balance < 0:
                board.kill_player(self)
                # GAME OVER



        def prop_types(self):
            loc_type = locations[self.location]["type"]
            
            if loc_type in ["go", "free_parking", "jail"]:          # locations without effects
                pass
            elif loc_type == "tax":                                 # tax location
                self.balance -= 150         # average tax amount
                print(f"{self.name} paid 150 in tax")
            elif loc_type in ["community_chest", "chance"]:         # community chest or chance location
                if loc_type == "community_chest":
                    card = random.choice(community_chest_cards)  # returns a random card
                else:
                    card = random.choice(chance_cards)  # returns a random card
                
                if card["category"] == "pay":
                    self.balance += card["effect"]
                    print(f"{self.name} gains {card['effect']} from the random card")
                elif card["category"] == "go":
                    self.location = card["effect"]  
                    print(f"{self.name} moved to {self.location} thanks to the random card")
                    self.prop_types()  

            elif board.prop_dict[self.location] != None:            # property location owned by someone
                self.pay()
            elif board.prop_dict[self.location] == None:            # property location free to buy
                self.buy()
            
        def buy(self):
            if self.balance - properties[self.location]["cost"] < 200:     # we want to be safe, keeping at least 200 $ before making an investment
                print(f"{self.name} doesn't have enough money to buy {self.location}")
                pass
            else:
                if ROI_type == "random":
                    expect_ROI = vfn.random_ROI ()
                    TestArray.append(expect_ROI)
                    print(f"Expected ROI for {self.location}: {expect_ROI:.2f}")
                    if expect_ROI > 0.5:      # if the expected ROI is greater than 1, buy the property
                        self.balance -= properties[self.location]["cost"]
                        self.owned[properties[self.location]["color"]].append(self.location)
                        board.prop_dict[self.location] = [self.name, 0]
                        print(f"{self.name} bought {self.location}")
                
                elif ROI_type == "simple":
                    expect_ROI = vfn.simple_ROI(self)
                    TestArray.append(expect_ROI)
                    print(f"Expected ROI for {self.location}: {expect_ROI:.2f}")
                    if expect_ROI > 0.5:
                        self.balance -= properties[self.location]["cost"]
                        self.owned[properties[self.location]["color"]].append(self.location)
                        board.prop_dict[self.location] = [self.name, 0]
                        print(f"{self.name} bought {self.location}")
                
                elif ROI_type == "complex":
                    expect_ROI = vfn.ROI(self, num_pl, board.turn)
                    TestArray.append(expect_ROI)
                    print(f"Expected ROI for {self.location}: {expect_ROI:.2f}")
                    if expect_ROI > 0.5:
                        self.balance -= properties[self.location]["cost"]
                        self.owned[properties[self.location]["color"]].append(self.location)
                        board.prop_dict[self.location] = [self.name, 0]
                        print(f"{self.name} bought {self.location}")

                elif ROI_type == "color":
                    expect_ROI = vfn.color_ROI(self, board)
                    TestArray.append(expect_ROI)
                    print(f"Expected ROI for {self.location}: {expect_ROI:.2f}")
                    if expect_ROI == 0:
                        print(f"Somebody else owns \"{properties[self.location]["color"]}\" properties, so {self.name} didn't buy {self.location}")
                    elif expect_ROI == 1:
                        print(f"{self.name} already owns \"{properties[self.location]['color']}\" properties")
                    if expect_ROI > 0.2:
                        self.balance -= properties[self.location]["cost"]
                        self.owned[properties[self.location]["color"]].append(self.location)
                        board.prop_dict[self.location] = [self.name, 0]
                        print(f"{self.name} bought {self.location}")
        
        def pay(self):
            place = self.location
            owner = board.prop_dict[place][0]
            me = self.name
            for player in board.players:
                if player.name == owner:
                    if place in self.owned[properties[place]["color"]]:
                        print(f"{me} landed on {place}, which is owned by {owner} (himself)")
                        pass

                    else:
                        if place in dict_by_color["railroad"]:      # bills on railroad
                            num_stat = len(player.owned["railroad"])
                            rent = 25 * 2 ** (num_stat - 1)
                            print(f"{me} landed on {place} and paid {rent} to {owner}")

                            
                        elif place in dict_by_color["utility"]:       # bills on utilities
                            num_uti = len(player.owned["utility"])
                            dice1 = random.randint(1, 6)
                            dice2 = random.randint(1, 6)
                            print(f"{self.name} rolled {dice1} and {dice2}")    # roll the dice
                            rent = (dice1 + dice2) * (6 * num_uti - 2)
                            print(f"{me} landed on {place} and paid {rent} to {owner}")

                        else:                                       # bills for normal prop
                            num_houses = board.prop_dict[place][1]
                            rent = properties[place]["rent"][num_houses]
                            print(f"{me} landed on {place} and paid {rent} to {owner}")
                            
                        self.balance -= rent
                        player.balance += rent
                    break   
            
        def check_if_pass_go(self, dice1, dice2):
            if dice1 + dice2 + self.position >= 40:
                self.balance += 200
                print(f"{self.name} passed Start and received 200 from the bank")

        def houses(self):    
            for color, ls_color in list(self.owned.items())[:-2]:
                if len(ls_color) == len(dict_by_color[color]):
                    print(f'HOUSES BUILDING in {color}:')
                    for ele in ls_color:
                        condition_budget = (self.balance - properties[ele]["house_cost"] > 400)
                        condition_num_prop = (board.prop_dict[ele][1] < 5)
                        if condition_budget and condition_num_prop:
                            self.balance -= properties[ele]["house_cost"]
                            board.new_house(ele)
                            print(f'    A new house was built in {ele} by {self.name}')
                        else:
                            print(f'    Not enough money or limit of houses reached (houses on this place: {board.prop_dict[ele][1]})')      
            
        def end_turn(self):
            board.next_turn()
            print(f"{self.name} ended his turn (balance = {self.balance})\n")

    players = [Player(f"Player {i}") for i in range(num_pl)]    # initialize the players
    for pl in players:  # assign a token to each player's name
        pl.name = board.monopoly_tokens.pop(random.randint(0, len(board.monopoly_tokens) - 1))

    board.players = players  # initialize the board with the players

    return board, TestArray

# Function that prints out the properties owned by each player
def print_player_properties(players):
    for player in players:
        print(f"\n{player.name}'s properties:")
        for color, properties in player.owned.items():
            if properties:
                print(f"  {color.capitalize()}: {', '.join(properties)}")

# Function that prints out the board
def print_board(board):
    for player in board.players:
        print(f"\n{player.name}: \n  Balance: {player.balance}")

# function that runs the game for N_turns turns
def game_engine(num_pl, ROI_type):
    board, TestArray = init_player(num_pl, ROI_type)
    print(f"\nGame started with {num_pl} players")
    print(f"ROI type: {ROI_type}\n")
    print("---------------------- START ----------------------")
    print_board(board)
    while len(board.players) != 1:      # when just one player is left the game ends
        for player in board.players:
            player.turn()
            player.end_turn()

        print('-------------- BALANCE --------------')
        print_board(board)
        print('\n-------------- PROPERTIES --------------')
        print_player_properties(board.players)
        
        board.check_inflation()
        if board.total_money > board.max_cash:
            print('\n********* G A M E   O V E R *********\n')
            print("Max cash reached. Bank has no funds anymore...\nThe richest player wins!")
            board.whos_winner()
            print('SUMMARY REPORT (property: [owner, n_houses]):\n')
            for i in board.prop_dict:
                print(f'{i}: {board.prop_dict[i]}')
            return TestArray
        print('\n-------------- END ROUND --------------')
    
    print('\n********* G A M E   O V E R *********\n')
    winner = board.players[0]
    turn = board.turn

    print(f"{winner.name} wins the game at turn {turn}, with a final MONOPOLY of {winner.balance} $")
    print('\nSUMMARY REPORT (property: [owner, n_houses]):\n')
    for i in board.prop_dict:
        print(f'{i}: {board.prop_dict[i]}')
    print('\nEND RESUME')

    return TestArray

def run_game(num_pl, ROI_type="random", output_to_file=True):
    if output_to_file:
        print(f'Report inside file "output_{ROI_type}.txt"')
        print("\nRESUME OF THE GAME:")
        game_over = '********* G A M E   O V E R *********'

        vfn.print_resume(f'output_{ROI_type}.txt', game_over, 'END RESUME')
        with open(f"output_{ROI_type}.txt", "w", encoding="utf-8") as f:
            original_stdout = sys.stdout  # Save the original value of sys.stdout
            sys.stdout = f
            try:
                TestArray = game_engine(num_pl, ROI_type)
            finally:
                sys.stdout = original_stdout  # Restore sys.stdout to its original value
    else:
        print('Report on screen')
        TestArray = game_engine(num_pl, ROI_type)

    print("Game simulation SUCCESSFULL!\n")
    roi_values = np.array(TestArray)
    return roi_values


def random_dist(roi_values):
    print("***** RANDOM ROI FUNCTION *****")

    print(f"\nMean ROI: {np.mean(roi_values):.2f}")
    print(f"Median ROI: {np.median(roi_values):.2f}")

    print(f"\nMinimum ROI: {np.min(roi_values):.2f}")
    print(f"Maximum ROI: {np.max(roi_values):.2f}")
    print(f"How many over 0.5 ROI: {len(roi_values[roi_values > 0.5]) / len(roi_values) * 100:.2f} %")
    print(f"Dimension of the ROI array: {len(roi_values)}")

    # Plot the distribution of ROI values
    fig, ax = plt.subplots(figsize=(10, 5))  
    ax.hist(roi_values, bins=10, edgecolor='k', alpha=0.7, density=True, label='Normalised histogram of ROI')
    ax.hlines(1, 0, 1, color='orange', label='Expected uniform distribution', linestyles='--')
    ax.fill_between(np.linspace(0, 1, 100), 1, alpha=0.2, color='orange')
    ax.vlines(0.5, 0, 2, color='red', label='Threshold for buying', linestyles='--')

    ax.set_title('Distribution of ROI Values')
    ax.set_xlabel('ROI')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.grid(True, alpha=0.4)

    plt.show()


def color_dist(roi_values):
    print("***** COLOR ROI FUNCTION *****")

    print(f"\nMean ROI: {np.mean(roi_values):.2f}")
    print(f"Median ROI: {np.median(roi_values):.2f}")

    print(f"\nMinimum ROI: {np.min(roi_values):.2f}")
    print(f"Maximum ROI: {np.max(roi_values):.2f}")
    print(f"How many over 0.2 ROI: {len(roi_values[roi_values > 0.2]) / len(roi_values) * 100:.2f} %")
    print(f"Dimension of the ROI array: {len(roi_values)}")

    # Plot the distribution of ROI values
    fig, ax = plt.subplots(figsize=(10, 5))  
    ax.hist(roi_values, bins=10, edgecolor='k', alpha=0.7, label='Distribution of ROI')
    ax.vlines(0.2, 0, 100, color='red', label='Threshold for buying', linestyles='--')
    ax.set_title('Distribution of ROI Values')
    ax.set_xlabel('ROI')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.grid(True, alpha=0.4)

    plt.show()

