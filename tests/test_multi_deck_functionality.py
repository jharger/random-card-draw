"""
Test suite to verify the new multi-deck functionality.
"""

import pytest
from card_deck.card_deck import DeckManager, Card


@pytest.fixture
def deck_manager():
    """Create and configure a DeckManager for testing."""
    manager = DeckManager()
    manager.load_decks_from_directory("data/example_deck")
    return manager


def test_deck_loading_from_directory():
    """Test that decks can be loaded from a directory."""
    # Arrange
    deck_manager = DeckManager()
    
    # Act
    deck_manager.load_decks_from_directory("data/example_deck")
    
    # Assert
    assert len(deck_manager.decks) == 2
    assert "example_deck" in deck_manager.decks
    assert "event_deck" in deck_manager.decks


def test_deck_content_verification(deck_manager):
    """Test that loaded decks have expected content."""
    # Arrange & Act
    example_deck = deck_manager.get_deck("example_deck")
    event_deck = deck_manager.get_deck("event_deck")
    
    # Assert
    assert example_deck is not None
    assert event_deck is not None
    assert example_deck.total_cards > 0
    assert event_deck.total_cards > 0


def test_regular_card_drawing(deck_manager):
    """Test that regular cards can be drawn from decks."""
    # Arrange
    draw_count = 3
    successful_draws = 0
    
    # Act
    for i in range(draw_count):
        result = deck_manager.draw_card_with_extras("example_deck")
        main_card = result["main_card"]
        extra_cards = result["extra_cards"]
        
        if main_card:
            successful_draws += 1
            # Verify the result structure
            assert "main_card" in result
            assert "extra_cards" in result
            assert isinstance(extra_cards, list)
    
    # Assert
    assert successful_draws > 0


def test_event_card_drawing_and_extras(deck_manager):
    """Test that Event card can be found and triggers extra cards."""
    # Arrange
    attempts = 0
    max_attempts = 100
    event_found = False
    example_deck = deck_manager.get_deck("example_deck")
    example_deck.reset()
    
    # Act
    while attempts < max_attempts and not event_found:
        result = deck_manager.draw_card_with_extras("example_deck")
        main_card = result["main_card"]
        extra_cards = result["extra_cards"]
        attempts += 1
        
        if main_card and isinstance(main_card, Card) and main_card.name == "Event":
            event_found = True
            
            # Assert
            assert main_card.description is not None
            assert isinstance(extra_cards, list)
            assert len(extra_cards) > 0
            
            # Verify extra cards are valid
            for extra_card in extra_cards:
                assert isinstance(extra_card, Card)
                assert extra_card.name is not None
            
            break
    
    # Assert
    assert event_found, f"Event card not found after {max_attempts} attempts"