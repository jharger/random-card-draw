"""
Unit tests for the CardDeck class.
"""

import json
import tempfile
import pytest
from card_deck.card_deck import CardDeck


class TestCardDeck:
    """Test cases for the CardDeck class."""

    def test_init_empty_deck(self):
        """Test initializing an empty deck."""
        deck = CardDeck()
        assert deck.deck_size == 0
        assert deck.total_cards == 0
        assert deck.is_empty()

    def test_init_with_cards(self):
        """Test initializing a deck with cards."""
        cards = ["A", "B", "C"]
        deck = CardDeck(cards)
        assert deck.deck_size == 3
        assert deck.total_cards == 3
        assert not deck.is_empty()
        assert set(deck.cards_in_deck) == set(cards)

    def test_add_card(self):
        """Test adding a single card."""
        deck = CardDeck()
        deck.add_card("X")
        assert deck.deck_size == 1
        assert "X" in deck.cards_in_deck

    def test_add_cards(self):
        """Test adding multiple cards."""
        deck = CardDeck()
        cards = ["X", "Y", "Z"]
        deck.add_cards(cards)
        assert deck.deck_size == 3
        assert set(deck.cards_in_deck) == set(cards)

    def test_draw_card(self):
        """Test drawing a single card."""
        cards = ["A", "B", "C"]
        deck = CardDeck(cards)

        drawn = deck.draw_card()
        assert drawn in cards
        assert deck.deck_size == 2
        assert len(deck.drawn_cards) == 1
        assert drawn in deck.drawn_cards

    def test_draw_card_empty_deck(self):
        """Test drawing from an empty deck."""
        deck = CardDeck()
        drawn = deck.draw_card()
        assert drawn is None

    def test_draw_cards(self):
        """Test drawing multiple cards."""
        cards = ["A", "B", "C", "D"]
        deck = CardDeck(cards)

        drawn = deck.draw_cards(3)
        assert len(drawn) == 3
        assert deck.deck_size == 1
        assert len(deck.drawn_cards) == 3

    def test_draw_cards_more_than_available(self):
        """Test drawing more cards than available."""
        cards = ["A", "B"]
        deck = CardDeck(cards)

        drawn = deck.draw_cards(5)
        assert len(drawn) == 2
        assert deck.is_empty()

    def test_return_card(self):
        """Test returning a card to the deck."""
        cards = ["A", "B", "C"]
        deck = CardDeck(cards)

        drawn = deck.draw_card()
        deck.return_card(drawn)

        assert deck.deck_size == 3
        assert len(deck.drawn_cards) == 0
        assert drawn in deck.cards_in_deck

    def test_return_all_cards(self):
        """Test returning all drawn cards."""
        cards = ["A", "B", "C"]
        deck = CardDeck(cards)

        deck.draw_cards(2)
        deck.return_all_cards()

        assert deck.deck_size == 3
        assert len(deck.drawn_cards) == 0
        assert set(deck.cards_in_deck) == set(cards)

    def test_shuffle(self):
        """Test shuffling the deck."""
        cards = ["A", "B", "C", "D"]
        deck = CardDeck(cards)

        original_order = deck.cards_in_deck.copy()
        deck.shuffle()
        shuffled_order = deck.cards_in_deck

        # The order should be different (though there's a small chance
        # it could be the same)
        assert deck.deck_size == 4
        assert set(shuffled_order) == set(original_order)

    def test_properties_return_copies(self):
        """Test that properties return copies, not references."""
        cards = ["A", "B", "C"]
        deck = CardDeck(cards)

        # Test cards_in_deck returns a copy
        deck_cards = deck.cards_in_deck
        deck_cards.append("D")  # This should not affect the deck
        assert deck.deck_size == 3

        # Test drawn_cards returns a copy
        deck.draw_card()
        drawn_cards = deck.drawn_cards
        drawn_cards.append("E")  # This should not affect the deck
        assert len(deck.drawn_cards) == 1

    def test_reset(self):
        """Test resetting the deck to its original state."""
        cards = ["A", "B", "C"]
        deck = CardDeck(cards)

        # Draw some cards
        deck.draw_cards(2)
        assert deck.deck_size == 1
        assert len(deck.drawn_cards) == 2

        # Reset the deck
        deck.reset()
        assert deck.deck_size == 3
        assert len(deck.drawn_cards) == 0
        assert set(deck.cards_in_deck) == set(cards)

    def test_from_json_file(self):
        """Test creating a CardDeck from a JSON file."""
        # Create a temporary JSON file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json_data = {
                "cards": [
                    {"name": "Grassland", "count": 3},
                    {"name": "Desert", "count": 2},
                ]
            }
            json.dump(json_data, f)
            temp_file = f.name

        try:
            deck = CardDeck.from_json_file(temp_file)
            assert deck.total_cards == 5
            assert deck.cards_in_deck.count("Grassland") == 3
            assert deck.cards_in_deck.count("Desert") == 2
        finally:
            import os

            os.unlink(temp_file)

    def test_from_json_file_invalid_structure(self):
        """Test creating a CardDeck from an invalid JSON structure."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json_data = {"invalid": "structure"}
            json.dump(json_data, f)
            temp_file = f.name

        try:
            with pytest.raises(
                KeyError, match="JSON file must contain a 'cards' key"
            ):
                CardDeck.from_json_file(temp_file)
        finally:
            import os

            os.unlink(temp_file)

    def test_from_json_file_invalid_card_format(self):
        """Test creating a CardDeck from JSON with invalid card format."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json_data = {
                "cards": [
                    {"name": "Grassland"},  # Missing count
                    {"name": "Desert", "count": 2},
                ]
            }
            json.dump(json_data, f)
            temp_file = f.name

        try:
            with pytest.raises(
                KeyError, match="Each card must have 'name' and 'count' keys"
            ):
                CardDeck.from_json_file(temp_file)
        finally:
            import os

            os.unlink(temp_file)

    def test_from_json_file_invalid_count(self):
        """Test creating a CardDeck from JSON with invalid count values."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json_data = {
                "cards": [
                    {"name": "Grassland", "count": 0},  # Invalid count
                    {"name": "Desert", "count": 2},
                ]
            }
            json.dump(json_data, f)
            temp_file = f.name

        try:
            with pytest.raises(
                ValueError, match="Card count must be a positive integer"
            ):
                CardDeck.from_json_file(temp_file)
        finally:
            import os

            os.unlink(temp_file)