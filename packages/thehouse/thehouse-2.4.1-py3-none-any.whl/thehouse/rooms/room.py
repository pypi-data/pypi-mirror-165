"""Room blueprint."""
from thehouse.helpers import print_pause, validate_input


class Room:
    """Room blueprint."""

    def __init__(self, player, thehouse):
        """Initialize the class.

        :param player: the instantiated Player class.
        :param thehouse: the instantiated TheHouse class.
        """
        self.player = player
        self.thehouse = thehouse

    def blueprint(self) -> None:
        """Print all sides of the room.

        This method will be called if user type "help".
        """
        pass

    def right(self) -> None:
        """Print content of the right side of the room."""
        pass

    def left(self) -> None:
        """Print content of the left side of the room."""
        pass

    def backward(self) -> None:
        """Print content of the back side of the room."""
        pass

    def forward(self):
        """Print content of the front side of the room."""
        pass

    def move(self) -> None:
        """Let the user move inside or outside the room."""
        print_pause("Where do you want to go?")

        choice = validate_input(
            'Type "forward", "right", "backward", "left", "help", "items": ',
            ["right", "left", "forward", "backward", "help", "items"],
        )

        if choice == "right":
            self.right()
        elif choice == "left":
            self.left()
        elif choice == "backward":
            self.backward()
        elif choice == "forward":
            self.forward()
        elif choice == "help":
            self.blueprint()
        elif choice == "items":
            self.player.print_items()
            self.move()
