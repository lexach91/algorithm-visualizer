"""
Functions for maze generation.
"""
import random
from constants import WIDTH, HEIGHT
from grid_functions import display_grid

def generate_horizontal_maze(grid):
    """
    Generates a maze with horizontal walls with random passages
    """
    for row in range(2, HEIGHT - 2, 2):
        skip = random.randint(1, WIDTH - 2)
        for col in range(1, WIDTH - 1):
            if col == skip:
                continue
            grid[row][col].make_wall()
            display_grid(grid)


def generate_vertical_maze(grid):
    """
    Generates a maze with vertical walls with random passages
    """
    for col in range(2, WIDTH - 2, 2):
        skip = random.randint(1, HEIGHT - 2)
        for i in range(1, HEIGHT - 1):
            # Using numpy slicing here to easily get the column.
            grid[:, col][i].make_wall()
            display_grid(grid)
        grid[:, col][skip].reset()


def generate_spiral_maze(grid):
    """
    Generates a maze in a form of a spiral
    """
    left = 1  # Start from the left border
    right = WIDTH - 2  # Finish two columns from the right border
    top = 2  # Start two rows from the top
    bottom = HEIGHT - 2  # Finish two rows from the bottom

    while left < right and top < bottom:
        if left > right:
            break
        for i in range(left, right):  # Drawing wall from left to right
            grid[top][i].make_wall()
            display_grid(grid)
        top += 2  # Moving to the next row down leaving a gap
        if top > bottom:
            break
        for i in range(top - 1, bottom):  # Drawing wall from top to bottom
            grid[i][right - 1].make_wall()
            display_grid(grid)
        right -= 2  # Moving to the next column to the left leaving a gap
        if right < left:
            break
        for i in range(right, left, -1):  # Drawing wall from right to left
            grid[bottom - 1][i].make_wall()
            display_grid(grid)
        bottom -= 2  # Moving to the next row up leaving a gap
        if bottom < top:
            break
        for i in range(bottom, top - 1, -1):  # Drawing wall from bottom to top
            grid[i][left + 1].make_wall()
            display_grid(grid)
        left += 2  # Moving to the next column to the right leaving a gap


def generate_random_pattern(grid):
    """
    Generates randomly placed barriers on the grid.
    """
    for row in range(1, HEIGHT):
        for col in range(1, WIDTH):
            if random.random() < 0.14:  # 0.14 is the probability of a barrier
                grid[row][col].make_wall()
        display_grid(grid)


def generate_maze_recursive_division(
    grid, row_start, row_end, col_start, col_end, orientation="horizontal"
):
    """
    Generates a maze using recursive division algorithm.
    """
    if row_end - row_start < 0 and col_end - col_start < 0:  # Stop condition
        return
    # Horizontal division
    if orientation == "horizontal":
        # Adding every second row to the list
        possible_rows = list(range(row_start, row_end + 1, 2))
        # Adding every second column to the list
        possible_cols = list(range(col_start - 1, col_end + 2, 2))
        # Randomly choosing a row for a wall
        current_row = random.choice(possible_rows)
        # Randomly choosing a column for a passage
        col_to_skip = random.choice(possible_cols)
        for col in range(col_start - 1, col_end + 2):
            grid[current_row][col].make_wall()
            if col == col_to_skip:
                grid[current_row][col].make_empty()
                continue
            display_grid(grid)
        # Checking upper and lower parts of the grid
        # if we need to divide it horizontally or vertically
        # and recursively calling the function

        # If height of the upper part is greater than width,
        # we divide horizontally
        if current_row - 2 - row_start > col_end - col_start:
            generate_maze_recursive_division(
                grid,
                row_start,
                current_row - 2,
                col_start,
                col_end,
                "horizontal"
            )
        # If width of the upper part is greater than height,
        # we divide vertically
        else:
            generate_maze_recursive_division(
                grid,
                row_start,
                current_row - 2,
                col_start,
                col_end,
                "vertical"
            )
        # If height of the lower part is greater than width,
        # we divide horizontally
        if row_end - current_row - 2 > col_end - col_start:
            generate_maze_recursive_division(
                grid,
                current_row + 2,
                row_end,
                col_start,
                col_end,
                "horizontal"
            )
        # If width of the lower part is greater than height,
        # we divide vertically
        else:
            generate_maze_recursive_division(
                grid, current_row + 2, row_end, col_start, col_end, "vertical"
            )
    # Vertical division
    else:
        # Adding every second row to the list
        possible_rows = list(range(row_start - 1, row_end + 2, 2))
        # Adding every second column to the list
        possible_cols = list(range(col_start, col_end + 1, 2))
        # Randomly choosing a row for a passage
        row_to_skip = random.choice(possible_rows)
        # Randomly choosing a column for a wall
        current_col = random.choice(possible_cols)
        for row in range(row_start - 1, row_end + 2):
            grid[row][current_col].make_wall()
            if row == row_to_skip:
                grid[row][current_col].make_empty()
                continue
            display_grid(grid)
        # Checking left and right parts of the grid
        # if we need to divide it horizontally or vertically
        # and recursively calling the function

        # If height of the left part is greater than width,
        # we divide horizontally
        if row_end - row_start > current_col - 2 - col_start:
            generate_maze_recursive_division(
                grid,
                row_start,
                row_end,
                col_start,
                current_col - 2,
                "horizontal"
            )
        # If width of the left part is greater than height,
        # we divide vertically
        else:
            generate_maze_recursive_division(
                grid,
                row_start,
                row_end,
                col_start,
                current_col - 2,
                "vertical"
            )
        # If height of the right part is greater than width,
        # we divide horizontally
        if row_end - row_start > col_end - current_col - 2:
            generate_maze_recursive_division(
                grid,
                row_start,
                row_end,
                current_col + 2,
                col_end,
                "horizontal"
            )
        # If width of the right part is greater than height,
        # we divide vertically
        else:
            generate_maze_recursive_division(
                grid,
                row_start,
                row_end,
                current_col + 2,
                col_end,
                "vertical"
            )
