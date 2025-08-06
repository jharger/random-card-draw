#!/usr/bin/env python3
"""
Main script for the Random Tile Bag project.

This script provides a text-based interface for drawing tiles from a bag.
"""

import argparse
import json
import sys
from random_tile_bag.tile_bag import TileBag


def load_tiles_from_file(file_path: str) -> TileBag:
    """
    Load tiles from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        A TileBag instance loaded with tiles from the file

    Raises:
        SystemExit: If the file cannot be loaded
    """
    try:
        return TileBag.from_json_file(file_path)
    except FileNotFoundError:
        print(f"Error: Tile file '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in tile file: {e}")
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"Error: Invalid tile file format: {e}")
        sys.exit(1)


def print_help():
    """Display the help message with available commands."""
    print("\nAvailable commands:")
    print("  d - Draw a random tile")
    print("  r - Reset the bag to its original state")
    print("  q - Quit the application")
    print("  h, ? - Show this help message")
    print()


def print_bag_status(bag: TileBag):
    """Print the current status of the bag."""
    print(f"\nBag contains {bag.bag_size} tiles")
    if bag.drawn_tiles:
        print(f"Drawn tiles: {', '.join(bag.drawn_tiles)}")
    print()


def main():
    """Main function providing the text-based interface."""
    parser = argparse.ArgumentParser(
        description="Random Tile Bag - Draw tiles from a bag interactively"
    )
    parser.add_argument(
        "--tiles",
        default="data/tiles.json",
        help=(
            "Path to the JSON file containing tile definitions "
            "(default: data/tiles.json)"
        ),
    )

    args = parser.parse_args()

    # Load tiles from the specified file
    print("Loading tiles from:", args.tiles)
    bag = load_tiles_from_file(args.tiles)

    print(f"Loaded {bag.total_tiles} tiles into the bag")
    print_bag_status(bag)

    print("Random Tile Bag - Interactive Mode")
    print("Type 'h' or '?' for help")

    while True:
        try:
            command = input("> ").strip().lower()

            if command == "d":
                if bag.is_empty():
                    print("The bag is empty!")
                else:
                    tile = bag.draw_tile()
                    print(f"Drew: {tile}")
                print_bag_status(bag)

            elif command == "r":
                bag.reset()
                print("Bag reset to original state")
                print_bag_status(bag)

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
