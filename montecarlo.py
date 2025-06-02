
# LIBRARIES
import numpy as np
import matplotlib.pyplot as plt
import various_func as vfn
import random
from prop_and_loc import loc_list, prop_list, dict_by_color, properties, locations, community_chest_cards, chance_cards

# CLASSES
# Class that represents the board
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
        self.players.remove(player)
        for color, props in player.owned.items():
            for prop in props:
                self.prop_dict[prop] = None
        # bye bye space cowboy ...    

    def check_inflation(self):
        self.total_money = 0    # Reset the total money amount and proceed to count if bank finished the cash available
        for player in self.players:
            self.total_money += player.balance
    
    def whos_winner(self):
        winner = None
        balance = 0
        for player in self.players:
            new_bal = player.balance
            if  new_bal > balance:
                winner = player
                balance = new_bal
        return winner

# Function that initializes the players and the board, given the number of players
def init_player(num_pl, ROI_type):
    
    GameResume = {
        "game_lenght": 0,
        "final_budget": 0,
        "over_cashed": False,   # True if the game ends with a overflow of cash
        "properties_owned": [],    # when the player looses we register his props, so that the first element will be the list of all props from the winner
        "locations_visited": {key: 0 for key in loc_list},
        "houses": {key: 0 for key in prop_list},
        "gain_4_prop": {key: 0 for key in prop_list},
        "gain_4_color": {key: 0 for key in dict_by_color.keys()}
    }
    board = Table (num_players=num_pl)  # initialize the board

    # Class that represents the player
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
            dice1 = random.randint(1, 6)        # draw phase
            dice2 = random.randint(1, 6)
            self.check_if_pass_go(dice1, dice2)     # check if the player passed go and assigns the money
            self.position = (self.position + (dice1 + dice2)) % 40  # update the position
            self.location = loc_list[self.position]     # update the location
            GameResume["locations_visited"][self.location] += 1
            self.prop_types()   # check the type of the location and apply the effects
            self.houses()       # check if we want to build some houses for our props
            if self.balance < 0:
                board.kill_player(self)
                dead_prop = []
                for color, props in self.owned.items():
                    for prop in props:
                        dead_prop.append(prop)
                GameResume["properties_owned"].append(dead_prop)
                # GAME OVER

        def prop_types(self):
            loc_type = locations[self.location]["type"]
            
            if loc_type in ["go", "free_parking", "jail"]:          # locations without effects
                pass
            elif loc_type == "tax":                                 # tax location
                self.balance -= 150         # average tax amount
            elif loc_type in ["community_chest", "chance"]:         # community chest or chance location
                if loc_type == "community_chest":
                    card = random.choice(community_chest_cards)  # returns a random card
                else:
                    card = random.choice(chance_cards)  # returns a random card
                
                if card["category"] == "pay":
                    self.balance += card["effect"]
                elif card["category"] == "go":
                    self.location = card["effect"]  
                    self.prop_types()  

            elif board.prop_dict[self.location] != None:            # property location owned by someone
                self.pay()
            elif board.prop_dict[self.location] == None:            # property location free to buy
                self.buy()
            
        def buy(self):
            if self.balance - properties[self.location]["cost"] < 200:     # we want to be safe, keeping at least 250 $ before making an investment
                pass
            else:
                if ROI_type == "random":
                    expect_ROI = vfn.random_ROI()
                    if expect_ROI > 0.5:      # if the expected ROI is greater than 1, buy the property
                        self.balance -= properties[self.location]["cost"]
                        self.owned[properties[self.location]["color"]].append(self.location)
                        board.prop_dict[self.location] = [self.name, 0]

                elif ROI_type == "simple":
                    expect_ROI = vfn.simple_ROI(self)
                    if expect_ROI > 0.5:
                        self.balance -= properties[self.location]["cost"]
                        self.owned[properties[self.location]["color"]].append(self.location)
                        board.prop_dict[self.location] = [self.name, 0]
                
                
                elif ROI_type == "complex":
                    expect_ROI = vfn.ROI(self, num_pl, board.turn)
                    if expect_ROI > 0.5:
                        self.balance -= properties[self.location]["cost"]
                        self.owned[properties[self.location]["color"]].append(self.location)
                        board.prop_dict[self.location] = [self.name, 0]

                elif ROI_type == "color":
                    expect_ROI = vfn.color_ROI(self, board)
                    if expect_ROI > 0.2:
                        self.balance -= properties[self.location]["cost"]
                        self.owned[properties[self.location]["color"]].append(self.location)
                        board.prop_dict[self.location] = [self.name, 0]

                else:
                    pass
        
        def pay(self):
            place = self.location
            owner = board.prop_dict[place][0] 
            me = self.name
            for player in board.players:
                if player.name == owner:
                    if place in self.owned[properties[place]["color"]]:
                        pass

                    else:
                        if place in dict_by_color["railroad"]:      # bills on railroad
                            num_stat = len(player.owned["railroad"])
                            rent = 25 * 2 ** (num_stat - 1)
                            
                        elif place in dict_by_color["utility"]:       # bills on utilities
                            num_uti = len(player.owned["utility"])
                            dice1 = random.randint(1, 6)
                            dice2 = random.randint(1, 6)
                            rent = (dice1 + dice2) * (6 * num_uti - 2)

                        else:                                       # bills for normal prop
                            num_houses = board.prop_dict[place][1]
                            rent = properties[place]["rent"][num_houses]
                        
                        # print(place, ': ',  rent)     # if interested in registering each transaction in the game
                        GameResume["gain_4_prop"][place] += rent
                        self.balance -= rent
                        player.balance += rent
                    break
            
        def check_if_pass_go(self, dice1, dice2):
            if dice1 + dice2 + self.position >= 40:
                self.balance += 200

        def houses(self):    
            for color, ls_color in list(self.owned.items())[:-2]:
                if len(ls_color) == len(dict_by_color[color]):
                    for ele in ls_color:
                        condition_budget = (self.balance - properties[ele]["house_cost"] > 400)
                        condition_num_prop = (board.prop_dict[ele][1] < 5)
                        if condition_budget and condition_num_prop:
                            self.balance -= properties[ele]["house_cost"]
                            board.new_house(ele)
                            GameResume["houses"][ele] += 1
                                    
        def end_turn(self):
            board.next_turn()

    players = [Player(f"Player {i}") for i in range(num_pl)]    # initialize the players
    for pl in players:  # assign a token to each player's name
        pl.name = board.monopoly_tokens.pop(random.randint(0, len(board.monopoly_tokens) - 1))

    board.players = players  # initialize the board with the players

    return board, GameResume

# function that runs the game for N_turns turns
def toy_exp(num_pl, ROI_type = "random"):
    board, GameResume = init_player(num_pl, ROI_type)
    # print(f"Game started with {num_pl} players")
    # print(f"ROI type: {ROI_type}")

    while len(board.players) != 1:      # when just one player is left the game ends
        for player in board.players:
            player.turn()
            player.end_turn()

        board.check_inflation()
        if board.total_money > board.max_cash:
            winner = board.whos_winner()
            GameResume["game_lenght"] = board.turn
            GameResume["final_budget"] = winner.balance
            for player in board.players:
                dead_prop = []
                for color, props in player.owned.items():
                    for prop in props:
                        dead_prop.append(prop)
                GameResume["properties_owned"].append(dead_prop)
            # print("\nMax Cash reached. Bank has no funds anymore...\nThe richest player wins!")
            # print(f"\n{winner.name} wins the game at turn {board.turn}, with a final MONOPOLY of {winner.balance} $\n")
            GameResume["over_cashed"] = True
            for color, props in dict_by_color.items():
                for prop in props:
                    GameResume["gain_4_color"][properties[prop]["color"]] += GameResume["gain_4_prop"][prop]
            
            return GameResume
    
    winner = board.players[0]
    turn = board.turn

    winner_prop = []
    for color, props in winner.owned.items():
        for prop in props:
            winner_prop.append(prop)
    GameResume["properties_owned"].append(winner_prop)
    GameResume["game_lenght"] = turn
    GameResume["final_budget"] = winner.balance
    for color, props in dict_by_color.items():
        for prop in props:
            GameResume["gain_4_color"][properties[prop]["color"]] += GameResume["gain_4_prop"][prop]
            
    # print(f"\n{winner.name} wins the game at turn {turn}, with a final MONOPOLY of {winner.balance} $\n")
    return GameResume

# Function that runs the game for N_turns turns
def montecarlo_run(num_sim, num_player, ROI_type = "random"):
    game_lenght = []
    final_budget = []
    over_cashed = []
    locations_visited = {key: 0 for key in loc_list}
    houses = {key: 0 for key in prop_list}
    gain_4_prop = {key: 0 for key in prop_list}
    gain_4_color = {key: 0 for key in dict_by_color.keys()}

    for i in range(num_sim):
        resume = toy_exp(num_player, ROI_type)

        game_lenght.append(resume["game_lenght"])
        final_budget.append(resume["final_budget"])
        over_cashed.append(resume["over_cashed"])
        for key, value in resume["locations_visited"].items():
            locations_visited[key] += value
        for key, value in resume["houses"].items():
            houses[key] += value
        for key, value in resume["gain_4_prop"].items():
            gain_4_prop[key] += value
        for key, value in resume["gain_4_color"].items():
            gain_4_color[key] += value

    return (game_lenght, final_budget, over_cashed, locations_visited, houses, gain_4_prop, gain_4_color)

