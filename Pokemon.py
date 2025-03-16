
import random
import ast
import pandas as pd
from collections import deque


class Move:
    def __init__(self, name, move_type, power):
        self.name = name
        self.move_type = move_type
        self.power = power
        self.used = False
        self.moves = None
        

class Pokemon:
    def __init__(self):
        self.pokemon_df = pd.read_csv("pokemon-data.csv")
        self.moves_df = pd.read_csv("moves-data.csv")
        self.player_pokemon = deque()
        self.teamRocket_pokemon = deque()
        self.player_hp = None
        self.rocketTeam_hp = None
        self.moves = None

        

    def makePokemonTeam(self, player_name):
        pokemon_list = self.pokemon_df.to_dict('records')  
        
        teamRocket_list = random.sample(pokemon_list, 3)  
        player_list = random.sample([p for p in pokemon_list if p not in self.teamRocket_pokemon], 3) 
        for p in teamRocket_list:
            self.teamRocket_pokemon.append(p)
        
        for p in player_list:
            self.player_pokemon.append(p)
        print("")    
        print("Team Rocket Team enters with", [p["Name"] for p in self.teamRocket_pokemon])
        print(f"Team {player_name} Team enters with", [p["Name"] for p in self.player_pokemon])

        
    def calculate_damage(self, move_power, move_type, attacker_type, defender_type, attack_power, defense_power):
        group_table = {
        'Normal': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1},
        'Fire': {'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 1, 'Grass': 2},
        'Water': {'Normal': 1, 'Fire': 2, 'Water': 0.5, 'Electric': 1, 'Grass': 0.5},
        'Electric': {'Normal': 1, 'Fire': 1, 'Water': 2, 'Electric': 0.5, 'Grass': 0.5},
        'Grass': {'Normal': 1, 'Fire': 0.5, 'Water': 2, 'Electric': 1, 'Grass': 0.5},
        'Others': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1}
        }
        stab = 1
        if move_type == attacker_type:
            stab = 1.5
        type_effectiveness = group_table[attacker_type][defender_type]

        random_factor = random.uniform(0.5, 1)  

        damage = (move_power * attack_power / defense_power) * stab * type_effectiveness * random_factor 
        return int(damage)
    
    def Player_Game(self, player_name):
        attacker = self.player_pokemon[0]
        attacker_name = attacker["Name"]
        attacker_type = attacker["Type"]
        attacker_attack = int(attacker["Attack"])

        if self.player_hp is None:
            self.player_hp = int(attacker["HP"])
            
        defender = self.teamRocket_pokemon[0]
        defender_name = defender["Name"]
        defender_type = defender["Type"]
        defender_defense = int(defender["Defense"])

        if self.rocketTeam_hp is None:
            self.rocketTeam_hp = int(defender["HP"])

        move_names = ast.literal_eval(attacker["Moves"])  
        print(type(move_names))
        available_moves = [
            move for move in move_names if move in self.moves_df["Name"].values
        ]

        if self.moves is None:
            self.moves = move_names

        print(f"Choose the move for {attacker_name}:")
        for i, move_name in enumerate(self.moves):
            print(f"{i + 1}. {move_name}")


        while True:
            try:
                print("")
                choice = int(input(f"Team {player_name}’s choice: ")) - 1
                if 0 <= choice < len(available_moves) and not " (N/A)" in self.moves[choice]:
                    selected_move_name = available_moves[choice]
                    break
                else:
                    print("Invalid choice! Please select again.")
            except ValueError:
                print("Invalid input. Enter a number.")
        
        self.moves[choice] = self.moves[choice]+" (N/A)"

        move_details = self.moves_df[self.moves_df["Name"] == selected_move_name].iloc[0]
        move_type = move_details["Type"]
        move_power = int(move_details["Power"])

        selected_move = Move(selected_move_name, move_type, move_power)

        damage = self.calculate_damage(move_power, move_type, attacker_type, defender_type, attacker_attack, defender_defense)

        # self.rocketTeam_hp -= damage
        # defender["HP"] = self.rocketTeam_hp  

        self.rocketTeam_hp = max(0, self.rocketTeam_hp - damage)
        defender["HP"] = self.rocketTeam_hp  


        print(f"{attacker_name} cast '{selected_move_name}' to {defender_name}:")
        print(f"Damage to {defender_name} is {damage} points.")
        print(f"Now {defender_name} has {defender['HP']} HP, and {attacker_name} has {attacker['HP']} HP.")
        print("")


        if self.rocketTeam_hp <= 0:
            print(f"{defender_name} fainted!")
            self.teamRocket_pokemon.popleft()
            if self.teamRocket_pokemon:
                self.rocketTeam_hp = int(self.teamRocket_pokemon[0]["HP"]) 
                print("")
                print(f"Next for Team Rocket, {self.teamRocket_pokemon[0]['Name']} enters battle!")
                print("")
            else:
                print(f"All of the Team Rocket's Pokermon fainted, and Team {player_name} prevails!")
                return True


        return False

    def TeamRocket_Game(self, player_name):
        attacker = self.teamRocket_pokemon[0]
        attacker_name = attacker["Name"]
        attacker_type = attacker["Type"]
        attacker_attack = int(attacker["Attack"])

        if self.rocketTeam_hp is None:
            self.rocketTeam_hp = int(attacker["HP"])
            
        defender = self.player_pokemon[0]
        defender_name = defender["Name"]
        defender_type = defender["Type"]
        defender_defense = int(defender["Defense"])

        if self.player_hp is None:
            self.player_hp = int(defender["HP"])

        move_names = ast.literal_eval(attacker["Moves"])  
        available_moves = [
            move for move in move_names if move in self.moves_df["Name"].values
        ]

        selected_move_name = random.choice(available_moves)
        move_details = self.moves_df[self.moves_df["Name"] == selected_move_name].iloc[0]
        move_type = move_details["Type"]
        move_power = int(move_details["Power"])

        selected_move = Move(selected_move_name, move_type, move_power)

        damage = self.calculate_damage(move_power, move_type, attacker_type, defender_type, attacker_attack, defender_defense)

        # self.player_hp -= damage
        # defender["HP"] = self.player_hp  

        self.player_hp = max(0, self.player_hp - damage)
        defender["HP"] = self.player_hp  


        print(f"Team Rocket's {attacker_name} cast '{selected_move_name}' on {defender_name}:")
        print(f"Damage to {defender_name} is {damage} points.")
        print(f"Now {defender_name} has {defender['HP']} HP, and {attacker_name} has {attacker['HP']} HP.")
        print("")


        if self.player_hp <= 0:
            print(f"{defender_name} fainted!")
            self.player_pokemon.popleft()
            self.moves = None
            if self.player_pokemon:
                self.player_hp = int(self.player_pokemon[0]["HP"])
                print("")
                print(f"Next for Team Rocket, {self.teamRocket_pokemon[0]['Name']} enters battle!")
                print("")
            else:
                print(f"All of {player_name}'s Pokemon fainted, and Team Rocket prevails!")
                return True


        return False

        
    