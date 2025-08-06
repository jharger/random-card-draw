#!/usr/bin/env python3
"""
Main script for the Random Tile Bag project.

This script demonstrates the TileBag functionality with a simple example.
"""

from random_tile_bag.tile_bag import TileBag


def main():
    """Main function demonstrating TileBag usage."""
    print("Random Tile Bag Demo")
    print("=" * 50)
    
    # Create a tile bag with some sample tiles
    tiles = ["Forest", "Mountain", "Desert", "Ocean", "City", "Village", "Castle", "Cave"]
    bag = TileBag(tiles)
    
    print(f"Created bag with {bag.total_tiles} tiles: {bag.tiles_in_bag}")
    print()
    
    # Draw some tiles
    print("Drawing 3 tiles:")
    drawn = bag.draw_tiles(3)
    for i, tile in enumerate(drawn, 1):
        print(f"  {i}. Drew: {tile}")
    
    print(f"\nTiles remaining in bag: {bag.tiles_in_bag}")
    print(f"Tiles drawn: {bag.drawn_tiles}")
    print(f"Bag size: {bag.bag_size}")
    print()
    
    # Return one tile
    if drawn:
        returned_tile = drawn[0]
        bag.return_tile(returned_tile)
        print(f"Returned '{returned_tile}' to the bag")
        print(f"Tiles remaining in bag: {bag.tiles_in_bag}")
        print(f"Tiles drawn: {bag.drawn_tiles}")
        print()
    
    # Draw until empty
    print("Drawing remaining tiles:")
    count = 1
    while not bag.is_empty():
        tile = bag.draw_tile()
        print(f"  {count}. Drew: {tile}")
        count += 1
    
    print(f"\nBag is now empty: {bag.is_empty()}")
    print(f"All drawn tiles: {bag.drawn_tiles}")
    print()
    
    # Return all tiles and shuffle
    bag.return_all_tiles()
    bag.shuffle()
    print("Returned all tiles and shuffled the bag")
    print(f"Tiles in bag: {bag.tiles_in_bag}")


if __name__ == "__main__":
    main()
