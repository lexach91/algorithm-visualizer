from blessed import Terminal, terminal
import random
import numpy as np
from time import sleep

# create a Terminal instance
terminal = Terminal()

# Constants for the grid colors and dimensions
WALL = "⬜️"
PATH = "🟦"
VISITED = "🟩"
ACTIVE = "🟨"
START = "🧐"
END = "🏁"
EMPTY = "　"

WIDTH = 31
HEIGHT = 21


class Node:
    """
    Class that represents every cell on the grid.
    """

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = EMPTY
        self.neighbors = []
        self.visited = False
        self.passage = False
        self.distance = float("inf")
        self.previous = None

    def __str__(self):
        return self.color

    def get_position(self):
        return self.row, self.col

    def update_neighbors(self, grid):
        self.neighbors = []
        row, col = self.get_position()
        # Node to the top of the current node
        if row > 0 and not grid[row - 1][col].is_wall():
            self.neighbors.append(grid[row - 1][col])
        # Node to the bottom of the current node
        if row < HEIGHT - 1 and not grid[row + 1][col].is_wall():
            self.neighbors.append(grid[row + 1][col])
        # Node to the left of the current node
        if col > 0 and not grid[row][col - 1].is_wall():
            self.neighbors.append(grid[row][col - 1])
        # Node to the right of the current node
        if col < WIDTH - 1 and not grid[row][col + 1].is_wall():
            self.neighbors.append(grid[row][col + 1])

    def is_end(self):
        return self.color == END

    def is_start(self):
        return self.color == START

    def is_wall(self):
        return self.color == WALL

    def is_empty(self):
        return self.color == EMPTY

    def is_visited(self):
        return self.visited

    def is_passage(self):
        return self.passage

    def make_start(self):
        self.color = START

    def make_end(self):
        self.color = END

    def make_wall(self):
        self.color = WALL

    def make_empty(self):
        self.color = EMPTY

    def make_visited(self):
        self.color = VISITED
        self.visited = True

    def make_active(self):
        self.color = ACTIVE

    def make_passage(self):
        self.passage = True
        self.color = EMPTY

    def make_path(self):
        self.color = PATH

    def reset(self):
        self.color = EMPTY
        self.visited = False
        self.passage = False
        self.distance = float("inf")
        self.previous = None

def generate_grid():
    """
    Generates and returns a grid of nodes.
    """
    return np.array([[Node(row, col) for col in range(WIDTH)] for row in range(HEIGHT)])

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
    for i in range(WIDTH):
        grid[0][i].make_wall()
        grid[-1][i].make_wall()

def display_grid(grid):
    """
    Displays the grid in the terminal.
    """
    print(terminal.move(0, 0) + terminal.clear)
    for row in grid:
        print("".join(str(node) for node in row))
    sleep(0.1)

def generate_horizontal_maze(grid):
    """
    Generates a maze with horizontal walls with random passages
    """
    for row in range(2, HEIGHT - 2, 2):
        skip = random.randint(1, WIDTH - 1)
        for col in range(1, WIDTH - 1):
            if col == skip:
                continue
            grid[row][col].make_wall()


def generate_vertical_maze(grid):
    """
    Generates a maze with vertical walls with random passages
    """
    for col in range(2, WIDTH - 2, 2):
        skip = random.randint(1, HEIGHT - 1)
        for i in range(1, HEIGHT - 1):
            grid[:, col][i].make_wall()
        grid[:, col][skip].reset()


def generate_spiral_maze(grid):
    """
    Generates a maze in a form of a spiral
    """
    left = 1
    right = WIDTH - 2
    top = 2
    bottom = HEIGHT - 2

    while left < right and top < bottom:
        if left > right:
            break
        for i in range(left, right):
            grid[top][i].make_wall()
        top += 2
        if top > bottom:
            break
        for i in range(top - 1, bottom):
            grid[i][right - 1].make_wall()
        right -= 2
        if right < left:
            break
        for i in range(right, left, -1):
            grid[bottom - 1][i].make_wall()
        bottom -= 2
        if bottom < top:
            break
        for i in range(bottom, top - 1, -1):
            grid[i][left + 1].make_wall()
        left += 2


def generate_random_pattern(grid):
    """
    Generates randomly placed barriers on the grid.
    """
    for row in range(1, HEIGHT):
        for col in range(1, WIDTH):
            if random.random() < 0.14:
                grid[row][col].make_wall()


def generate_maze_recursive_division(
    grid, row_start, row_end, col_start, col_end, orientation="horizontal"
):
    """
    Generates a maze using recursive division algorithm.
    """
    if row_end - row_start < 2 and col_end - col_start < 2:
        return
    
    if orientation == "horizontal":
        possible_rows = list(range(row_start, row_end + 1, 2))
        possible_cols = list(range(col_start - 1, col_end + 2, 2))
        current_row = random.choice(possible_rows)
        col_to_skip = random.choice(possible_cols)
        for col in range(col_start - 1, col_end + 2):
            grid[current_row][col].make_wall()
            if col == col_to_skip:
                grid[current_row][col].make_empty()
                continue
            display_grid(grid)
            
        if current_row - 2 - row_start > col_end - col_start:
            generate_maze_recursive_division(grid, row_start, current_row - 2, col_start, col_end, "horizontal")
        else:
            generate_maze_recursive_division(grid, row_start, current_row - 2, col_start, col_end, "vertical")
            
        if row_end - current_row - 2 > col_end - col_start:
            generate_maze_recursive_division(grid, current_row + 2, row_end, col_start, col_end, "horizontal")
        else:
            generate_maze_recursive_division(grid, current_row + 2, row_end, col_start, col_end, "vertical")

    else:
        possible_rows = list(range(row_start - 1, row_end + 2, 2))
        possible_cols = list(range(col_start, col_end + 1, 2))
        row_to_skip = random.choice(possible_rows)
        current_col = random.choice(possible_cols)
        for row in range(row_start - 1, row_end + 2):
            grid[row][current_col].make_wall()
            if row == row_to_skip:
                grid[row][current_col].make_empty()
                continue
            display_grid(grid)
            
        if row_end - row_start > current_col - 2 - col_start:
            generate_maze_recursive_division(grid, row_start, row_end, col_start, current_col - 2, "horizontal")
        else:
            generate_maze_recursive_division(grid, row_start, row_end, col_start, current_col - 2, "vertical")
            
        if row_end - row_start > col_end - current_col - 2:
            generate_maze_recursive_division(grid, row_start, row_end, current_col + 2, col_end, "horizontal")
        else:
            generate_maze_recursive_division(grid, row_start, row_end, current_col + 2, col_end, "vertical")

def draw_path(grid, end_node):
    """
    Draws path from the end node to the start node on the grid.
    """
    current_node = end_node
    while current_node.previous:
        if current_node == end_node:
            end_node.make_end()
            current_node = current_node.previous
            continue
        current_node.make_path()
        current_node = current_node.previous
        display_grid(grid)

def dijkstra(grid, start_node, end_node):
    """
    Searches for the shortest path from the start node to the end node using Dijkstra's algorithm.
    """
    update_all_neighbors(grid)
    start_node.distance = 0
    # start_node.make_visited()
    start_node.previous = None
    nodes_to_visit = [start_node]
    
    while nodes_to_visit:
        current_node = nodes_to_visit.pop(0)
        
        if current_node == end_node:
            draw_path(grid, end_node)
            return
        
        for neighbor in current_node.neighbors:
            distance_from_start = current_node.distance + 1
            
            if distance_from_start < neighbor.distance:
                neighbor.previous = current_node
                neighbor.distance = distance_from_start
                
                if neighbor not in nodes_to_visit:
                    nodes_to_visit.append(neighbor)
                    neighbor.make_active()
                    
        if current_node != start_node:
            current_node.make_visited()
            display_grid(grid)
            
def main():
    """
    Main function.
    """
    grid = generate_grid()
    reset_grid(grid)
    
    generate_maze_recursive_division(grid, 2, HEIGHT - 2, 2, WIDTH - 2, "horizontal")
    
    start = grid[1][1]
    end = grid[-2][-2]
    start.make_start()
    end.make_end()
    
    dijkstra(grid, start, end)
    
if __name__ == "__main__":
    main()