"""
Test suite to verify the 's' command functionality.
"""

import pytest
import subprocess
import sys
from pathlib import Path


@pytest.fixture
def main_script_path():
    """Get the path to the main.py script."""
    return Path(__file__).parent.parent / "main.py"


def test_s_command_appears_in_help(main_script_path):
    """Test that the 's' command appears in the help output."""
    # Arrange
    commands = "h\nq\n"
    
    # Act
    process = subprocess.Popen(
        [sys.executable, str(main_script_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=commands, timeout=10)
    
    # Assert
    assert "s - Show the state of all loaded decks" in stdout
    assert process.returncode == 0


def test_s_command_produces_status_output(main_script_path):
    """Test that the 's' command produces expected status output."""
    # Arrange
    commands = "s\nq\n"
    
    # Act
    process = subprocess.Popen(
        [sys.executable, str(main_script_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=commands, timeout=10)
    
    # Assert
    assert "Status of all loaded decks" in stdout
    assert process.returncode == 0


def test_s_command_integration_flow(main_script_path):
    """Test the complete flow of help, status, and quit commands."""
    # Arrange
    commands = "h\ns\nq\n"
    
    # Act
    process = subprocess.Popen(
        [sys.executable, str(main_script_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=commands, timeout=10)
    
    # Assert
    assert "s - Show the state of all loaded decks" in stdout
    assert "Status of all loaded decks" in stdout
    assert process.returncode == 0
    assert stderr == ""


def test_s_command_timeout_handling():
    """Test that the subprocess doesn't hang indefinitely."""
    # Arrange
    main_script_path = Path(__file__).parent.parent / "main.py"
    commands = "s\nq\n"
    
    # Act & Assert
    with pytest.raises(subprocess.TimeoutExpired):
        process = subprocess.Popen(
            [sys.executable, str(main_script_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Use a very short timeout to test timeout handling
        stdout, stderr = process.communicate(input=commands, timeout=0.001)