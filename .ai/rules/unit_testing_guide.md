# How to Add New Unit Tests to This Project

Based on my analysis of the existing codebase and testing structure, here's a comprehensive guide for adding new unit tests to this random-card-draw project.

## Project Testing Overview

The project uses **pytest** as the testing framework with the following configuration:
- Test files are located in the `tests/` directory
- Test files follow the naming convention `test_*.py`
- Test classes follow the naming convention `Test*`
- Test functions follow the naming convention `test_*`
- Poetry is used for dependency management and running tests

## Current Testing Structure

The project currently has these test files:
- `test_card_deck.py` - Tests for the core CardDeck class
- `test_multi_deck_functionality.py` - Tests for multi-deck functionality
- `test_reshuffle.py` - Tests for reshuffle functionality
- `test_s_command.py` - Tests for specific command functionality

## Adding New Unit Tests: Step-by-Step Guide

### 1. Create a New Test File

For testing a new component or feature, create a new test file in the `tests/` directory:

```bash
# Navigate to the tests directory
cd tests/

# Create a new test file (replace 'feature_name' with your actual feature)
touch test_feature_name.py
```

### 2. Follow the Established Testing Patterns

Based on the existing codebase, here are the key patterns to follow:

**File Structure Template:**
```python
"""
Test module for [feature description].

This module tests that:
1. [Key functionality 1]
2. [Key functionality 2]
3. [Key functionality 3]
"""

import pytest
from card_deck.card_deck import [ImportedClasses]


class Test[FeatureName]:
    """Test class for [feature name] functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Initialize test objects here
        pass

    def test_[specific_functionality](self):
        """Test that [specific behavior description]."""
        # Arrange
        # [Setup test data]
        
        # Act
        # [Execute the functionality]
        
        # Assert
        # [Verify expected results]
        pass
```

### 3. Testing Patterns Used in This Project

**Class-Based Organization:**
- Use `class Test[FeatureName]` for organizing related tests
- Use `setup_method()` for test fixtures that need to be recreated for each test

**Arrange-Act-Assert Pattern:**
```python
def test_example_functionality(self):
    """Test that example functionality works correctly."""
    # Arrange
    deck_manager = DeckManager()
    expected_result = "some_value"
    
    # Act
    actual_result = deck_manager.some_method()
    
    # Assert
    assert actual_result == expected_result
```

**Descriptive Test Names:**
- Use descriptive method names that explain what is being tested
- Include the expected behavior in the test name
- Examples: `test_deck_loading_from_directory()`, `test_event_card_drawing_and_extras()`

### 4. Common Testing Scenarios to Add

Based on the project structure, consider adding tests for:

**Error Handling Tests:**
```python
def test_invalid_input_raises_appropriate_error(self):
    """Test that invalid input raises ValueError with clear message."""
    # Arrange
    deck = CardDeck()
    
    # Act & Assert
    with pytest.raises(ValueError, match="expected error message"):
        deck.invalid_operation()
```

**Edge Cases:**
```python
def test_behavior_with_empty_deck(self):
    """Test behavior when deck is empty."""
    # Test edge cases like empty collections, zero values, etc.
```

**Integration Tests:**
```python
def test_complete_workflow(self):
    """Test complete workflow from start to finish."""
    # Test entire user workflows
```

### 5. Running Tests

Use Poetry to run your tests as specified in the RULES.md:

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_your_new_file.py

# Run specific test method
poetry run pytest tests/test_your_new_file.py::TestYourClass::test_specific_method

# Run with verbose output
poetry run pytest -v

# Run with coverage (if you add coverage dependency)
poetry run pytest --cov=card_deck
```

### 6. Testing Guidelines from RULES.md

Follow these specific guidelines from the project's RULES.md:

**Test Structure:**
- Use Arrange-Act-Assert pattern clearly
- Write descriptive test names that describe the scenario
- Each test should verify one specific behavior
- Include tests for edge cases and error conditions

**Dependencies:**
- Make code testable by using dependency injection
- Minimize side effects in the code being tested
- Design code to be easily mocked in tests

### 7. Adding Test Dependencies

If you need additional testing tools, add them through Poetry:

```bash
# Add pytest plugins
poetry add --group dev pytest-cov  # for coverage
poetry add --group dev pytest-mock  # for mocking
poetry add --group dev pytest-asyncio  # for async tests
```

### 8. Test Documentation

Each test should include:
- A descriptive docstring explaining what is being tested
- Clear comments in complex test logic
- Assertion messages when helpful: `assert condition, "Helpful error message"`

### 9. Example New Test File

Here's a complete example for testing a hypothetical new feature:

```python
"""
Test module for card filtering functionality.

This module tests that:
1. Cards can be filtered by various criteria
2. Invalid filter criteria raise appropriate errors
3. Empty results are handled correctly
"""

import pytest
from card_deck.card_deck import CardDeck, Card


class TestCardFiltering:
    """Test class for card filtering functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.deck = CardDeck()
        self.deck.add_cards([
            Card("Red Card", "A red card"),
            Card("Blue Card", "A blue card"),
            Card("Green Card", "A green card")
        ])

    def test_filter_cards_by_color(self):
        """Test that cards can be filtered by color."""
        # Arrange
        color_filter = "Red"
        
        # Act
        filtered_cards = self.deck.filter_by_color(color_filter)
        
        # Assert
        assert len(filtered_cards) == 1
        assert filtered_cards[0].name == "Red Card"

    def test_filter_with_no_matches_returns_empty_list(self):
        """Test that filtering with no matches returns empty list."""
        # Arrange
        non_existent_color = "Purple"
        
        # Act
        filtered_cards = self.deck.filter_by_color(non_existent_color)
        
        # Assert
        assert filtered_cards == []
        assert len(filtered_cards) == 0

    def test_invalid_filter_raises_error(self):
        """Test that invalid filter criteria raise ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Invalid filter criteria"):
            self.deck.filter_by_color(None)
```

## Summary

To add new unit tests to this project:
1. Create new test files in the `tests/` directory following the `test_*.py` naming convention
2. Use class-based organization with the `Test*` naming pattern
3. Follow the Arrange-Act-Assert testing pattern
4. Write descriptive test names and docstrings
5. Use `poetry run pytest` to execute tests
6. Follow the guidelines in RULES.md for code quality and structure
7. Test both happy paths and edge cases/error conditions

The project has a solid testing foundation with pytest, and adding new tests should follow the established patterns for consistency and maintainability.