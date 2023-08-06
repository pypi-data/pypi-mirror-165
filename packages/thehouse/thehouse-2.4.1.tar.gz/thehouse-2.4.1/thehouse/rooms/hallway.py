"""Hallway.

Sides:
- FORWARD: the hall.
- RIGHT: door to the bedroom.
- BACKWARD: door to the studio.
- LEFT: door to the livingroom.
"""
from thehouse.helpers import print_pause, validate_input

from .room import Room


class Hallway(Room):
    """Hallway."""

    def __str__(self):
        """Return the name of the room."""
        return "Hallway"

    def blueprint(self) -> None:
        """Print the blueprint of the room."""
        print_pause("- In front of you there's the hall of the house.")
        print_pause("- On your right there's a little table and a door.")
        print_pause("- Behind you there's a door.")
        print_pause("- On your left there's a door and two paintings.")
        self.move()

    def center(self):
        """Print welcome message and blueprint."""
        print_pause("You are in the hallway.")
        self.blueprint()

    def backward(self):
        """Print content of the back side of the room."""
        studio = self.thehouse.rooms["studio"]

        if studio.door_locked or "PASSEPARTOUT" not in self.player.items:
            print_pause("The door is locked!")
            print_pause("It seems you have to find the key!")
            print_pause("You go back.")

            self.move()
        else:
            print_pause("You open the door and enter the room.")
            studio.center()

    def forward(self):
        """Move player to the hall."""
        self.thehouse.rooms["hall"].center()

    def right(self):
        """Move player to the bedroom."""
        if "PASSPARTOUT" not in self.player.items:
            print_pause("There's a little table and a door.")
            print_pause("Do you want to open the door or check the table?")

            choice = validate_input('Type "table" or "door": ', ["table", "door"])

            if choice == "door":
                print_pause("You open the door and enter the room.")
                self.thehouse.rooms["bedroom"].center()
            else:
                self.table()
        else:
            print_pause("You open the door and enter the room.")
            self.thehouse.rooms["bedroom"].center()

    def table(self):
        """Let the user check if there's something inside the table."""
        print_pause("You open the drawer and find but there's nothing inside.")
        print_pause("You go back.")
        self.move()

    def left(self):
        """Move player to the livingroom."""
        print_pause("You open the door and enter the room.")
        self.thehouse.rooms["livingroom"].center()
