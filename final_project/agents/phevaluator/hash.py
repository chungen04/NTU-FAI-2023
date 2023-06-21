"""Module hashing cards."""
from __future__ import annotations

from .tables import CHOOSE, DP


def hash_quinary(quinary: [int], num_cards: int) -> int:
    """Hash list of cards.

    Args:
        quinary ([int]): List of the count of the cards.
        num_cards (int): The number of cards.

    Returns:
        int: hash value
    """
    sum_numb = 0
    length = len(quinary)

    for rank, cnt in enumerate(quinary):
        if cnt:
            sum_numb += DP[cnt][length - rank - 1][num_cards]
            num_cards -= cnt

    return sum_numb


def hash_binary(binary: int, num_cards: int) -> int:
    """Hash binary.

    Args:
        binary (int): The binary expressing combination of the cards.
        num_cards (int): The number of the cards.

    """
    sum_numb = 0
    length = 15

    for rank in range(length):

        if (binary >> rank) % 2:
            sum_numb += CHOOSE[length - rank - 1][num_cards]
            num_cards -= 1

    return sum_numb
