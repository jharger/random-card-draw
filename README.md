# Random Tile Bag

A program for testing board game mechanics by simulating drawing a random tile from a bag.

## Installation

This project uses Poetry for dependency management. To install:

```bash
poetry install
```

## Usage

### Interactive Mode

Run the application in interactive mode:

```bash
poetry run python main.py
```

By default, tiles are loaded from `data/tiles.json`. You can specify a different tiles file:

```bash
poetry run python main.py --tiles data/other_tiles.json
```

### Interactive Commands

Once running, you can use these commands:

- `d` - Draw a random tile
- `r` - Reset the bag to its original state
- `q` - Quit the application
- `h` or `?` - Show help message

### Tile File Format

Tiles are defined in JSON files with the following structure:

```json
{
    "tiles": [
        {
            "name": "Grassland",
            "count": 12
        },
        {
            "name": "Desert",
            "count": 6
        }
    ]
}
```

Each tile definition must have:
- `name`: The name of the tile
- `count`: The number of this tile to include in the bag (must be a positive integer)

## Development

To run tests:
```bash
poetry run pytest
```

To format code:
```bash
poetry run black .
```

To lint code:
```bash
poetry run flake8
``` 