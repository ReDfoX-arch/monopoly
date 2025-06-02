import numpy as np
import matplotlib.pyplot as plt
from prop_and_loc import properties, prop_list
import os
import sys

# Define colors for each property type
color_map = {
    "brown": "saddlebrown",
    "light blue": "deepskyblue",
    "pink": "hotpink",
    "orange": "darkorange",
    "red": "red",
    "yellow": "yellow",
    "green": "green",
    "blue": "blue",
    "railroad": "black",
    "utility": "purple",
    "default": "black"
}

# Function to get color based on property type
def get_color(property_name):
    if property_name in properties:
        color = properties[property_name]["color"]
        return color_map.get(color, color_map["default"])
    return color_map["default"]
    # Update property names with colored labels
colored_prop_list = [f"\033[38;5;{get_color(prop)}m{prop}\033[0m" for prop in prop_list]

class analiser:
    def __init__(self, num_sim: int, num_players: int, mc, ROI_type: str, save=True, single=True):
        self.num_sim = num_sim
        self.num_players = num_players
        self.ROI_type = ROI_type
        self.save = save
        self.datapack = mc
        self.single = single
        
        self.game_lenght = mc[0]
        self.final_budget = mc[1]
        self.over_cashed = mc[2]
        self.loc_visits = mc[3]
        self.house_visits = mc[4]
        self.gain4prop = mc[5]
        self.gain4color = mc[6]
    
    def save_plot(self, plt, filename):
        if self.single:
            directory = os.path.join(f"{self.ROI_type}", "single", f"{self.num_players}_pl")
            if not os.path.exists(directory):
                os.makedirs(directory)
            plt.savefig(os.path.join(directory, f"{filename}_{self.num_players}_players.png"), bbox_inches='tight')
            plt.close()
        
        else:
            directory = os.path.join(f"{self.ROI_type}", "var", filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
            plt.savefig(os.path.join(directory, f"{filename}_{self.num_players}_players.png"), bbox_inches='tight')
            plt.close()

        if not self.save:
            plt.show()

    def lenght(self):
        print(f"Average game lenght: {np.mean(self.game_lenght):.2f} +/- {np.std(self.game_lenght):.2f}")
        print(f"Median game lenght: {np.median(self.game_lenght)}")
        print(f"Mode game lenght: {max(set(self.game_lenght), key=self.game_lenght.count)}")
        print(f"Max game lenght: {max(self.game_lenght)}")
        print(f"Min game lenght: {min(self.game_lenght)}\n")

        plt.hist(self.game_lenght, bins=15)
        plt.title(f"Game Lenght ({self.num_sim} sims, {self.num_players} players)")
        plt.grid(alpha=0.4)
        self.save_plot(plt, "game_lenght")

    def budget(self):
        print(f"Average final budget: {np.mean(self.final_budget):.2f} +/- {np.std(self.final_budget):.2f}")
        print(f"Median final budget: {np.median(self.final_budget)}")
        print(f"Mode final budget: {max(set(self.final_budget), key=self.final_budget.count)}")
        print(f"Max final budget: {max(self.final_budget)}")
        print(f"Min final budget: {min(self.final_budget)}\n")     
        
        plt.hist(self.final_budget, bins=15)
        plt.title(f"Final Budget ({self.num_sim} sims, {self.num_players} players)")
        plt.grid(alpha=0.4)
        self.save_plot(plt, "final_budget")
            
    def over(self):
        num_sim = self.num_sim
        data = self.over_cashed

        print(f"Over Cashed (bank finishes available cash): {np.count_nonzero(data) / num_sim * 100:.2f} %")

        over_np = np.array(data)
        num_true = np.count_nonzero(over_np)  # Count True values
        num_false = self.num_sim - num_true  # Remaining False values

        # Create dictionary
        over_dict = {True: num_true, False: num_false}

        # Define colors
        colors = ['lightcoral', 'lightskyblue']

        # Fake 3D effect using shadow and an elevated explode
        explode = (0.1, 0)  # Separate True slightly for 3D effect

        plt.figure(figsize=(7, 5))
        plt.pie(
            over_dict.values(), labels=over_dict.keys(), autopct='%1.2f%%',
            startangle=140, colors=colors, explode=explode, shadow=True
        )
        plt.title(f"Over Cashed ({num_sim} sims, {self.num_players} players)")
        self.save_plot(plt, "over_cashed")

    def visits(self):
        data = self.loc_visits
        num_sim = self.num_sim

        print(f"Average visits per location: {np.mean(list(data.values())) / num_sim:.2f} +/- {np.std(list(data.values())) / num_sim:.2f}")

        loc_keys = []
        loc_visits = []
        for key, value in data.items():
            loc_keys.append(key)
            loc_visits.append(value/num_sim)

        # Define margins (e.g., 30% above max and 30% below min)
        margin = 0.3
        y_min = min(loc_visits)
        y_max = max(loc_visits)

        y_range = y_max - y_min  # Compute range
        y_lower = max(0, y_min - margin * y_range)  # Ensure lower bound is not negative
        y_upper = y_max + margin * y_range

        # Plot with adjusted limits
        plt.figure(figsize=(10, 4))
        plt.bar(loc_keys, loc_visits, color=[get_color(key) for key in loc_keys])
        plt.hlines(np.mean(loc_visits), -1, len(loc_keys), colors="red", linestyles="dashed", alpha=0.7, label="Mean")
        plt.xticks(rotation=85)

        plt.ylim(y_lower, y_upper)  # Set the focus range
        plt.legend()
        plt.title(f"Locations Visits per Game ({num_sim} sims, {self.num_players} players)")
        self.save_plot(plt, "locations_visits")

    def visits_sort(self):
        data = self.loc_visits
        num_sim = self.num_sim

        loc_keys = []
        loc_visits = []
        for key, value in data.items():
            loc_keys.append(key)
            loc_visits.append(value/num_sim)

        # Sort data in descending order
        loc_keys, loc_visits = zip(*sorted(zip(loc_keys, loc_visits), key=lambda x: x[1], reverse=True))

        # Define margins (e.g., 30% above max and 30% below min)
        margin = 0.3
        y_min = min(loc_visits)
        y_max = max(loc_visits)

        y_range = y_max - y_min  # Compute range
        y_lower = max(0, y_min - margin * y_range)  # Ensure lower bound is not negative
        y_upper = y_max + margin * y_range

        # Plot with adjusted limits
        plt.figure(figsize=(10, 4))
        plt.bar(loc_keys, loc_visits, color=[get_color(key) for key in loc_keys])
        plt.hlines(np.mean(loc_visits), -1, len(loc_keys), colors="red", linestyles="dashed", alpha=0.7, label="Mean")
        plt.xticks(rotation=85)

        plt.ylim(y_lower, y_upper)  # Set the focus range
        plt.legend()
        plt.title(f"SORTED Locations Visits per Game ({num_sim} sims, {self.num_players} players)")
        self.save_plot(plt, "sorted_locations_visits")

    def house(self):
        data = self.house_visits
        num_sim = self.num_sim
        non_zero_values = [value for value in data.values() if value > 0]
        print(f"Average houses per location (excluding zeros): {np.mean(non_zero_values) / num_sim:.2f} +/- {np.std(non_zero_values) / num_sim:.2f}")

        house_keys = []
        house_visits = []
        for key, value in data.items():
            house_keys.append(key)
            house_visits.append(value/num_sim)

        # Sort data in descending order
        house_keys, house_visits = zip(*sorted(zip(house_keys, house_visits), key=lambda x: x[1], reverse=True))

        # Define margins (e.g., 30% above max and 30% below min)
        margin = 0.3
        y_min = min(house_visits)
        y_max = max(house_visits)

        y_range = y_max - y_min  # Compute range
        y_lower = max(0, y_min - margin * y_range)  # Ensure lower bound is not negative
        y_upper = y_max + margin * y_range

        # Plot with adjusted limits
        plt.figure(figsize=(10, 4))
        plt.bar(house_keys, house_visits, color=[get_color(key) for key in house_keys])
        non_zero_house_visits = [value for value in house_visits if value > 0]
        plt.hlines(np.mean(non_zero_house_visits), -1, len(house_keys), colors="red", linestyles="dashed", alpha=0.7, label="Mean (excluding zeros)")
        plt.xticks(rotation=85)

        plt.ylim(y_lower, y_upper)  # Set the focus range
        plt.legend()
        plt.title(f"Houses per Game ({num_sim} sims, {self.num_players} players)")
        self.save_plot(plt, "houses_per_game")

    def gain_prop(self): 
        data = self.gain4prop
        num_sim = self.num_sim

        print(f"Average gain per property: {np.mean(list(data.values())) / num_sim:.2f} +/- {np.std(list(data.values())) / num_sim:.2f}")

        prop_keys = []
        prop_visits = []
        for key, value in data.items():
            prop_keys.append(key)
            prop_visits.append(value/num_sim)

        # Sort data in descending order
        prop_keys, prop_visits = zip(*sorted(zip(prop_keys, prop_visits), key=lambda x: x[1], reverse=True))

        # Define margins (e.g., 30% above max and 30% below min)
        margin = 0.3
        y_min = min(prop_visits)
        y_max = max(prop_visits)

        y_range = y_max - y_min  # Compute range
        y_lower = max(0, y_min - margin * y_range)  # Ensure lower bound is not negative
        y_upper = y_max + margin * y_range

        # Plot with adjusted limits
        plt.figure(figsize=(10, 4))
        plt.bar(prop_keys, prop_visits, color=[get_color(key) for key in prop_keys])
        plt.hlines(np.mean(prop_visits), -1, len(prop_keys), colors="red", linestyles="dashed", alpha=0.7, label="Mean")
        plt.xticks(rotation=85)

        plt.ylim(y_lower, y_upper)  # Set the focus range
        plt.legend()	
        plt.title(f"Gain for each Property ({num_sim} sims, {self.num_players} players)")
        self.save_plot(plt, "gain_per_property")

    def gain_color(self):
        data = self.gain4color
        num_sim = self.num_sim        
        
        print(f"Average gain per color: {np.mean(list(data.values())) / num_sim:.2f} +/- {np.std(list(data.values())) / num_sim:.2f}")

        color_keys = []
        color_visits = []
        for key, value in data.items():
            color_keys.append(key)
            color_visits.append(value/num_sim)

        # Sort data in descending order
        color_keys, color_visits = zip(*sorted(zip(color_keys, color_visits), key=lambda x: x[1], reverse=True))

        # Define margins (e.g., 30% above max and 30% below min)
        margin = 0.3
        y_min = min(color_visits)
        y_max = max(color_visits)

        y_range = y_max - y_min  # Compute range
        y_lower = max(0, y_min - margin * y_range)  # Ensure lower bound is not negative
        y_upper = y_max + margin * y_range

        # Plot with adjusted limits
        plt.figure(figsize=(10, 4))
        plt.bar(color_keys, color_visits, color=[color_map.get(key, color_map["default"]) for key in color_keys])
        plt.hlines(np.mean(color_visits), -1, len(color_keys), colors="red", linestyles="dashed", alpha=0.7, label="Mean")
        plt.xticks(rotation=85)

        plt.ylim(y_lower, y_upper)  # Set the focus range
        plt.legend()
        plt.title(f"Gain for each Color ({num_sim} sims, {self.num_players} players)")
        self.save_plot(plt, "gain_per_color")

    def complete_analysis (self):
        if self.save:
            file_name = f"GameResume_{self.ROI_type}_{self.num_players}pl.txt"
            an_type = "single" if self.single else "var"
            
            # folder path
            folder_path = os.path.join(self.ROI_type, an_type, f"{self.num_players}_pl") if self.single else os.path.join(self.ROI_type, an_type, "GameResume")
            address = os.path.join(folder_path, file_name)  # complete path of the file

            # create the folder if doesn't exist
            os.makedirs(folder_path, exist_ok=True)
            print(f'Report inside file "{address}"')

            with open(address, "w", encoding="utf-8") as f:
                original_stdout = sys.stdout  # Save the original value of sys.stdout
                sys.stdout = f
                try:
                    print(f"COMPLETE STATS ANALYSIS over {self.num_sim} simulations:\n")
                    self.lenght()
                    self.budget()
                    self.over()
                    self.house()
                    self.visits()
                    self.visits_sort()
                    self.gain_prop()
                    self.gain_color()
                finally:
                    sys.stdout = original_stdout  # Restore sys.stdout to its original value
