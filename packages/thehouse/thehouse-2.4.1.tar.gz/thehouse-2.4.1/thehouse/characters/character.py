"""Character blueprint."""
import random

from thehouse.helpers import print_pause


class Character:
    """Character blueprint."""

    def __init__(self):
        """Set max_health and health."""
        self.max_health = random.randint(5, 10)
        self.health = self.max_health

    @property
    def is_alive(self) -> bool:
        """Return whether the character is alive or not."""
        return True if self.health > 0 else False

    def lose_health(self, damage=1) -> None:
        """Take an amount of damage and substract it to health.

        :param damage: the amount of damage as integer the character takes.
        """
        self.health -= damage
        self.print_health()

    def restore_health(self) -> None:
        """Restore the health to the maximum health of the character."""
        self.health = self.max_health
        self.print_health()

    def print_health(self) -> None:
        """Print a bar with the current health."""
        health = "*" * self.health
        pt_lost = "-" * (self.max_health - self.health)
        print_pause(f"Health: {health}{pt_lost}")

    def print_items(self) -> None:
        """Print a list of items."""
        if not len(self.items):
            print_pause("Your pockets are empty!")
        else:
            for item in self.items:
                print_pause(f"- {item}")
