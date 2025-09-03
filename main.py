#!/usr/bin/env python3
"""
Main script for the Random Card Deck project.

This script provides a text-based interface for drawing cards from a deck.
"""

import argparse
import json
import sys
from card_deck.card_deck import CardDeck, DeckManager, Card


def load_decks_from_directory(directory: str) -> DeckManager:
    """
    Load all decks from a directory.

    Args:
        directory: Path to the directory containing deck files

    Returns:
        A DeckManager instance loaded with all decks from the directory

    Raises:
        SystemExit: If the directory cannot be loaded or validation fails
    """
    try:
        deck_manager = DeckManager()
        deck_manager.load_decks_from_directory(directory)
        return deck_manager
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Deck validation failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to load decks: {e}")
        sys.exit(1)


def print_help():
    """Display the help message with available commands."""
    print("\nAvailable commands:")
    print("  d - Draw a random card")
    print("  r - Reset the deck to its original state")
    print("  s - Show the state of all loaded decks")
    print("  q - Quit the application")
    print("  h, ? - Show this help message")
    print()


def print_deck_status(deck_manager: DeckManager, deck_name: str):
    """Print the current status of the specified deck."""
    deck = deck_manager.get_deck(deck_name)
    if deck:
        print(f"\nDeck '{deck_name}' contains {deck.deck_size} cards")
        if deck.drawn_cards:
            card_names = []
            for card in deck.drawn_cards:
                if isinstance(card, Card):
                    card_names.append(card.name)
                else:
                    card_names.append(str(card))
            print(f"Drawn cards: {', '.join(card_names)}")
    print()


def print_all_decks_status(deck_manager: DeckManager):
    """Print the current status of all loaded decks."""
    print(f"\nStatus of all loaded decks ({len(deck_manager.decks)} total):")
    for deck_name, deck in deck_manager.decks.items():
        print(f"\nDeck '{deck_name}':")
        print(f"  Total cards: {deck.total_cards}")
        print(f"  Cards remaining: {deck.deck_size}")
        print(f"  Cards drawn: {len(deck.drawn_cards)}")
        if deck.drawn_cards:
            card_names = []
            for card in deck.drawn_cards:
                if isinstance(card, Card):
                    card_names.append(card.name)
                else:
                    card_names.append(str(card))
            print(f"  Drawn cards: {', '.join(card_names)}")
    print()


def main():
    """Main function providing the text-based interface."""
    parser = argparse.ArgumentParser(
        description="Random Card Deck - Draw cards from a deck interactively"
    )
    parser.add_argument(
        "--deck",
        default="example_deck",
        help=(
            "Name of the deck to load "
            "(default: example_deck)"
        ),
    )
    parser.add_argument(
        "--deck-dir",
        default="data/example_deck",
        help=(
            "Directory containing deck files "
            "(default: data/example_deck)"
        ),
    )

    args = parser.parse_args()

    # Load all decks from the specified directory
    import os
    print(f"Loading all decks from directory:", args.deck_dir)
    deck_manager = load_decks_from_directory(args.deck_dir)
    
    # Check if the specified deck exists
    main_deck = deck_manager.get_deck(args.deck)
    if not main_deck:
        available_decks = list(deck_manager.decks.keys())
        print(f"Error: Deck '{args.deck}' not found. Available decks: {', '.join(available_decks)}")
        sys.exit(1)

    print(f"Loaded {len(deck_manager.decks)} deck(s): {', '.join(deck_manager.decks.keys())}")
    print(f"Using main deck: '{args.deck}' with {main_deck.total_cards} cards")
    print_deck_status(deck_manager, args.deck)

    print("Random Card Deck - Interactive Mode")
    print("Type 'h' or '?' for help")

    while True:
        try:
            command = input("> ").strip().lower()

            if command == "d":
                if main_deck.is_empty():
                    print("The deck is empty!")
                else:
                    result = deck_manager.draw_card_with_extras(args.deck)
                    main_card = result["main_card"]
                    extra_cards = result["extra_cards"]
                    
                    if main_card:
                        # Display main card
                        if isinstance(main_card, Card):
                            print(f"Drew: {main_card.name}")
                            if main_card.description:
                                print(f"  Description: {main_card.description}")
                        else:
                            print(f"Drew: {main_card}")
                        
                        # Display extra cards if any
                        if extra_cards:
                            print(f"  This triggered {len(extra_cards)} additional card(s):")
                            for extra_card in extra_cards:
                                if isinstance(extra_card, Card):
                                    print(f"    - {extra_card.name}")
                                    if extra_card.description:
                                        print(f"      Description: {extra_card.description}")
                                else:
                                    print(f"    - {extra_card}")
                    else:
                        print("No card drawn!")
                        
                print_deck_status(deck_manager, args.deck)

            elif command == "r":
                for deck in deck_manager.decks.values():
                    deck.reset()
                print("All decks reset to original state")
                print_deck_status(deck_manager, args.deck)

            elif command == "s":
                print_all_decks_status(deck_manager)

            elif command in ["q", "quit", "exit"]:
                print("Goodbye!")
                break

            elif command in ["h", "?", "help"]:
                print_help()

            elif command == "":
                # Empty command, just continue
                continue

            else:
                print(f"Unknown command: {command}")
                print("Type 'h' or '?' for help")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
