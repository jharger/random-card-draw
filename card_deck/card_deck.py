"""
Card Deck implementation for simulating random card drawing from a deck.
"""

import json
import random
import os
from typing import List, Optional, Any, Dict, Union


class Card:
    """
    Represents a single card with its properties.
    """
    
    def __init__(self, name: str, description: str = "", draw_from: Optional[str] = None, draw_count: int = 0):
        """
        Initialize a card.
        
        Args:
            name: The name of the card
            description: Description of the card
            draw_from: Optional name of another deck to draw from when this card is drawn
            draw_count: Number of cards to draw from the other deck (default 0)
        """
        self.name = name
        self.description = description
        self.draw_from = draw_from
        self.draw_count = draw_count if draw_from else 0
    
    def __str__(self):
        """String representation of the card."""
        return self.name
    
    def __repr__(self):
        """Detailed representation of the card."""
        return f"Card(name='{self.name}', description='{self.description}', draw_from='{self.draw_from}', draw_count={self.draw_count})"


class DeckManager:
    """
    Manages multiple decks and their interactions.
    """
    
    def __init__(self):
        """Initialize the deck manager."""
        self.decks: Dict[str, 'CardDeck'] = {}
    
    def load_decks_from_directory(self, directory: str) -> None:
        """
        Load all deck files from a directory.
        
        Args:
            directory: Directory containing deck JSON files
            
        Raises:
            FileNotFoundError: If directory doesn't exist
            ValueError: If deck validation fails
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory '{directory}' not found")
        
        # Load all JSON files in the directory
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                try:
                    deck = CardDeck.from_json_file(file_path)
                    self.decks[deck.name] = deck
                except Exception as e:
                    print(f"Warning: Failed to load deck from {file_path}: {e}")
        
        # Validate that all referenced decks exist
        self._validate_deck_references()
    
    def _validate_deck_references(self) -> None:
        """
        Validate that all deck references in cards exist.
        
        Raises:
            ValueError: If a referenced deck doesn't exist
        """
        for deck_name, deck in self.decks.items():
            for card in deck._original_cards:
                if isinstance(card, Card) and card.draw_from:
                    if card.draw_from not in self.decks:
                        raise ValueError(f"Card '{card.name}' in deck '{deck_name}' references unknown deck '{card.draw_from}'")
    
    def get_deck(self, name: str) -> Optional['CardDeck']:
        """Get a deck by name."""
        return self.decks.get(name)
    
    def draw_card_with_extras(self, deck_name: str) -> Dict[str, Any]:
        """
        Draw a card and any additional cards it triggers.
        
        Args:
            deck_name: Name of the deck to draw from
            
        Returns:
            Dictionary containing the main card and any extra cards drawn
        """
        deck = self.get_deck(deck_name)
        if not deck or deck.is_empty():
            return {"main_card": None, "extra_cards": []}
        
        main_card = deck.draw_card()
        extra_cards = []
        
        if isinstance(main_card, Card) and main_card.draw_from and main_card.draw_count > 0:
            extra_deck = self.get_deck(main_card.draw_from)
            if extra_deck:
                extra_cards = extra_deck.draw_cards(main_card.draw_count)
        
        return {"main_card": main_card, "extra_cards": extra_cards}


class CardDeck:
    """
    A deck containing cards that can be drawn randomly.

    This class simulates drawing cards from a deck, which is common in board
    games.
    It supports adding cards, drawing cards, and tracking the deck's state.
    """

    def __init__(self, cards: Optional[List[Any]] = None, name: str = ""):
        """
        Initialize a new card deck.

        Args:
            cards: Optional list of cards to start with in the deck
            name: Name of the deck
        """
        self._cards = cards.copy() if cards else []
        self._drawn_cards = []
        self._original_cards = cards.copy() if cards else []
        self.name = name

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

        deck_name = data.get("name", os.path.splitext(os.path.basename(file_path))[0])

        cards = []
        for card_def in data["cards"]:
            if "name" not in card_def or "count" not in card_def:
                raise KeyError("Each card must have 'name' and 'count' keys")

            name = card_def["name"]
            count = card_def["count"]
            description = card_def.get("description", "")
            draw_from = card_def.get("draw_from")
            draw_count = card_def.get("draw_count", 0)

            if not isinstance(count, int) or count <= 0:
                raise ValueError("Card count must be a positive integer")

            # Create Card objects if any advanced properties are present
            if description or draw_from:
                card = Card(name=name, description=description, draw_from=draw_from, draw_count=draw_count)
                cards.extend([card] * count)
            else:
                # Backward compatibility: store as string for simple cards
                cards.extend([name] * count)

        return cls(cards, name=deck_name)

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