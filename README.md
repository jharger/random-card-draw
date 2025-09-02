# Random Card Deck

A program for testing board game mechanics by simulating drawing a random card from a deck.

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

By default, cards are loaded from `data/cards.json`. You can specify a different cards file:

```bash
poetry run python main.py --cards data/other_cards.json
```

### Interactive Commands

Once running, you can use these commands:

- `d` - Draw a random card
- `r` - Reset the deck to its original state
- `q` - Quit the application
- `h` or `?` - Show help message

### Card File Format

Cards are defined in JSON files with the following structure:

```json
{
    "cards": [
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

Each card definition must have:
- `name`: The name of the card
- `count`: The number of this card to include in the deck (must be a positive integer)

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