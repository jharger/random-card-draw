"""
Unit tests for the TileBag class.
"""

import json
import tempfile
import pytest
from random_tile_bag.tile_bag import TileBag


class TestTileBag:
    """Test cases for the TileBag class."""

    def test_init_empty_bag(self):
        """Test initializing an empty bag."""
        bag = TileBag()
        assert bag.bag_size == 0
        assert bag.total_tiles == 0
        assert bag.is_empty()

    def test_init_with_tiles(self):
        """Test initializing a bag with tiles."""
        tiles = ["A", "B", "C"]
        bag = TileBag(tiles)
        assert bag.bag_size == 3
        assert bag.total_tiles == 3
        assert not bag.is_empty()
        assert set(bag.tiles_in_bag) == set(tiles)

    def test_add_tile(self):
        """Test adding a single tile."""
        bag = TileBag()
        bag.add_tile("X")
        assert bag.bag_size == 1
        assert "X" in bag.tiles_in_bag

    def test_add_tiles(self):
        """Test adding multiple tiles."""
        bag = TileBag()
        tiles = ["X", "Y", "Z"]
        bag.add_tiles(tiles)
        assert bag.bag_size == 3
        assert set(bag.tiles_in_bag) == set(tiles)

    def test_draw_tile(self):
        """Test drawing a single tile."""
        tiles = ["A", "B", "C"]
        bag = TileBag(tiles)

        drawn = bag.draw_tile()
        assert drawn in tiles
        assert bag.bag_size == 2
        assert len(bag.drawn_tiles) == 1
        assert drawn in bag.drawn_tiles

    def test_draw_tile_empty_bag(self):
        """Test drawing from an empty bag."""
        bag = TileBag()
        drawn = bag.draw_tile()
        assert drawn is None

    def test_draw_tiles(self):
        """Test drawing multiple tiles."""
        tiles = ["A", "B", "C", "D"]
        bag = TileBag(tiles)

        drawn = bag.draw_tiles(3)
        assert len(drawn) == 3
        assert bag.bag_size == 1
        assert len(bag.drawn_tiles) == 3

    def test_draw_tiles_more_than_available(self):
        """Test drawing more tiles than available."""
        tiles = ["A", "B"]
        bag = TileBag(tiles)

        drawn = bag.draw_tiles(5)
        assert len(drawn) == 2
        assert bag.is_empty()

    def test_return_tile(self):
        """Test returning a tile to the bag."""
        tiles = ["A", "B", "C"]
        bag = TileBag(tiles)

        drawn = bag.draw_tile()
        bag.return_tile(drawn)

        assert bag.bag_size == 3
        assert len(bag.drawn_tiles) == 0
        assert drawn in bag.tiles_in_bag

    def test_return_all_tiles(self):
        """Test returning all drawn tiles."""
        tiles = ["A", "B", "C"]
        bag = TileBag(tiles)

        bag.draw_tiles(2)
        bag.return_all_tiles()

        assert bag.bag_size == 3
        assert len(bag.drawn_tiles) == 0
        assert set(bag.tiles_in_bag) == set(tiles)

    def test_shuffle(self):
        """Test shuffling the bag."""
        tiles = ["A", "B", "C", "D"]
        bag = TileBag(tiles)

        original_order = bag.tiles_in_bag.copy()
        bag.shuffle()
        shuffled_order = bag.tiles_in_bag

        # The order should be different (though there's a small chance
        # it could be the same)
        assert bag.bag_size == 4
        assert set(shuffled_order) == set(original_order)

    def test_properties_return_copies(self):
        """Test that properties return copies, not references."""
        tiles = ["A", "B", "C"]
        bag = TileBag(tiles)

        # Test tiles_in_bag returns a copy
        bag_tiles = bag.tiles_in_bag
        bag_tiles.append("D")  # This should not affect the bag
        assert bag.bag_size == 3

        # Test drawn_tiles returns a copy
        bag.draw_tile()
        drawn_tiles = bag.drawn_tiles
        drawn_tiles.append("E")  # This should not affect the bag
        assert len(bag.drawn_tiles) == 1

    def test_reset(self):
        """Test resetting the bag to its original state."""
        tiles = ["A", "B", "C"]
        bag = TileBag(tiles)

        # Draw some tiles
        bag.draw_tiles(2)
        assert bag.bag_size == 1
        assert len(bag.drawn_tiles) == 2

        # Reset the bag
        bag.reset()
        assert bag.bag_size == 3
        assert len(bag.drawn_tiles) == 0
        assert set(bag.tiles_in_bag) == set(tiles)

    def test_from_json_file(self):
        """Test creating a TileBag from a JSON file."""
        # Create a temporary JSON file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json_data = {
                "tiles": [
                    {"name": "Grassland", "count": 3},
                    {"name": "Desert", "count": 2},
                ]
            }
            json.dump(json_data, f)
            temp_file = f.name

        try:
            bag = TileBag.from_json_file(temp_file)
            assert bag.total_tiles == 5
            assert bag.tiles_in_bag.count("Grassland") == 3
            assert bag.tiles_in_bag.count("Desert") == 2
        finally:
            import os

            os.unlink(temp_file)

    def test_from_json_file_invalid_structure(self):
        """Test creating a TileBag from an invalid JSON structure."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json_data = {"invalid": "structure"}
            json.dump(json_data, f)
            temp_file = f.name

        try:
            with pytest.raises(
                KeyError, match="JSON file must contain a 'tiles' key"
            ):
                TileBag.from_json_file(temp_file)
        finally:
            import os

            os.unlink(temp_file)

    def test_from_json_file_invalid_tile_format(self):
        """Test creating a TileBag from JSON with invalid tile format."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json_data = {
                "tiles": [
                    {"name": "Grassland"},  # Missing count
                    {"name": "Desert", "count": 2},
                ]
            }
            json.dump(json_data, f)
            temp_file = f.name

        try:
            with pytest.raises(
                KeyError, match="Each tile must have 'name' and 'count' keys"
            ):
                TileBag.from_json_file(temp_file)
        finally:
            import os

            os.unlink(temp_file)

    def test_from_json_file_invalid_count(self):
        """Test creating a TileBag from JSON with invalid count values."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json_data = {
                "tiles": [
                    {"name": "Grassland", "count": 0},  # Invalid count
                    {"name": "Desert", "count": 2},
                ]
            }
            json.dump(json_data, f)
            temp_file = f.name

        try:
            with pytest.raises(
                ValueError, match="Tile count must be a positive integer"
            ):
                TileBag.from_json_file(temp_file)
        finally:
            import os

            os.unlink(temp_file)
