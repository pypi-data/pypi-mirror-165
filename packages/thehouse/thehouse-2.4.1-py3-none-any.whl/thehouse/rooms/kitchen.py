"""Kitchen.

Sides:
- FORWARD: window
- RIGHT: door to the hall
- BACKWARD: drawers
- LEFT: drawers
"""
import random

from thehouse.helpers import print_pause, validate_input

from .room import Room


class Kitchen(Room):
    """Kitchen."""

    def __init__(self, player, thehouse):
        """Initialize class.

        :param player: the instantiated Player class.
        :param thehouse: the instantiated TheHouse class.
        """
        super().__init__(player, thehouse)
        self.knife_in_drawer = random.randint(1, 3)
        self.knife_on_wall = random.choice(["left", "backward"])

    def __str__(self):
        """Return the name of the room."""
        return "Kitchen"

    def blueprint(self) -> None:
        """Print the blueprint of the room."""
        print_pause("- In front of you there's a window")
        print_pause("- On your right there's a door.")
        print_pause("- Backwards there are some kitchen's drawers")
        print_pause("- On your left there are more kitchen's drawers")
        self.move()

    def center(self):
        """Print a welcome message."""
        print_pause("You're in the kitchen!")
        self.blueprint()

    def forward(self):
        """Print the content of the front side of the room."""
        print_pause("You look outside of the window.")
        print_pause("There's nothing to see...")
        print_pause("You go back.")
        self.move()

    def right(self):
        """Move the player to the hall."""
        self.thehouse.rooms["hall"].center()

    def left(self):
        """Show user the drawers."""
        print_pause("There are three drawers, you know you have to look into them all")
        print_pause("1. Open the first")
        print_pause("2. Open the second")
        print_pause("3. Open the third")

        self.pick_a_drawer("left")

    def backward(self):
        """Show user the drawers."""
        print_pause("There are three drawers, you know you have to look into them all")
        print_pause("1. Open the first")
        print_pause("2. Open the second")
        print_pause("3. Open the third")

        self.pick_a_drawer("backward")

    def pick_a_drawer(self, wall):
        """Let the user pick a drawer.

        :param wall: the wall where the knife is located.
        """
        choice = validate_input(
            "Type a number between 1 and 3 included, or back: ",
            ["1", "2", "3", "back"],
        )

        if choice == "back":
            print_pause("You go back to the center of the room.")
            self.move()
        else:
            print_pause("There's some tools, let's find something useful!")

            if wall == self.knife_on_wall and int(choice) == self.knife_in_drawer:
                if "knife" in self.player.items:
                    print_pause("You've already picked a KNIFE from this drawer!")
                    print_pause("There's nothing more in it.")
                else:
                    print_pause("You've found a KNIFE!")
                    self.player.pick_an_item("KNIFE")
            else:
                print_pause("There's nothing useful here...")

            self.pick_a_drawer(wall)
