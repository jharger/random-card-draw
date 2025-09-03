# Python Code Rules for Agentic Programming

This document outlines coding standards and best practices specifically designed for Python code that will be worked on by AI agents and automated tools.

## General Principles

### 1. Code Clarity and Readability
- **Explicit over Implicit**: Always prefer explicit code over clever or implicit solutions
- **Self-Documenting**: Write code that reads like documentation
- **Consistent Naming**: Use descriptive, consistent naming conventions
- **Avoid Magic**: No magic numbers, strings, or complex one-liners

### 2. Structure and Organization
- **Single Responsibility**: Each function/class should have one clear purpose
- **Logical Grouping**: Group related functionality together
- **Clear Dependencies**: Make dependencies explicit and minimal
- **Separation of Concerns**: Keep business logic separate from infrastructure code

## Naming Conventions

### Variables and Functions
```python
# Good - descriptive and clear
def calculate_tile_probability(tile_type: str, bag_contents: List[str]) -> float:
    pass

# Bad - unclear purpose
def calc(t: str, b: List[str]) -> float:
    pass
```

### Classes
```python
# Good - noun-based, descriptive
class TileBag:
    pass

class ProbabilityCalculator:
    pass

# Bad - unclear or generic
class Handler:
    pass

class Utils:
    pass
```

### Constants
```python
# Good - UPPER_CASE with underscores
MAX_TILES_PER_BAG = 100
DEFAULT_TILE_TYPES = ['red', 'blue', 'green']

# Bad - unclear or inconsistent
maxTiles = 100
default_types = ['red', 'blue', 'green']
```

## Function Design

### 1. Function Signatures
- **Type Hints**: Always include type hints for parameters and return values
- **Default Values**: Use None or sensible defaults, avoid complex default expressions
- **Parameter Order**: Put required parameters first, then optional ones
- **Limit Parameters**: Keep functions to 3-4 parameters maximum

```python
# Good
def draw_tiles(
    bag: TileBag,
    count: int,
    replacement: bool = False,
    seed: Optional[int] = None
) -> List[str]:
    pass

# Bad - too many parameters, unclear types
def draw(bag, count, replacement=False, seed=None, validate=True, log=False):
    pass
```

### 2. Return Values
- **Single Return Type**: Functions should return one consistent type
- **Explicit Returns**: Always use explicit return statements
- **Meaningful Values**: Return values that clearly indicate success/failure

```python
# Good
def validate_tile_bag(bag: TileBag) -> bool:
    if not bag.tiles:
        return False
    return len(bag.tiles) <= bag.max_capacity

# Bad - unclear return meaning
def check_bag(bag: TileBag):
    if not bag.tiles:
        return 0
    return len(bag.tiles)
```

## Error Handling

### 1. Exception Strategy
- **Specific Exceptions**: Use specific exception types, not generic Exception
- **Meaningful Messages**: Include context in exception messages
- **Fail Fast**: Validate inputs early and fail immediately

```python
# Good
def add_tile(bag: TileBag, tile: str) -> None:
    if not isinstance(tile, str):
        raise ValueError(f"Tile must be a string, got {type(tile)}")
    
    if len(bag.tiles) >= bag.max_capacity:
        raise ValueError(f"Bag is full (capacity: {bag.max_capacity})")
    
    bag.tiles.append(tile)

# Bad - generic exception handling
def add_tile(bag: TileBag, tile: str) -> None:
    try:
        bag.tiles.append(tile)
    except Exception as e:
        print(f"Error: {e}")
```

### 2. Input Validation
- **Early Validation**: Validate all inputs at the start of functions
- **Clear Error Messages**: Provide specific, actionable error messages
- **Type Checking**: Use isinstance() for type validation

```python
# Good
def create_tile_bag(tiles: List[str], max_capacity: int) -> TileBag:
    if not isinstance(tiles, list):
        raise TypeError("Tiles must be a list")
    
    if not isinstance(max_capacity, int):
        raise TypeError("Max capacity must be an integer")
    
    if max_capacity <= 0:
        raise ValueError("Max capacity must be positive")
    
    return TileBag(tiles, max_capacity)
```

## Documentation

### 1. Docstrings
- **Always Include**: Every public function/class should have a docstring
- **Google Style**: Use Google-style docstring format
- **Examples**: Include usage examples for complex functions
- **Parameter Documentation**: Document all parameters and return values

```python
def draw_random_tile(bag: TileBag, seed: Optional[int] = None) -> str:
    """Draw a random tile from the bag.
    
    Args:
        bag: The tile bag to draw from
        seed: Optional random seed for reproducible results
        
    Returns:
        The drawn tile as a string
        
    Raises:
        ValueError: If the bag is empty
        
    Example:
        >>> bag = TileBag(['red', 'blue', 'green'])
        >>> draw_random_tile(bag)
        'red'
    """
    if not bag.tiles:
        raise ValueError("Cannot draw from empty bag")
    
    random.seed(seed)
    return random.choice(bag.tiles)
```

### 2. Comments
- **Why, Not What**: Comment on the reasoning, not the obvious
- **Complex Logic**: Explain complex algorithms or business rules
- **Temporary Code**: Mark temporary or experimental code clearly

```python
# Good - explains the reasoning
# Use reservoir sampling for memory-efficient random selection
# when dealing with large datasets
def reservoir_sample(items: List[str], k: int) -> List[str]:
    pass

# Bad - states the obvious
# Loop through items
for item in items:
    pass
```

## Testing Considerations

### 1. Testable Code
- **Dependency Injection**: Make dependencies injectable for testing
- **Pure Functions**: Prefer pure functions when possible
- **Side Effects**: Minimize and isolate side effects
- **Mockable**: Design code to be easily mocked in tests

```python
# Good - dependencies can be injected
class TileBag:
    def __init__(self, tiles: List[str], random_generator=None):
        self.tiles = tiles
        self.random_generator = random_generator or random

# Bad - hard to test due to global state
class TileBag:
    def __init__(self, tiles: List[str]):
        self.tiles = tiles
        # Uses global random module - hard to test
```

### 2. Test Structure
- **Arrange-Act-Assert**: Structure tests with clear sections
- **Descriptive Names**: Test names should describe the scenario
- **One Assertion**: Each test should verify one specific behavior
- **Edge Cases**: Include tests for edge cases and error conditions

```python
# Good
def test_draw_tile_from_empty_bag_raises_error():
    """Test that drawing from empty bag raises appropriate error."""
    # Arrange
    bag = TileBag([])
    
    # Act & Assert
    with pytest.raises(ValueError, match="Cannot draw from empty bag"):
        bag.draw_tile()
```

### 3. Unit Testing Guide
For detailed instructions on adding new unit tests to this project, see the comprehensive guide:
- **Unit Testing Guide**: [.ai/rules/unit_testing_guide.md](.ai/rules/unit_testing_guide.md)

This guide covers:
- Project testing overview and current structure
- Step-by-step instructions for adding new tests
- Testing patterns and best practices used in this project
- Running tests and adding test dependencies
- Complete examples and templates

## Code Organization

### 1. File Structure
- **One Class Per File**: For complex classes, use one file per class
- **Logical Grouping**: Group related functions/classes together
- **Import Organization**: Organize imports (standard library, third-party, local)
- **Clear Boundaries**: Define clear module boundaries

### 2. Module Design
```python
# Good - clear module structure
"""
Tile bag simulation module.

This module provides classes and functions for simulating
random tile drawing from bags with various configurations.
"""

from typing import List, Optional
import random

from .exceptions import EmptyBagError, InvalidTileError
from .models import TileBag, TileType

__all__ = ['TileBag', 'draw_tile', 'create_bag']

def draw_tile(bag: TileBag) -> str:
    """Draw a random tile from the bag."""
    pass
```

## Performance Considerations

### 1. Algorithm Choice
- **Big O Awareness**: Understand time/space complexity
- **Efficient Data Structures**: Choose appropriate data structures
- **Lazy Evaluation**: Use generators for large datasets
- **Caching**: Cache expensive computations when appropriate

### 2. Memory Management
- **Generator Functions**: Use generators for large sequences
- **Context Managers**: Use context managers for resource management
- **Avoid Memory Leaks**: Be careful with closures and circular references

```python
# Good - memory efficient
def tile_generator(bag: TileBag):
    """Generate tiles one at a time to save memory."""
    for tile in bag.tiles:
        yield tile

# Bad - loads everything into memory
def get_all_tiles(bag: TileBag) -> List[str]:
    return list(bag.tiles)
```

## Security and Safety

### 1. Input Sanitization
- **Validate All Inputs**: Never trust external input
- **Escape Output**: Properly escape output when needed
- **Resource Limits**: Set reasonable limits on resource usage

### 2. Error Information
- **Don't Expose Internals**: Error messages shouldn't reveal implementation details
- **Logging**: Use appropriate logging levels
- **Graceful Degradation**: Handle errors gracefully when possible

## Version Control

### 1. Commit Messages
- **Clear and Descriptive**: Write commit messages that explain the "why"
- **Atomic Commits**: Make small, focused commits
- **Conventional Format**: Use conventional commit format when possible

### 2. Code Review
- **Self-Review**: Review your own code before submitting
- **Documentation Updates**: Update documentation with code changes
- **Test Coverage**: Ensure adequate test coverage for changes

## Tools and Automation

### 1. Poetry Usage
- **Always Use Poetry**: All Python-related commands should be run through Poetry
- **Python Interpreter**: Use `poetry run python` instead of `python`
- **Linting and Formatting**: Use `poetry run black`, `poetry run flake8`, `poetry run mypy`
- **Testing**: Use `poetry run pytest` for running tests
- **Package Management**: Use `poetry add` and `poetry remove` for dependencies
- **Environment**: Use `poetry shell` to activate the virtual environment

### 2. Linting and Formatting
- **Black**: Use `poetry run black` for code formatting
- **Flake8**: Use `poetry run flake8` for linting
- **MyPy**: Use `poetry run mypy` for type checking
- **Pre-commit Hooks**: Set up pre-commit hooks for automated checks

### 3. CI/CD
- **Automated Testing**: Run tests automatically on all changes
- **Code Quality**: Include code quality checks in CI
- **Documentation**: Automate documentation generation

## Best Practices Summary

1. **Write for Humans**: Code should be readable and maintainable
2. **Be Explicit**: Avoid clever or implicit solutions
3. **Document Everything**: Include docstrings and comments
4. **Test Thoroughly**: Write comprehensive tests
5. **Handle Errors**: Implement proper error handling
6. **Follow Standards**: Use consistent naming and formatting
7. **Think About Performance**: Consider efficiency without premature optimization
8. **Keep It Simple**: Prefer simple solutions over complex ones
9. **Validate Inputs**: Always validate and sanitize inputs
10. **Use Type Hints**: Include type hints for better tooling support

Remember: Code written for AI agents should be even more explicit and well-documented than code written for human developers alone. The goal is to make the code's intent and behavior crystal clear to both humans and AI tools. 