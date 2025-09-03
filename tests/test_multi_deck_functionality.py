#!/usr/bin/env python3
"""
Test script to verify the new multi-deck functionality.
"""

from card_deck.card_deck import DeckManager, Card

def test_multi_deck_functionality():
    """Test that the new multi-deck functionality works correctly."""
    print("Testing multi-deck functionality...")
    
    # Initialize deck manager
    deck_manager = DeckManager()
    
    # Load all decks from the directory
    try:
        deck_manager.load_decks_from_directory("data/example_deck")
        print(f"✓ Successfully loaded {len(deck_manager.decks)} deck(s): {', '.join(deck_manager.decks.keys())}")
    except Exception as e:
        print(f"✗ Failed to load decks: {e}")
        assert False, f"Failed to load decks: {e}"
    
    # Check that both decks were loaded
    if "example_deck" not in deck_manager.decks:
        print("✗ example_deck not found")
        assert False, "example_deck not found"
    if "event_deck" not in deck_manager.decks:
        print("✗ event_deck not found")
        assert False, "event_deck not found"
    
    print("✓ Both example_deck and event_deck loaded successfully")
    
    # Check deck contents
    example_deck = deck_manager.get_deck("example_deck")
    event_deck = deck_manager.get_deck("event_deck")
    
    print(f"✓ Example deck has {example_deck.total_cards} cards")
    print(f"✓ Event deck has {event_deck.total_cards} cards")
    
    # Test drawing regular cards
    print("\nTesting regular card draws...")
    for i in range(3):
        result = deck_manager.draw_card_with_extras("example_deck")
        main_card = result["main_card"]
        extra_cards = result["extra_cards"]
        
        if main_card:
            if isinstance(main_card, Card):
                print(f"  Drew: {main_card.name}")
                if main_card.description:
                    print(f"    Description: {main_card.description}")
                if extra_cards:
                    print(f"    Triggered {len(extra_cards)} extra card(s):")
                    for extra_card in extra_cards:
                        print(f"      - {extra_card.name}: {extra_card.description}")
            else:
                print(f"  Drew: {main_card}")
        else:
            print("  No card drawn")
    
    # Try to find and draw the Event card specifically
    print("\nLooking for Event card...")
    attempts = 0
    max_attempts = 100
    event_found = False
    
    # Reset deck first
    example_deck.reset()
    
    while attempts < max_attempts and not event_found:
        result = deck_manager.draw_card_with_extras("example_deck")
        main_card = result["main_card"]
        extra_cards = result["extra_cards"]
        attempts += 1
        
        if main_card and isinstance(main_card, Card) and main_card.name == "Event":
            event_found = True
            print(f"✓ Found Event card after {attempts} attempts!")
            print(f"  Event card description: {main_card.description}")
            print(f"  Triggered {len(extra_cards)} extra card(s) from event_deck:")
            for extra_card in extra_cards:
                if isinstance(extra_card, Card):
                    print(f"    - {extra_card.name}: {extra_card.description}")
                else:
                    print(f"    - {extra_card}")
            break
    
    if not event_found:
        print(f"✗ Event card not found after {max_attempts} attempts")
        assert False, f"Event card not found after {max_attempts} attempts"
    
    print("\n✓ All tests passed! Multi-deck functionality is working correctly.")
    # Test passes if we reach this point

if __name__ == "__main__":
    success = test_multi_deck_functionality()
    exit(0 if success else 1)