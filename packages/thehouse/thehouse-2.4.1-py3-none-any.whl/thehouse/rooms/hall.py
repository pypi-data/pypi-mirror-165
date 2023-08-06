"""HALL.

Sides:
- FORWARD: the main door of the house.
- RIGHT: door to the diningroom.
- BACKWARD: hallway.
- LEFT: kitchen.
"""
from thehouse.helpers import print_pause

from .room import Room


class Hall(Room):
    """Hall."""

    def __str__(self):
        """Return the name of the room."""
        return "Hall"

    def blueprint(self) -> None:
        """Print blueprint of the house."""
        print_pause("- In front of you there's the main door of the house.")
        print_pause("- On your right there's a door.")
        print_pause("- Backwards there's the hallway.")
        print_pause("- On your left there's another door.")
        self.move()

    def center(self):
        """Print welcome message."""
        print_pause("You're in the hall!")
        self.blueprint()

    def backward(self):
        """Move the player to the hallway."""
        self.thehouse.rooms["hallway"].center()

    def left(self):
        """Move the player to the kitchen."""
        print_pause("You open the door and enter the room.")
        self.thehouse.rooms["kitchen"].center()

    def right(self):
        """Move the player to the diningroom."""
        print_pause("You open the door and enter the room.")
        self.thehouse.rooms["diningroom"].center()

    def forward(self):
        """Move the player towards the main door of the house."""
        if (
            "THE HOUSE KEY 1" in self.player.items
            and "THE HOUSE KEY 2" in self.player.items
            and "THE HOUSE KEY 3" in self.player.items
        ):
            print_pause("You unlock the door and finally exit the house!")
            self.player.escaped = True
        else:
            print_pause("You need three keys to open the door!")
            print_pause("You go back.")

            self.move()
