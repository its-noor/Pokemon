
import random
from Pokemon import Pokemon



 
print("Welcome to Pokemon Colosseum!")
player_name = input("Enter Player Name: ")


# team_rocket, team_player = self.makePokemonTeam()
game = Pokemon()
teams = game.makePokemonTeam(player_name)

isPlayerTurn = False

print("")
print("Let the battle begine!")

randnum = random.randrange(0, 2)
if randnum == 1:
    print("Coin toss goes to ----- Team Rocket to start the attack!")
    print("")
    isPlayerTurn = False
else: 
    print(f"Coin toss goes to ----- Team {player_name} to start the attack!")
    print("")
    isPlayerTurn = True

GameOver = False

while not GameOver:

    if isPlayerTurn:
        GameOver = game.Player_Game(player_name)
    
    if not isPlayerTurn:
        GameOver = game.TeamRocket_Game(player_name)
    
    isPlayerTurn = not isPlayerTurn











  
        
 


