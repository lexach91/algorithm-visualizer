"""
Constants for the project.
"""
from blessed import Terminal

# Instance of Terminal to use in the project
terminal = Terminal()

# Constants for the project
WALL = "⬜️"
PATH = "🟦"
VISITED = "🟩"
ACTIVE = "🟨"
START = "🧐"
END = "🏁"
# EMPTY = "　" # This line should be used when the app is running on desktop
EMPTY = " " # This line should be used when the app is running on heroku

WIDTH = 25
HEIGHT = 19
