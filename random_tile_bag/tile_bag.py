"""
Tile Bag implementation for simulating random tile drawing from a bag.
"""

import random
from typing import List, Optional, Any


class TileBag:
    """
    A bag containing tiles that can be drawn randomly.
    
    This class simulates drawing tiles from a bag, which is common in board games.
    It supports adding tiles, drawing tiles, and tracking the bag's state.
    """
    
    def __init__(self, tiles: Optional[List[Any]] = None):
        """
        Initialize a new tile bag.
        
        Args:
            tiles: Optional list of tiles to start with in the bag
        """
        self._tiles = tiles.copy() if tiles else []
        self._drawn_tiles = []
    
    def add_tile(self, tile: Any) -> None:
        """
        Add a tile to the bag.
        
        Args:
            tile: The tile to add to the bag
        """
        self._tiles.append(tile)
    
    def add_tiles(self, tiles: List[Any]) -> None:
        """
        Add multiple tiles to the bag.
        
        Args:
            tiles: List of tiles to add to the bag
        """
        self._tiles.extend(tiles)
    
    def draw_tile(self) -> Optional[Any]:
        """
        Draw a random tile from the bag.
        
        Returns:
            The drawn tile, or None if the bag is empty
        """
        if not self._tiles:
            return None
        
        tile = random.choice(self._tiles)
        self._tiles.remove(tile)
        self._drawn_tiles.append(tile)
        return tile
    
    def draw_tiles(self, count: int) -> List[Any]:
        """
        Draw multiple random tiles from the bag.
        
        Args:
            count: Number of tiles to draw
            
        Returns:
            List of drawn tiles (may be shorter than requested if bag runs out)
        """
        drawn = []
        for _ in range(count):
            tile = self.draw_tile()
            if tile is None:
                break
            drawn.append(tile)
        return drawn
    
    def return_tile(self, tile: Any) -> None:
        """
        Return a drawn tile back to the bag.
        
        Args:
            tile: The tile to return to the bag
        """
        if tile in self._drawn_tiles:
            self._drawn_tiles.remove(tile)
            self._tiles.append(tile)
    
    def return_all_tiles(self) -> None:
        """
        Return all drawn tiles back to the bag.
        """
        self._tiles.extend(self._drawn_tiles)
        self._drawn_tiles.clear()
    
    def shuffle(self) -> None:
        """
        Shuffle the tiles remaining in the bag.
        """
        random.shuffle(self._tiles)
    
    @property
    def tiles_in_bag(self) -> List[Any]:
        """
        Get the tiles currently in the bag.
        
        Returns:
            List of tiles remaining in the bag
        """
        return self._tiles.copy()
    
    @property
    def drawn_tiles(self) -> List[Any]:
        """
        Get the tiles that have been drawn.
        
        Returns:
            List of tiles that have been drawn
        """
        return self._drawn_tiles.copy()
    
    @property
    def bag_size(self) -> int:
        """
        Get the number of tiles currently in the bag.
        
        Returns:
            Number of tiles in the bag
        """
        return len(self._tiles)
    
    @property
    def total_tiles(self) -> int:
        """
        Get the total number of tiles (in bag + drawn).
        
        Returns:
            Total number of tiles
        """
        return len(self._tiles) + len(self._drawn_tiles)
    
    def is_empty(self) -> bool:
        """
        Check if the bag is empty.
        
        Returns:
            True if the bag is empty, False otherwise
        """
        return len(self._tiles) == 0 