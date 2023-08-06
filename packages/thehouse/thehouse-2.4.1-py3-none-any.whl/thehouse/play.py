"""This module is responsible of initializing the game."""
from thehouse.characters import Player
from thehouse.thehouse import TheHouse
from thehouse.helpers import validate_input, print_pause


def play():
    player = Player()
    game = TheHouse(player)

    game.play()

    print_pause("Do you want to play again?")
    choice = validate_input("Type yes or no: ", ["yes", "no"])

    if choice == "yes":
        play()
    else:
        quit()


if __name__ == "__main__":
    play()
