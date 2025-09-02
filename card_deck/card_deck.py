"""
Card Deck implementation for simulating random card drawing from a deck.
"""

import json
import random
from typing import List, Optional, Any


class CardDeck:
    """
    A deck containing cards that can be drawn randomly.

    This class simulates drawing cards from a deck, which is common in board
    games.
    It supports adding cards, drawing cards, and tracking the deck's state.
    """

    def __init__(self, cards: Optional[List[Any]] = None):
        """
        Initialize a new card deck.

        Args:
            cards: Optional list of cards to start with in the deck
        """
        self._cards = cards.copy() if cards else []
        self._drawn_cards = []
        self._original_cards = cards.copy() if cards else []

    @classmethod
    def from_json_file(cls, file_path: str) -> "CardDeck":
        """
        Create a CardDeck from a JSON file.

        Args:
            file_path: Path to the JSON file containing card definitions

        Returns:
            A new CardDeck instance loaded with cards from the JSON file

        Raises:
            FileNotFoundError: If the JSON file doesn't exist
            json.JSONDecodeError: If the JSON file is malformed
            KeyError: If the JSON structure is invalid
        """
        with open(file_path, "r") as f:
            data = json.load(f)

        if "cards" not in data:
            raise KeyError("JSON file must contain a 'cards' key")

        cards = []
        for card_def in data["cards"]:
            if "name" not in card_def or "count" not in card_def:
                raise KeyError("Each card must have 'name' and 'count' keys")

            name = card_def["name"]
            count = card_def["count"]

            if not isinstance(count, int) or count <= 0:
                raise ValueError("Card count must be a positive integer")

            # Add the card 'count' number of times
            cards.extend([name] * count)

        return cls(cards)

    def reset(self) -> None:
        """
        Reset the deck to its original state.
        """
        self._cards = self._original_cards.copy()
        self._drawn_cards = []

    def add_card(self, card: Any) -> None:
        """
        Add a card to the deck.

        Args:
            card: The card to add to the deck
        """
        self._cards.append(card)

    def add_cards(self, cards: List[Any]) -> None:
        """
        Add multiple cards to the deck.

        Args:
            cards: List of cards to add to the deck
        """
        self._cards.extend(cards)

    def draw_card(self) -> Optional[Any]:
        """
        Draw a random card from the deck.

        Returns:
            The drawn card, or None if the deck is empty
        """
        if not self._cards:
            return None

        card = random.choice(self._cards)
        self._cards.remove(card)
        self._drawn_cards.append(card)
        return card

    def draw_cards(self, count: int) -> List[Any]:
        """
        Draw multiple random cards from the deck.

        Args:
            count: Number of cards to draw

        Returns:
            List of drawn cards (may be shorter than requested if deck runs out)
        """
        drawn = []
        for _ in range(count):
            card = self.draw_card()
            if card is None:
                break
            drawn.append(card)
        return drawn

    def return_card(self, card: Any) -> None:
        """
        Return a drawn card back to the deck.

        Args:
            card: The card to return to the deck
        """
        if card in self._drawn_cards:
            self._drawn_cards.remove(card)
            self._cards.append(card)

    def return_all_cards(self) -> None:
        """
        Return all drawn cards back to the deck.
        """
        self._cards.extend(self._drawn_cards)
        self._drawn_cards.clear()

    def shuffle(self) -> None:
        """
        Shuffle the cards remaining in the deck.
        """
        random.shuffle(self._cards)

    @property
    def cards_in_deck(self) -> List[Any]:
        """
        Get the cards currently in the deck.

        Returns:
            List of cards remaining in the deck
        """
        return self._cards.copy()

    @property
    def drawn_cards(self) -> List[Any]:
        """
        Get the cards that have been drawn.

        Returns:
            List of cards that have been drawn
        """
        return self._drawn_cards.copy()

    @property
    def deck_size(self) -> int:
        """
        Get the number of cards currently in the deck.

        Returns:
            Number of cards in the deck
        """
        return len(self._cards)

    @property
    def total_cards(self) -> int:
        """
        Get the total number of cards (in deck + drawn).

        Returns:
            Total number of cards
        """
        return len(self._cards) + len(self._drawn_cards)

    def is_empty(self) -> bool:
        """
        Check if the deck is empty.

        Returns:
            True if the deck is empty, False otherwise
        """
        return len(self._cards) == 0