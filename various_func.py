
"""
This module contains various utility functions for a Monopoly game simulation.
These functions are designed to assist in making strategic
decisions during the game.

Functions:
- max_turn(num_pl): Calculates the maximum number of turns for a game based on the number of players.
- turn_posi(turn, position, num_pl): Evaluates the position of a player on the board relative to the turn.
- cost_development(prop): Calculates the cost of developing a property.
- calc_p_visit(prop): Calculates the probability of landing on a specific property.
- search_par_buy(self): Finds the parameters needed to evaluate the ROI of a property.

"""

# ***************************************************************************************************************

import numpy as np
import matplotlib.pyplot as plt
import os
from prop_and_loc import loc_list, prop_list, dict_by_color, properties, locations, community_chest_cards, chance_cards


# *****************************************************
#            FUNCTIONS FOR GENERAL PURPOSE
# *****************************************************

# def print_resume(txtFile):
def print_resume(file_path, start_text, end_text):
    with open(file_path, 'w+', encoding='utf-8') as file:
        inside_range = False
        for line in file:
            if start_text in line:
                inside_range = True
                continue  # Skip the line containing the start text
            if end_text in line and inside_range:
                break  # Stop reading when the end text is found
            if inside_range:
                print(line.strip())


# *****************************************************
#    FUNCTIONS TO EVALUATE IF BUY A PROPERTY OR NOT
# *****************************************************

# -------------------------------------------------------------

def max_turn (num_pl):
    return 60 * num_pl     # lenght of an average monoply game 

# -------------------------------------------------------------

# Define the parameter related to the turn for the calculation of the ROI
# using a two-dimensional function that represents a sheet folded along the diagonal with a maximum at (0,0)
# must be normalised related to the average lenght of a game (60 turns per player)
def calc_turn(turn, position, num_pl):
    return np.exp(-((turn / max_turn(num_pl)  - position / 40)**2) / 0.3) + 0.5
    
    # # Genero i valori di x e y
    # x = np.linspace(0, 240, 400)
    # y = np.linspace(0, 40, 400)
    # X, Y = np.meshgrid(x, y)
    # Z = calc_turn(X, Y, 2)

    # # Creo la figura e l'asse 3D
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # # Traccio la superficie
    # ax.plot_surface(X, Y, Z, cmap='viridis')

    # # Aggiungo etichette agli assi
    # ax.set_xlabel('Turn')
    # ax.set_ylabel('Position')
    # ax.set_zlabel('k turn') 

    # # Mostro il grafico
    # plt.show()

# -------------------------------------------------------------

# Evaluate the cost of developing a property
def cost_development(prop):
    if properties [prop]['house_cost'] is None:
        return 1  # if the property is a railroad or a utility, the cost of development is 1
    else:
        return properties [prop]['house_cost'] * 5 / 2000  # 4 case + 1 albergo

    # # Calcolo del cost development per ogni proprietà
    # for nome, prop in props.items():
    #     cost_development = calcola_cost_development(prop)
    #     print(f"{nome}: {cost_development}")

# -------------------------------------------------------------

# Evaluate the probability of landing on a specific property
def calc_p_visit(prop):
    # Adjust probability based on chance and community chest cards
    p_visit = 1 / 40  # base probability of landing on any given property
    for card in chance_cards + community_chest_cards:
        if card['category'] == 'go' and card['effect'] == prop:
            p_visit += 1 / len(chance_cards + community_chest_cards)
    return p_visit
    # loc_list = list(locations.keys())
    # for loc in loc_list:
    #     p_visit(loc)

# -------------------------------------------------------------

# Evaluate the coefficient about to the number of properties of the same color owned by the player
def k_col (selfie, prop):
    return len(selfie.owned[properties[prop]["color"]]) + 1

# -------------------------------------------------------------

# Evaluate the ROI of a property
def ROI (selfie, num_players, turn):
    """
    Assigns a value to evaluate the ROI of the property
    We decide if buy or not a prop in consequence of this value

    Returns:
        ROI (float) : Return on investment 
    """

    prop = selfie.location              # name of the property
    n_col = k_col(selfie, prop)         # coefficient related to the number of properties of the same color owned by the player
    cost = properties[prop]['cost']     # cost of the property
    rent = properties[prop]['rent'][0]  # rent of the property
    p_visit = calc_p_visit(prop)        # probability of landing on the property
    k_turn = calc_turn(turn/4, selfie.position, num_players)  # position of the player on the board
    cost_dev = cost_development(prop)   # cost of the further development on the property, derived from the need of building houses

    n_col, cost, rent, p_visit = (
        n_col / 3,
        cost / 400,
        rent / 50, 
        p_visit / 1, 
    )

    print(f'n_col: {n_col}, cost: {cost}, rent: {rent}, p_visit: {p_visit}, k_turn: {k_turn}, cost_dev: {cost_dev}')

    return (n_col * rent * p_visit / (cost + cost_dev) * k_turn) * 100

# -------------------------------------------------------------

# Evaluate the simplified ROI of a property
def simple_ROI(selfie):
    """
    Assigns a value to evaluate the ROI of the property
    We decide if buy or not a prop in consequence of this value

    Returns:
        ROI (float) : Return on investment 
    """

    prop = selfie.location    # name of the property
    n_col = k_col(selfie, prop)  # coefficient related to the number of properties of the same color owned by the player
    cost = properties[prop]['cost']  # cost of the property
    rent = properties[prop]['rent'][0]  # rent of the property
    cost_dev = cost_development(prop)   # cost of the further development on the property, derived from the need of building houses

    n_col, cost, rent = (
        n_col / 3,
        cost / 400,
        rent / 50, 
    )

    print(f'n_col: {n_col}, cost: {cost}, rent: {rent}')

    return (n_col * rent / (cost + cost_dev))

# -------------------------------------------------------------

def random_ROI():
    return np.random.rand()

# -------------------------------------------------------------

# Evaluate the ROI of a property based on the color of the property
# If the player owns other properties of the same color, the ROI is 1
# Otherwise, the ROI is random

def color_ROI(selfie, table):
    place = selfie.location
    num_color = len(selfie.owned[properties[place]["color"]])
    if num_color > 0:
        return 1
    else:
        for prop in dict_by_color[properties[place]["color"]]:
            if table.prop_dict[prop] is not None:
                return 0
        return random_ROI()

# *****************************************************

if __name__ == '__main__':
    pass

