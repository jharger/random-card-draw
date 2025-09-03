"""
Test module for reshuffle functionality.

This module tests that:
1. Event deck reshuffles automatically when empty
2. Main deck does not reshuffle when empty
3. Reshuffle notifications are displayed
"""

import pytest
from card_deck.card_deck import DeckManager


class TestReshuffleFunctionality:
    """Test class for reshuffle functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.deck_manager = DeckManager()
        self.deck_manager.load_decks_from_directory("data/example_deck")
        self.event_deck = self.deck_manager.get_deck("event_deck")
        self.main_deck = self.deck_manager.get_deck("example_deck")

    def test_decks_loaded_successfully(self):
        """Test that both decks are loaded successfully."""
        assert self.event_deck is not None, "Event deck should be loaded"
        assert self.main_deck is not None, "Main deck should be loaded"

    def test_reshuffle_settings(self):
        """Test that reshuffle settings are correct for each deck."""
        assert self.event_deck.reshuffle is True, "Event deck should have reshuffle enabled"
        assert self.main_deck.reshuffle is False, "Main deck should have reshuffle disabled"

    def test_event_deck_reshuffles_when_empty(self, capsys):
        """Test that event deck automatically reshuffles when empty."""
        # Record initial card count
        initial_total = self.event_deck.total_cards
        assert initial_total > 0, "Event deck should have cards initially"

        # Draw all cards from event deck
        drawn_cards = []
        while not self.event_deck.is_empty():
            card = self.event_deck.draw_card()
            if card:
                drawn_cards.append(card)

        # Verify deck is empty
        assert self.event_deck.is_empty(), "Deck should be empty after drawing all cards"
        assert len(drawn_cards) == initial_total, "Should have drawn all initial cards"

        # Try to draw one more card - should trigger reshuffle
        card = self.event_deck.draw_card()
        
        # Verify card was drawn after reshuffle
        assert card is not None, "Should be able to draw card after reshuffle"
        assert not self.event_deck.is_empty(), "Deck should not be empty after reshuffle"

        # Check that reshuffle notification was displayed
        captured = capsys.readouterr()
        assert "reshuffled" in captured.out.lower(), "Should display reshuffle notification"

    def test_main_deck_does_not_reshuffle_when_empty(self):
        """Test that main deck does not reshuffle when empty."""
        # Reset to original state
        self.main_deck.reset()
        initial_total = self.main_deck.total_cards
        assert initial_total > 0, "Main deck should have cards initially"

        # Draw all cards from main deck
        drawn_count = 0
        while not self.main_deck.is_empty():
            card = self.main_deck.draw_card()
            if card:
                drawn_count += 1

        # Verify deck is empty and all cards were drawn
        assert self.main_deck.is_empty(), "Deck should be empty after drawing all cards"
        assert drawn_count == initial_total, "Should have drawn all initial cards"

        # Try to draw one more card - should return None (no reshuffle)
        card = self.main_deck.draw_card()
        
        # Verify no card was drawn and deck remains empty
        assert card is None, "Should not be able to draw card from empty non-reshuffling deck"
        assert self.main_deck.is_empty(), "Deck should remain empty"

    def test_event_deck_multiple_reshuffles(self):
        """Test that event deck can be reshuffled multiple times."""
        initial_total = self.event_deck.total_cards
        
        # Empty and reshuffle twice
        for cycle in range(2):
            # Draw all cards
            while not self.event_deck.is_empty():
                self.event_deck.draw_card()
            
            # Draw one more to trigger reshuffle
            card = self.event_deck.draw_card()
            assert card is not None, f"Should draw card after reshuffle cycle {cycle + 1}"
            
        # Verify deck still has cards available after multiple reshuffles
        assert not self.event_deck.is_empty(), "Deck should have cards after multiple reshuffles"