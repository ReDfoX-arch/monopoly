
locations = {   # this double dictionary has no sense, it could be enough one dict...
    "Start": {"type": "go"},
    "Vicolo Corto": {"type": "property"},
    "Probabilità 1": {"type": "chance"},
    "Vicolo Stretto": {"type": "property"},
    "Tassa patrimoniale": {"type": "tax"},
    "Stazione Sud": {"type": "railroad"},
    "Bastioni Gran Sasso": {"type": "property"},
    "Imprevisti 1": {"type": "community_chest"},
    "Viale Monterosa": {"type": "property"},
    "Viale Vesuvio": {"type": "property"},
    "Prigione/Transito": {"type": "jail"},
    "Via Accademia": {"type": "property"},
    "Società Elettrica": {"type": "utility"},
    "Corso Ateneo": {"type": "property"},
    "Piazza Università": {"type": "property"},
    "Stazione Ovest": {"type": "railroad"},
    "Via Verdi": {"type": "property"},
    "Probabilità 2": {"type": "chance"},
    "Corso Raffaello": {"type": "property"},
    "Piazza Dante": {"type": "property"},
    "Parcheggio gratuito": {"type": "free_parking"},
    "Via Marco Polo": {"type": "property"},
    "Imprevisti 2": {"type": "community_chest"},
    "Corso Magellano": {"type": "property"},
    "Largo Colombo": {"type": "property"},
    "Stazione Nord": {"type": "railroad"},
    "Viale Costantino": {"type": "property"},
    "Viale Traiano": {"type": "property"},
    "Società Acqua Potabile": {"type": "utility"},
    "Piazza Giulio Cesare": {"type": "property"},
    "Vai in prigione": {"type": "jail"},
    "Via Roma": {"type": "property"},
    "Corso Impero": {"type": "property"},
    "Probabilità 3": {"type": "chance"},
    "Largo Augusto": {"type": "property"},
    "Stazione Est": {"type": "railroad"},
    "Imprevisti 3": {"type": "community_chest"},
    "Viale dei Giardini": {"type": "property"},
    "Tassa di lusso": {"type": "tax"},
    "Parco della Vittoria": {"type": "property"}
}
properties = {
    "Vicolo Corto": {
        "color": "brown",
        "cost": 60,
        "rent": [2, 10, 30, 90, 160, 250],
        "house_cost": 10
    },
    "Vicolo Stretto": {
        "color": "brown",
        "cost": 60,
        "rent": [4, 20, 60, 180, 320, 450],
        "house_cost": 10
    },
    "Stazione Sud": {
        "color": "railroad",
        "cost": 200,
        "rent": [25, 50, 100, 200],
        "house_cost": None
    },
    "Bastioni Gran Sasso": {
        "color": "light blue",
        "cost": 100,
        "rent": [6, 30, 90, 270, 400, 550],
        "house_cost": 16
    },
    "Viale Monterosa": {
        "color": "light blue",
        "cost": 100,
        "rent": [6, 30, 90, 270, 400, 550],
        "house_cost": 16
    },
    "Viale Vesuvio": {
        "color": "light blue",
        "cost": 120,
        "rent": [8, 40, 100, 300, 450, 600],
        "house_cost": 20
    },
    "Via Accademia": {
        "color": "pink",
        "cost": 140,
        "rent": [10, 50, 150, 450, 625, 750],
        "house_cost": 23
    },
    "Società Elettrica": {
        "color": "utility",
        "cost": 150,
        "rent": [4, 10],
        "house_cost": None
    },
    "Corso Ateneo": {
        "color": "pink",
        "cost": 140,
        "rent": [10, 50, 150, 450, 625, 750],
        "house_cost": 23
    },
    "Piazza Università": {
        "color": "pink",
        "cost": 160,
        "rent": [12, 60, 180, 500, 700, 900],
        "house_cost": 26
    },
    "Stazione Ovest": {
        "color": "railroad",
        "cost": 200,
        "rent": [25, 50, 100, 200],
        "house_cost": None
    },
    "Via Verdi": {
        "color": "orange",
        "cost": 180,
        "rent": [14, 70, 200, 550, 750, 950],
        "house_cost": 30
    },
    "Corso Raffaello": {
        "color": "orange",
        "cost": 180,
        "rent": [14, 70, 200, 550, 750, 950],
        "house_cost": 30
    },
    "Piazza Dante": {
        "color": "orange",
        "cost": 200,
        "rent": [16, 80, 220, 600, 800, 1000],
        "house_cost": 33
    },
    "Via Marco Polo": {
        "color": "red",
        "cost": 220,
        "rent": [18, 90, 250, 700, 875, 1050],
        "house_cost": 36
    },
    "Corso Magellano": {
        "color": "red",
        "cost": 220,
        "rent": [18, 90, 250, 700, 875, 1050],
        "house_cost": 36
    },
    "Largo Colombo": {
        "color": "red",
        "cost": 240,
        "rent": [20, 100, 300, 750, 925, 1100],
        "house_cost": 40
    },
    "Stazione Nord": {
        "color": "railroad",
        "cost": 200,
        "rent": [25, 50, 100, 200],
        "house_cost": None
    },
    "Viale Costantino": {
        "color": "yellow",
        "cost": 260,
        "rent": [22, 110, 330, 800, 975, 1150],
        "house_cost": 43
    },
    "Viale Traiano": {
        "color": "yellow",
        "cost": 260,
        "rent": [22, 110, 330, 800, 975, 1150],
        "house_cost": 43
    },
    "Società Acqua Potabile": {
        "color": "utility",
        "cost": 150,
        "rent": [4, 10],
        "house_cost": None
    },
    "Piazza Giulio Cesare": {
        "color": "yellow",
        "cost": 280,
        "rent": [24, 120, 360, 850, 1025, 1200],
        "house_cost": 46
    },
    "Via Roma": {
        "color": "green",
        "cost": 300,
        "rent": [26, 130, 390, 900, 1100, 1275],
        "house_cost": 50
    },
    "Corso Impero": {
        "color": "green",
        "cost": 300,
        "rent": [26, 130, 390, 900, 1100, 1275],
        "house_cost": 50
    },
    "Largo Augusto": {
        "color": "green",
        "cost": 320,
        "rent": [28, 150, 450, 1000, 1200, 1400],
        "house_cost": 53
    },
    "Stazione Est": {
        "color": "railroad",
        "cost": 200,
        "rent": [25, 50, 100, 200],
        "house_cost": None
    },
    "Viale dei Giardini": {
        "color": "blue",
        "cost": 350,
        "rent": [35, 175, 500, 1100, 1300, 1500],
        "house_cost": 58
    },
    "Parco della Vittoria": {
        "color": "blue",
        "cost": 400,
        "rent": [50, 200, 600, 1400, 1700, 2000],
        "house_cost": 66
    }
}
# go to jail doesn't work anymore, it doesn't affect the game in a long period, it has become a normal location without effects

prop_list = list(properties.keys())
loc_list = list(locations.keys())

dict_by_color = {
    "brown": ["Vicolo Corto", "Vicolo Stretto"],
    "light blue": ["Bastioni Gran Sasso", "Viale Monterosa", "Viale Vesuvio"],
    "pink": ["Via Accademia", "Corso Ateneo", "Piazza Università"],
    "orange": ["Via Verdi", "Corso Raffaello", "Piazza Dante"],
    "red": ["Via Marco Polo", "Corso Magellano", "Largo Colombo"],
    "yellow": ["Viale Costantino", "Viale Traiano", "Piazza Giulio Cesare"],
    "green": ["Via Roma", "Corso Impero", "Largo Augusto"],
    "blue": ["Viale dei Giardini", "Parco della Vittoria"],
    "railroad": ["Stazione Sud", "Stazione Ovest", "Stazione Nord", "Stazione Est"],
    "utility": ["Società Elettrica", "Società Acqua Potabile"]
}

# escape from jail community card removed
community_chest_cards = [
    {"category": "pay", "effect": 100},
    {"category": "pay", "effect": -100},
    {"category": "pay", "effect": -50},
    {"category": "pay", "effect": 200},
    {"category": "pay", "effect": -10},
    {"category": "pay", "effect": 25},
    {"category": "pay", "effect": -25},
    {"category": "pay", "effect": 50},
    {"category": "pay", "effect": -150},
    {"category": "pay", "effect": 75},
    {"category": "pay", "effect": -75},
    {"category": "pay", "effect": 20},
    {"category": "pay", "effect": -20},
    {"category": "pay", "effect": +10},
    {"category": "pay", "effect": -10}
]
chance_cards = [
    {"category": "go", "effect": "Start"},
    {"category": "go", "effect": "Prigione/Transito"},
    {"category": "pay", "effect": -50},
    {"category": "pay", "effect": +50},
    {"category": "go", "effect": "Stazione Nord"},
    {"category": "go", "effect": "Viale Vesuvio"},
    {"category": "go", "effect": "Stazione Sud"},
    {"category": "go", "effect": "Parco della Vittoria"},
    {"category": "pay", "effect": -15},
    {"category": "pay", "effect": +100},
    {"category": "go", "effect": "Largo Augusto"},
    {"category": "go", "effect": "Vicolo Corto"},
    {"category": "pay", "effect": +50},
    {"category": "pay", "effect": -20},
    {"category": "go", "effect": "Corso Impero"},
    {"category": "go", "effect": "Piazza Università"}
]
