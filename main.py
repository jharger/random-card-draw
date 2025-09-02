#!/usr/bin/env python3
"""
Main script for the Random Card Deck project.

This script provides a text-based interface for drawing cards from a deck.
"""

import argparse
import json
import sys
from card_deck.card_deck import CardDeck


def load_cards_from_file(file_path: str) -> CardDeck:
    """
    Load cards from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        A CardDeck instance loaded with cards from the file

    Raises:
        SystemExit: If the file cannot be loaded
    """
    try:
        return CardDeck.from_json_file(file_path)
    except FileNotFoundError:
        print(f"Error: Card file '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in card file: {e}")
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"Error: Invalid card file format: {e}")
        sys.exit(1)


def print_help():
    """Display the help message with available commands."""
    print("\nAvailable commands:")
    print("  d - Draw a random card")
    print("  r - Reset the deck to its original state")
    print("  q - Quit the application")
    print("  h, ? - Show this help message")
    print()


def print_deck_status(deck: CardDeck):
    """Print the current status of the deck."""
    print(f"\nDeck contains {deck.deck_size} cards")
    if deck.drawn_cards:
        print(f"Drawn cards: {', '.join(deck.drawn_cards)}")
    print()


def main():
    """Main function providing the text-based interface."""
    parser = argparse.ArgumentParser(
        description="Random Card Deck - Draw cards from a deck interactively"
    )
    parser.add_argument(
        "--cards",
        default="data/cards.json",
        help=(
            "Path to the JSON file containing card definitions "
            "(default: data/cards.json)"
        ),
    )

    args = parser.parse_args()

    # Load cards from the specified file
    print("Loading cards from:", args.cards)
    deck = load_cards_from_file(args.cards)

    print(f"Loaded {deck.total_cards} cards into the deck")
    print_deck_status(deck)

    print("Random Card Deck - Interactive Mode")
    print("Type 'h' or '?' for help")

    while True:
        try:
            command = input("> ").strip().lower()

            if command == "d":
                if deck.is_empty():
                    print("The deck is empty!")
                else:
                    card = deck.draw_card()
                    print(f"Drew: {card}")
                print_deck_status(deck)

            elif command == "r":
                deck.reset()
                print("Deck reset to original state")
                print_deck_status(deck)

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
