"""Module for card."""
from __future__ import annotations

from typing import Any, Union

# fmt: off
rank_map = {
    "2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7,
    "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12,
}
suit_map = {
    "C": 0, "D": 1, "H": 2, "S": 3,
    "c": 0, "d": 1, "h": 2, "s": 3
}
# fmt: on

rank_reverse_map = {value: key for key, value in rank_map.items()}
suit_reverse_map = {value: key for key, value in suit_map.items() if key.islower()}


class Card:
    """An immutable card object.

    Attributes:
        __id (int): The integer that identifies the card.
            We can use an integer to represent a card. The two least significant bits
            represent the 4 suits, ranged from 0-3. The rest of it represent the 13
            ranks, ranged from 0-12.

            More specifically, the ranks are:

            deuce = 0, trey = 1, four = 2, five = 3, six = 4, seven = 5, eight = 6,
            nine = 7, ten = 8, jack = 9, queen = 10, king = 11, ace = 12.

            And the suits are:
            club = 0, diamond = 1, heart = 2, spade = 3

            So that you can use `rank * 4 + suit` to get the card ID.

    """

    __slots__ = ["__id"]
    __id: int

    def __init__(self, other: Union[int, str, Card]):
        """Construct card object.

        If the passed argument is integer, it's set to `self.__id`.
        If the passed argument is string, its id is calculated and set to `self.__id`.
        Thus, the original string is discarded. e.g. Card("2C").describe_card() == "2c"
        If the passed argument is Card, it's copied.

        Args:
            other (int): The integer that identifies the card.
            other (str): The description of the card. e.g. "2c", "Ah"
            other (Card): The other card to copy.

        """
        card_id = Card.to_id(other)
        # Note: use base class assignment because assignment to this class is protected
        # by `Card.__setattr__`
        # Note: use name mangling: `_Card__id` instead of `Card.__id`.
        object.__setattr__(self, "_Card__id", card_id)  # equiv to `self.__id = card_id`

    @property
    def id_(self) -> int:
        """Return `self.__id`.

        Returns:
            int:
        """
        return self.__id

    @staticmethod
    def to_id(other: Union[int, str, Card]) -> int:
        """Return the Card ID integer as API.

        If the passed argument is integer, it's returned with doing nothing.
        If the passed argument is string, its id is calculated.
        If the passed argument is Card, `other.id_` is returned.

        Args:
            other (int): The integer that identifies the card.
            other (str): The description of the card. e.g. "2c", "Ah"
            other (Card): The other card to copy.

        Raises:
            ValueError: Passed invalid string
            TypeError: Passed unsupported type

        Returns:
            int: Card ID
        """
        if isinstance(other, int):
            return other
        elif isinstance(other, str):
            if len(other) != 2:
                raise ValueError(f"The length of value must be 2. passed: {other}")
            rank, suit, *_ = tuple(other)
            return rank_map[rank] * 4 + suit_map[suit]
        elif isinstance(other, Card):
            return other.id_

        raise TypeError(
            f"Type of parameter must be int, str or Card. passed: {type(other)}"
        )

    def describe_rank(self) -> str:
        """Calculate card rank.

        Returns:
            str: The card rank

        """
        return rank_reverse_map[self.id_ // 4]

    def describe_suit(self) -> str:
        """Calculate suit. It's lowercased.

        Returns:
            str: The suit of the card

        """
        return suit_reverse_map[self.id_ % 4]

    def describe_card(self) -> str:
        """Return card description.

        Returns:
            str: The card description.

        """
        return self.describe_rank() + self.describe_suit()

    def __eq__(self, other: Any) -> bool:
        """Return equality. This is special method.

        Args:
            other (int): This is compared to `int(self)`
            other (str): This is compared to `str(self)`. It's case-insensitive.
            other (Card): `other.id_` is compared to `self.id_`.
            other (Any): This is compared to `self.id_`

        Returns:
            bool: The result of `self == other`

        """
        if isinstance(other, int):
            return int(self) == other
        if isinstance(other, str):
            # case-insensitive
            return str(self).lower() == other.lower()
        if isinstance(other, Card):
            return self.id_ == other.id_
        return self.id_ == other

    def __str__(self) -> str:
        """str: Special method for `str(self)`. e.g. '2c', 'Ah'."""
        return self.describe_card()

    def __repr__(self) -> str:
        """str: Special method for `repr(self)`. e.g. Card("2c"), Card("Ah")."""
        return f'Card("{self.describe_card()}")'

    def __int__(self) -> int:
        """int: Special method for `int(self)`."""
        return self.id_

    def __hash__(self) -> int:
        """int: Special method for `hash(self)`."""
        return hash(self.id_)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an attribute. This causes TypeError since assignment to attribute is prevented."""
        raise TypeError("Card object does not support assignment to attribute")

    def __delattr__(self, name: str) -> None:
        """Delete an attribute. This causes TypeError since deletion of attribute is prevented."""
        raise TypeError("Card object does not support deletion of attribute")
