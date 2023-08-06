"""Diningroom.

Sides:
- FORWARD: corpse.
- RIGHT: corpse.
- BACK: corpse.
- LEFT: door to hall.
"""
import random

from thehouse.helpers import print_pause

from .room import Room


class Diningroom(Room):
    """Diningroom."""

    def __init__(self, player, thehouse):
        """Initialize class.

        :param player: the instantiated Player class.
        :param thehouse: the instantiated TheHouse class.
        """
        super().__init__(player, thehouse)
        self.key_in_corpse = random.choice(["forward", "left", "backward"])

    def __str__(self):
        """Return the name of the room."""
        return "Diningroom"

    def blueprint(self) -> None:
        """Print the blueprint of the room."""
        print_pause("- Forward there's a corpse!")
        print_pause("- On your right there's another corpse!")
        print_pause("- On your back there's a third corpse!")
        print_pause("- On your left there's a door.")
        self.move()

    def center(self):
        """Print a welcome message."""
        print_pause("You're in the diningroom!")
        print_pause("There's a bloody mess here...")
        print_pause("Someone or something has killed three poeple!")
        self.blueprint()

    def forward(self):
        """Describe the corpse."""
        print_pause("Something has smashed its head!")
        print_pause("There's a lot of blood and a strange material on the corpse")
        print_pause("You check its pockets")

        if self.key_in_corpse == "forward":
            if "THE HOUSE KEY 2" in self.player.items:
                print_pause("You already checked its pocket and found a key!")
                print_pause("You go back!")
            else:
                print_pause("You have found a key!")
                self.player.pick_an_item("THE HOUSE KEY 2")
        else:
            print_pause("There's nothing inside its pocket. You go back.")

        self.move()

    def right(self):
        """Describe the corpse."""
        print_pause("Something has ripped its arms off!")
        print_pause("You check its pocket")

        if self.key_in_corpse == "left":
            if "THE HOUSE KEY 2" in self.player.items:
                print_pause("You already checked its pocket and found a key!")
                print_pause("You go back!")
            else:
                print_pause("You have found a key!")
                self.player.pick_an_item("THE HOUSE KEY 2")
        else:
            print_pause("There's nothing inside its pocket. You go back.")

        self.move()

    def backward(self):
        """Describe the corpse."""
        print_pause("There's a huge hole inside the chest of the corpse.")
        print_pause("Something has ripped its heart off!")
        print_pause("You check its pocket")

        if self.key_in_corpse == "backward":
            if "THE HOUSE KEY 2" in self.player.items:
                print_pause("You already checked its pocket and found a key!")
                print_pause("You go back!")
            else:
                print_pause("You have found a key!")
                self.player.pick_an_item("THE HOUSE KEY 2")
        else:
            print_pause("There's nothing inside its pocket. You go back.")

        self.move()

    def left(self):
        """Move player towards the hall."""
        print_pause("You open the door and enter the room.")
        self.thehouse.rooms["hall"].center()
