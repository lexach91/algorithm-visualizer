"""
Module for grid functions.
"""
from time import sleep
import numpy as np
from constants import WIDTH, HEIGHT, terminal
from node_class import Node


def generate_grid():
    """
    Generates and returns a grid of nodes as a 2D numpy array.
    """
    return np.array(
        [[Node(row, col) for col in range(WIDTH)] for row in range(HEIGHT)]
        )


def update_all_neighbors(grid):
    """
    Updates neighbors of all nodes on the grid.
    """
    for row in grid:
        for node in row:
            node.update_neighbors(grid)


def reset_grid(grid):
    """
    Resets all nodes on the grid to its initial state.
    After that creates a wall border around the grid.
    """
    for row in grid:
        for node in row:
            node.reset()
    for i in range(HEIGHT):
        grid[i][0].make_wall()
        grid[i][-1].make_wall()
        display_grid(grid)
    for i in range(WIDTH):
        grid[0][i].make_wall()
        grid[-1][i].make_wall()
        display_grid(grid)


def reset_grid_partially(grid):
    """
    Resets visited and active nodes on the grid
    before running another algorithm.
    """
    for row in grid:
        for node in row:
            if (
                node.is_visited() or
                node.is_active() or
                node.is_path() and not
                node.is_end() and not
                node.is_start()
            ):
                node.reset()


def display_grid(grid):
    """
    Displays the grid in the terminal.
    """
    with terminal.hidden_cursor():
        print(terminal.home + terminal.clear)
        for row in grid:
            print(" ".join(str(node) for node in row))
        sleep(0.15)


def display_prepared_grid(start_node, end_node, grid):
    """
    Places the start and end nodes on the grid and displays it.
    """
    start_node.make_start()
    end_node.make_end()
    display_grid(grid)


def place_start_node_manually(grid):
    """
    Allows user to place start node on the grid manually.
    """
    # Making sure that the start node is not on the grid
    start_node = None
    # Creating a variable to place temporary start node on the grid,
    # and coloring it as START
    temp_start = grid[1][1]
    temp_start.make_start()
    # terminal.cbreak() makes the terminal read key presses instantly
    # terminal.hidden_cursor() hides the cursor from the screen
    with terminal.cbreak(), terminal.hidden_cursor():
        # While the start node is not placed on the grid
        while not start_node:
            # Every iteration we clear the screen
            print(terminal.home + terminal.clear)
            # And display the grid
            # The reason why the function display_grid() is not used here
            # is because it contains sleep() function, which we don't need here
            for row in grid:
                print(" ".join(str(node) for node in row))
            # Displaying the instructions to the user under the grid
            print(
                terminal.bold +
                terminal.yellow +
                "Place the start node." +
                terminal.normal
                )
            print("Use ARROW keys to move around the grid.")
            print("Press ENTER to place the start node.")
            print("Press ESC to cancel the start node placement.")
            # Variable to store the key pressed by the user
            key_pressed = terminal.inkey(timeout=0.1)
            # If the user pressed any of the arrow keys,
            # we check if the node can be moved there.
            # If it can, we make the temporary start node EMPTY,
            # and move the temporary start node to the new position,
            # coloring it as START.
            if key_pressed.code == terminal.KEY_UP:
                if (
                    temp_start.row > 1 and
                    grid[temp_start.row - 1][temp_start.col].is_empty()
                ):
                    temp_start.make_empty()
                    temp_start = grid[temp_start.row - 1][temp_start.col]
                    temp_start.make_start()
            elif key_pressed.code == terminal.KEY_DOWN:
                if (
                    temp_start.row < HEIGHT - 2 and
                    grid[temp_start.row + 1][temp_start.col].is_empty()
                ):
                    temp_start.make_empty()
                    temp_start = grid[temp_start.row + 1][temp_start.col]
                    temp_start.make_start()
            elif key_pressed.code == terminal.KEY_LEFT:
                if (
                    temp_start.col > 1 and
                    grid[temp_start.row][temp_start.col - 1].is_empty()
                ):
                    temp_start.make_empty()
                    temp_start = grid[temp_start.row][temp_start.col - 1]
                    temp_start.make_start()
            elif key_pressed.code == terminal.KEY_RIGHT:
                if (
                    temp_start.col < WIDTH - 2 and
                    grid[temp_start.row][temp_start.col + 1].is_empty()
                ):
                    temp_start.make_empty()
                    temp_start = grid[temp_start.row][temp_start.col + 1]
                    temp_start.make_start()
            # If the user pressed ENTER, we return the start node
            elif key_pressed.code == terminal.KEY_ENTER:
                return temp_start
            # If the user pressed ESC, we make the temporary start node EMPTY,
            # and return None
            elif key_pressed.code == terminal.KEY_ESCAPE:
                temp_start.make_empty()
                return None
            # For any other key, we do nothing
            else:
                continue


def place_end_node_manually(grid):
    """
    Allows user to place end node on the grid manually.
    """
    # Making sure that the end node is not on the grid
    end_node = None
    # Creating a variable for the temporary end node.
    temp_end = None
    # Looping through the grid to find the first empty node.
    for row in grid:
        for node in row:
            if node.is_empty():
                temp_end = node
    # Color the temporary end node as END
    temp_end.make_end()
    # terminal.cbreak() makes the terminal read key presses instantly
    # terminal.hidden_cursor() hides the cursor from the screen
    with terminal.cbreak(), terminal.hidden_cursor():
        # While the end node is not placed on the grid
        while not end_node:
            # Every iteration we clear the screen
            print(terminal.home + terminal.clear)
            # And display the grid
            # The reason why the function display_grid() is not used here
            # is because it contains sleep() function, which we don't need here
            for row in grid:
                print(" ".join(str(node) for node in row))
            # Displaying the instructions to the user under the grid
            print(
                terminal.bold +
                terminal.yellow +
                "Place the end node." +
                terminal.normal
                )
            print("Use ARROW keys to move around the grid.")
            print("Press ENTER to place the end node.")
            print("Press ESC to cancel the end node placement.")
            # Variable to store the key pressed by the user
            key_pressed = terminal.inkey(timeout=0.1)
            # If the user pressed any of the arrow keys,
            # we check if the node can be moved there.
            # If it can, we make the temporary end node EMPTY,
            # and move the temporary end node to the new position,
            # coloring it as END.
            if key_pressed.code == terminal.KEY_UP:
                if (
                    temp_end.row > 1 and
                    grid[temp_end.row - 1][temp_end.col].is_empty()
                ):
                    temp_end.make_empty()
                    temp_end = grid[temp_end.row - 1][temp_end.col]
                    temp_end.make_end()
            elif key_pressed.code == terminal.KEY_DOWN:
                if (
                    temp_end.row < HEIGHT - 2 and
                    grid[temp_end.row + 1][temp_end.col].is_empty()
                ):
                    temp_end.make_empty()
                    temp_end = grid[temp_end.row + 1][temp_end.col]
                    temp_end.make_end()
            elif key_pressed.code == terminal.KEY_LEFT:
                if (
                    temp_end.col > 1 and
                    grid[temp_end.row][temp_end.col - 1].is_empty()
                ):
                    temp_end.make_empty()
                    temp_end = grid[temp_end.row][temp_end.col - 1]
                    temp_end.make_end()
            elif key_pressed.code == terminal.KEY_RIGHT:
                if (
                    temp_end.col < WIDTH - 2 and
                    grid[temp_end.row][temp_end.col + 1].is_empty()
                ):
                    temp_end.make_empty()
                    temp_end = grid[temp_end.row][temp_end.col + 1]
                    temp_end.make_end()
            # If the user pressed ENTER, we return the end node
            elif key_pressed.code == terminal.KEY_ENTER:
                end_node = temp_end
                return end_node
            # If the user pressed ESC, we make the temporary end node EMPTY,
            # and return None
            elif key_pressed.code == terminal.KEY_ESCAPE:
                temp_end.make_empty()
                return None
            # For any other key, we do nothing
            else:
                continue
