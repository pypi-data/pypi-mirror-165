"""Player."""
from thehouse.helpers.print_pause import print_pause
from .character import Character


class Player(Character):
    """Player.

    This class create a concrete player.
    """

    def __init__(self):
        """Inizialize escaped and items."""
        super().__init__()
        self.escaped = False
        self.items = []

    def __str__(self) -> str:
        """Return a the health of the character."""
        return f"Player - health: {self.health}; escaped {self.escaped}"

    def __contains__(self, item) -> bool:
        """Return whether an item is in the items list.

        :param item: in item to check.
        """
        return item in self.items

    def escape_the_house(self) -> None:
        """Let the Player escape the house."""
        self.escaped = True

    def pick_an_item(self, item) -> None:
        """Pick an item and append it to the list.

        :param item: an item as a string.
        """
        self.items.append(item)
        print_pause(f"You pick {item}!")
