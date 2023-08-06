"""Studio.

Sides:
- FORWARD: door to the hallway
- RIGHT: window
- BACKWARD: desk
- LEFT: shelf
"""


import random

from thehouse.helpers import print_pause, validate_input

from .room import Room


class Studio(Room):
    """Studio class."""

    def __init__(self, player, thehouse):
        """Initialize class.

        :param player: the instantiated Player class.
        :param thehouse: the instantiated TheHouse class.
        """
        super().__init__(player, thehouse)
        self.door_locked = True
        self.lights = random.choice([True, False])
        self.key_in_book = random.randint(1, 3)

    def __str__(self):
        """Return the name of the room."""
        return "Studio"

    def prompt_light(self):
        """Ask the user to turn the lights on."""
        switch_position = random.choice(["right", "left", "forward", "backward"])

        print_pause("You hear something lurking in the dark")
        print_pause("You defenetly want to turn the lights on.")
        print_pause("You extend your arms to:")
        print_pause("- forward")
        print_pause("- the right")
        print_pause("- backward")
        print_pause("- the left")

        while self.player.health > 0:
            choice = validate_input(
                'Type "forward", "right", "backward", "left": ',
                ["right", "left", "forward", "backward"],
            )

            if choice == switch_position:
                print_pause("You've turned the lights on!")
                break
            else:
                print_pause("There's nothing here!")
                print_pause(
                    "But you sense there's something that want to reach your hand..."
                )
                self.player.lose_health()

    def blueprint(self) -> None:
        """Print blueprint of the room."""
        print_pause("- In front of you there's a closed door.")
        print_pause("- On your right there's a window.")
        print_pause("- Behind you there's a desk with some papers on it.")
        print_pause("- On your left there's a shelf with many books on it.")

        self.move()

    def center(self) -> None:
        """Print center of the room."""
        lights = "on" if self.lights else "off"

        print_pause(f"You find yourself in a room with the lights {lights}")

        if not self.lights:
            self.prompt_light()

        if self.player.is_alive:
            print_pause("You're in the middle of a studio")
            self.blueprint()

    def right(self) -> None:
        """Print the content of the backward side."""
        print_pause("On your back there's a window.")
        print_pause("You have a glimpse outside but it's pitch black.")
        print_pause("You can't see anything interesting here.")
        print_pause("You go back.")
        self.move()

    def backward(self):
        """Print the content of the back side."""
        combination = self.thehouse.rooms["livingroom"].safe_combination

        """Print the content of the right side."""
        print_pause("The desk is so full of papers")
        print_pause("There's a note on the desk.")
        print_pause(f"It says: {combination}")
        print_pause("You go back.")
        self.move()

    def left(self):
        """Print the content of the left side."""
        print_pause("On your left there's a shelf full of books.")
        print_pause(
            "You run your finger through the dusty books "
            "and rapidly read the titles."
        )
        print_pause("There are so many books in this shelf.")
        print_pause("You wonder yourself if you've ever read this amount of books")

        self.pick_a_book()

    def book_divine_comedy(self):
        """Print content of the Divine Comedy book."""
        if self.key_in_book == 2 and ("THE STUDIO KEY" not in self.player.items):
            self.pick_the_key()
        else:
            print_pause("Amor, ch’a nullo amato amar perdona,")
            print_pause("mi prese del costui piacer sì forte,")
            print_pause("che, come vedi, ancor non m’abbandona")

    def book_the_king_in_yellow(self):
        """Print content of The King in Yellow book."""
        if self.key_in_book == 2 and ("THE STUDIO KEY" not in self.player.items):
            self.pick_the_key()
        else:
            print_pause("for I knew that the King in Yellow")
            print_pause("had opened his tattered mantle")
            print_pause("and there was only God to cry to now.")

    def book_arkhams_secrets(self):
        """Print content of Arkham's secrets book."""
        if self.key_in_book == 3 and ("THE STUDIO KEY" not in self.player.items):
            self.pick_the_key()
        else:
            print_pause("West of Arkham the hills rise wild,")
            print_pause("and there are valleys with deep")
            print_pause("woods that no axe has ever cut.")

    def pick_the_key(self):
        """Add the key into the player's items."""
        print_pause("You open the book and a key fall onto the ground.")
        self.player.pick_an_item("THE STUDIO KEY")
        self.pick_a_book()

    def pick_a_book(self):
        """Let the user chose a book."""
        print_pause("You pick a book:")
        print_pause("1. Divine Comedy")
        print_pause("2. The King in Yellow")
        print_pause("3. Arkham's Secrets")

        choice = validate_input("Type 1, 2, 3, or back: ", ["1", "2", "3", "back"])

        if choice == "1":
            self.book_divine_comedy()
            self.pick_a_book()
        elif choice == "2":
            self.book_the_king_in_yellow()
            self.pick_a_book()
        elif choice == "3":
            self.book_arkhams_secrets()
        elif choice == "back":
            self.move()

    def forward(self):
        """Print content of the front side of the house."""
        if not self.door_locked:
            print_pause("You open the door and enter the room.")
            self.thehouse.rooms["hallway"].center()
        else:
            print_pause("There's a closed door in front of you")
            print_pause("Do you want to try open it?")

            choice = validate_input("Type yes or no: ", ["yes", "no"])

            if choice == "yes":
                if (
                    "THE STUDIO KEY" in self.player.items
                    or "PASSEPARTOUT" in self.player.items
                ):
                    self.door_locked = False
                    print_pause("You use the key to unlock the door")
                    print_pause("You exit the studio.")
                    self.thehouse.rooms["hallway"].center()
                else:
                    print_pause("The door is loked.")
                    print_pause("It seems you need a key to open it!")
                    print_pause("You go back.")
                    self.move()
            else:
                print_pause("You hear something from the other side of the door!")
                print_pause("You instantly go back!")
                self.player.lose_health()

                if self.player.is_alive:
                    self.move()
