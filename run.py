from time import sleep
import random
import numpy as np
from blessed import Terminal, terminal
from simple_term_menu import TerminalMenu

# create a Terminal instance
terminal = Terminal()

# Constants for the grid colors and dimensions of the grid
WALL = "⬜️"
PATH = "🟦"
VISITED = "🟩"
ACTIVE = "🟨"
START = "🧐"
END = "🏁"
# EMPTY = "　"
EMPTY = " "

WIDTH = 25
HEIGHT = 19


class Node:
    """
    Class that represents every cell on the grid.
    """

    def __init__(self, row, col):
        # Row and column position of the node
        self.row = row
        self.col = col
        # Color (state) of the node. Node is empty by default.
        self.color = EMPTY
        # Empty list to store neighbors of the node in the future.
        self.neighbors = []
        # Distance from the start node to the current node.
        # Infinity by default. Used in all pathfinding algorithms.
        self.distance = float("inf")
        # Variable to store the previous node in the path.
        # Used in all pathfinding algorithms.
        self.previous = None
        # Variable to store the next node in the path.
        # Used in bidirectional BFS.
        self.next = None
        # Variable to store the manhattan distance to the end node.
        # Used in A* algorithm.
        self.manhattan_distance = float("inf")
        # Variable to store the total cost of traveling through this node.
        # Used in A* algorithm.
        self.total_cost = float("inf")

    def __str__(self):
        # Need this method to print the node.
        return self.color

    def get_position(self):
        """
        Returns the position of the node as a tuple.
        """
        return self.row, self.col

    def update_neighbors(self, grid):
        """
        Updates the neighbors of the current node skipping the walls.
        """
        # reset the neighbors list
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
        """
        Returns True if the node is the end node.
        """
        return self.color == END

    def is_start(self):
        """
        Returns True if the node is the start node.
        """
        return self.color == START

    def is_wall(self):
        """
        Returns True if the node is a wall.
        """
        return self.color == WALL

    def is_empty(self):
        """
        Returns True if the node is empty.
        """
        return self.color == EMPTY

    def is_visited(self):
        """
        Returns True if the node has been visited.
        """
        return self.color == VISITED

    def is_path(self):
        """
        Returns True if the node is a path.
        """
        return self.color == PATH

    def is_active(self):
        """
        Returns True if the node is the active node.
        """
        return self.color == ACTIVE

    def make_start(self):
        """
        Makes the node the start node.
        """
        self.color = START

    def make_end(self):
        """
        Makes the node the end node.
        """
        self.color = END

    def make_wall(self):
        """
        Makes the node a wall.
        """
        self.color = WALL

    def make_empty(self):
        """
        Makes the node empty.
        """
        self.color = EMPTY

    def make_visited(self):
        """
        Makes the node visited.
        """
        self.color = VISITED

    def make_active(self):
        """
        Makes the node active.
        """
        self.color = ACTIVE

    def make_path(self):
        """
        Makes the node a path.
        """
        self.color = PATH

    def reset(self):
        """
        Resets the node to its initial state.
        """
        self.color = EMPTY
        self.distance = float("inf")
        self.manhattan_distance = float("inf")
        self.total_cost = float("inf")
        self.previous = None
        self.next = None


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
    if row_end - row_start < 2 and col_end - col_start < 2:  # Stop condition
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


def draw_path(grid, end_node):
    """
    Draws path from the end node to the start node on the grid.
    """
    current_node = end_node
    # Keep calling the previous node until we reach the start node
    while current_node.previous:
        # Skipping the end node
        if current_node == end_node:
            end_node.make_end()
            current_node = current_node.previous
            continue
        # Drawing the path from current node to the previous node
        current_node.make_path()
        # Changing the current node to the previous node
        current_node = current_node.previous
        # Displaying the grid every iteration to animate the process
        display_grid(grid)
        print("Path found!")


def dijkstra(grid, start_node, end_node):
    """
    Searches for the shortest path from the start node to the end node
    using Dijkstra's algorithm.
    """
    # Flag to check if the path was found
    path_found = False
    # Resetting the grid from previous searches
    reset_grid_partially(grid)
    # Updating neighbors of all nodes
    update_all_neighbors(grid)
    # Checking if the start node and the end node are neighbors
    if start_node in end_node.neighbors:
        print(terminal.home + terminal.clear)
        display_grid(grid)
        print("The start and the end node are neighbors!")
        return
    # Setting distance of the start node to 0
    start_node.distance = 0
    # Resetting the distance of the end node to infinity
    end_node.distance = float("inf")
    # Setting the previous node of the start node to None
    start_node.previous = None
    # Creating a list of nodes we need to visit
    # and placing the start node in it
    nodes_to_visit = [start_node]

    # While we still have nodes to visit
    while nodes_to_visit:
        # Choosing the first node in the list as the current node
        # and removing it from the list
        current_node = nodes_to_visit.pop(0)

        for neighbor in current_node.neighbors:
            # Creating a variable for the distance from the start node
            # and setting it to the distance of the current node + 1
            distance_from_start = current_node.distance + 1
            # If the distance is less than the distance of the neighbor
            if distance_from_start < neighbor.distance:
                # Setting current node as the previous node of the neighbor
                neighbor.previous = current_node
                # Setting the distance of the neighbor
                # to the distance from the start node
                neighbor.distance = distance_from_start
                if neighbor not in nodes_to_visit:
                    # Adding the neighbor to the list of nodes to visit
                    nodes_to_visit.append(neighbor)
                    if neighbor == end_node:
                        # If the neighbor is the end node,
                        # we found the path and we call the function to draw it
                        draw_path(grid, neighbor)
                        path_found = True
                        return  # Empty return statement to exit the function
                    # If the neighbor is not the end node,
                    # we color it as ACTIVE
                    neighbor.make_active()

        if current_node != start_node:
            # After visiting the node, we color it as VISITED
            current_node.make_visited()
            # Displaying the grid every iteration to animate the process
            display_grid(grid)
    if not path_found:
        # If after the loop the path was not found,
        # we let the user know about it
        print("No path found. The end or the start node is blocked.")


def manhattan_distance(node1, node2):
    """
    Calculates the manhattan distance between two nodes.
    """
    return abs(node1.row - node2.row) + abs(node1.col - node2.col)


def closest_node(nodes):
    """
    Returns the node in the list of nodes with minimal total cost.
    """
    # Using lambda function to easily access the total cost of the node.
    return min(nodes, key=lambda node: node.total_cost)


def a_star(grid, start_node, end_node):
    """
    Searches for the shortest path from the start node to the end node
    using A* algorithm.
    """
    # Flag to check if the path was found
    path_found = False
    # Resetting the grid from previous searches
    reset_grid_partially(grid)
    # Updating neighbors of all nodes
    update_all_neighbors(grid)
    # Checking if the start node and the end node are neighbors
    if start_node in end_node.neighbors:
        print(terminal.home + terminal.clear)
        display_grid(grid)
        print("The start and the end node are neighbors!")
        return
    # Setting distance of the start node to 0
    start_node.distance = 0
    # Calculating the manhattan distance from the start node to the end node
    start_node.manhattan_distance = manhattan_distance(start_node, end_node)
    # Setting the total cost of the start node
    # to sum of its distance and manhattan distance
    start_node.total_cost = start_node.distance + start_node.manhattan_distance
    # Resetting the distance of the end node to infinity
    end_node.distance = float("inf")
    # Setting the previous node of the start node to None
    start_node.previous = None
    # Creating a list of nodes we need to visit
    nodes_to_visit = [start_node]
    # While we still have nodes to visit
    while nodes_to_visit:
        # Choosing the node with minimal total cost as the current node
        current_node = closest_node(nodes_to_visit)
        # and removing it from the list
        nodes_to_visit.remove(current_node)

        for neighbor in current_node.neighbors:
            # Creating variables for the distance from the start node,
            # manhattan distance and total cost
            distance_from_start = current_node.distance + 1
            manhattan_distance_from_end = manhattan_distance(
                neighbor,
                end_node
                )
            total_cost = distance_from_start + manhattan_distance_from_end
            # If the distance is less than the distance of the neighbor
            if distance_from_start < neighbor.distance:
                # Setting current node as the previous node of the neighbor
                neighbor.previous = current_node
                # Setting the distance, manhattan distance
                # and total cost of the neighbor
                neighbor.distance = distance_from_start
                neighbor.manhattan_distance = manhattan_distance_from_end
                neighbor.total_cost = total_cost
                if neighbor not in nodes_to_visit:
                    # Adding the neighbor to the list of nodes to visit
                    nodes_to_visit.append(neighbor)
                    if neighbor == end_node:
                        # If the neighbor is the end node,
                        # we found the path and we call the function to draw it
                        draw_path(grid, neighbor)
                        path_found = True
                        return
                    # If the neighbor is not the end node,
                    # we color it as ACTIVE
                    neighbor.make_active()

        if current_node != start_node:
            # After visiting the node, we color it as VISITED
            current_node.make_visited()
            # Displaying the grid every iteration to animate the process
            display_grid(grid)
    if not path_found:
        # If after the loop the path was not found,
        # we let the user know about it
        print("No path found. The end or the start node is blocked.")


def draw_path_bidirectional(grid, intersection_node):
    """
    Draws the path from the intersection node
    to the start and end nodes simultaneously.
    """
    # First we make the intersection node the path.
    intersection_node.make_path()
    # Accessing the previous node of the intersection node.
    forward = intersection_node.previous
    # Accessing the next node of the intersection node.
    backward = intersection_node.next
    # Flag to continue drawing the path
    drawing = True
    while drawing:
        # Check if the forward node has a previous node
        if forward.previous:
            # If so, we make it the path
            forward.make_path()
            # And we access the previous node of the forward node
            forward = forward.previous
        # Check if the backward node has a next node
        if backward.next:
            # If so, we make it the path
            backward.make_path()
            # And we access the next node of the backward node
            backward = backward.next
        # We stop if the forward node has no previous node
        # and the backward node has no next node
        if not forward.previous and not backward.next:
            drawing = False
        # Displaying the grid every iteration to animate the process
        display_grid(grid)


def bidirectional_breadth_first_search(grid, start_node, end_node):
    """
    Searches for the shortest path from the start node to the end node
    using bidirectional breadth-first search algorithm.
    """
    # Flag to check if the path was found
    path_found = False
    # Resetting the grid from previous searches
    reset_grid_partially(grid)
    # Updating neighbors of all nodes
    update_all_neighbors(grid)
    # Checking if the start node and the end node are neighbors
    if start_node in end_node.neighbors:
        print(terminal.home + terminal.clear)
        display_grid(grid)
        print("The start and the end node are neighbors!")
        return
    # Setting distance of the start node to 0
    start_node.distance = 0
    # Setting distance of the end node to 0
    end_node.distance = 0
    # Resetting the previous and next nodes
    # of the start node and the end node
    start_node.previous = None
    start_node.next = None
    end_node.previous = None
    end_node.next = None
    # Creating two lists of nodes we need to visit from both directions
    nodes_to_visit = [start_node]
    nodes_to_visit_reverse = [end_node]
    while nodes_to_visit and nodes_to_visit_reverse:
        # Creating variables for current nodes from both lists
        current_node_forward = nodes_to_visit.pop(0)
        current_node_reverse = nodes_to_visit_reverse.pop(0)

        for neighbor in current_node_forward.neighbors:
            # Creating variable for the distance from the start node
            distance_from_start = current_node_forward.distance + 1
            if neighbor.next:
                # If the neighbor has a next node, it means
                # that it has been visited from the backward direction
                # Setting neighbor's previous node to the current node forward
                neighbor.previous = current_node_forward
                # Setting the next node of the current node forward
                # as the neighbor.
                current_node_forward.next = neighbor
                # And calling the function to draw the path
                draw_path_bidirectional(grid, neighbor)
                path_found = True
                # Empty return statement to break the loop
                return
            # If the distance from the start node is less
            # than the distance of the neighbor
            if distance_from_start < neighbor.distance:
                # Setting the previous node of the neighbor
                neighbor.previous = current_node_forward
                # Setting the distance of the neighbor
                neighbor.distance = distance_from_start
                # If the neighbor is not in the list of nodes to visit
                if neighbor not in nodes_to_visit:
                    # Adding the neighbor to the list of nodes to visit
                    nodes_to_visit.append(neighbor)
                    # Color the neighbor as ACTIVE
                    neighbor.make_active()

        for neighbor in current_node_reverse.neighbors:
            # Creating variable for the distance from the end node
            distance_from_end = current_node_reverse.distance + 1
            if neighbor.previous:
                # If the neighbor has a previous node, it means
                # that it has been visited from the forward direction.
                # Setting neighbor's next node to the current node reverse
                neighbor.next = current_node_reverse
                # Setting the previous node of the current node reverse
                # as the neighbor.
                current_node_reverse.previous = neighbor
                # And calling the function to draw the path
                draw_path_bidirectional(grid, neighbor)
                path_found = True
                # Empty return statement to break the loop
                return
            # If the distance from the end node is less
            # than the distance of the neighbor
            if distance_from_end < neighbor.distance:
                # Setting the next node of the neighbor
                neighbor.next = current_node_reverse
                # Setting the distance of the neighbor
                neighbor.distance = distance_from_end
                # If the neighbor is not in the list of nodes to visit
                if neighbor not in nodes_to_visit_reverse:
                    # Adding the neighbor to the list of nodes to visit
                    nodes_to_visit_reverse.append(neighbor)
                    # Color the neighbor as ACTIVE
                    neighbor.make_active()

        # Color all nodes we visited as VISITED,
        # except the start and end nodes
        if current_node_forward != start_node:
            current_node_forward.make_visited()
        if current_node_reverse != end_node:
            current_node_reverse.make_visited()
        # Displaying the grid every iteration to animate the process
        display_grid(grid)
    # If after the loop the path was not found,
    # we let the user know about it.
    if not path_found:
        print("No path found. The end or the start node is blocked.")


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
            print("Place the start node.")
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
            print("Place the end node.")
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


def main():
    """
    Main function.
    """
    # Variable for the grid
    grid = generate_grid()
    # Variable for the start node
    start_node = None
    # Variable for the end node
    end_node = None
    # Flag to check if any patter has been generated on the grid.
    pattern_generated = False

    # List of options for the main menu
    options_main = [
        "Grid options",
        "Place start and end node",
        "Pathfinder algorithms",
        "Exit",
    ]
    # List of options for the grid options menu
    options_grid = [
        "Empty grid",
        "Random pattern",
        "Maze with vertical walls",
        "Maze with horizontal walls",
        "Maze with spiral pattern",
        "Maze recursive division",
        "Go back",
    ]
    # List of options for the start and end node placement menu
    options_start_end = [
        "Place by default",
        "Place randomly",
        "Place manually",
        "Go back",
    ]
    # List of options for the pathfinder algorithms menu
    options_pathfinder = [
        "Dijkstra's algorithm",
        "A* algorithm",
        "Bi-directional BFS",
        "Go back",
    ]
    # Variable for all menus.
    main_menu = TerminalMenu(
        options_main,
        title="Main menu"
        )
    grid_menu = TerminalMenu(
        options_grid,
        title="Grid menu"
        )
    start_end_menu = TerminalMenu(
        options_start_end,
        title="Start and end node menu"
        )
    pathfinder_menu = TerminalMenu(
        options_pathfinder,
        title="Pathfinder menu"
        )

    # Flag to check if the app is running.
    app_running = True

    while app_running:
        # First we show the main menu to the user,
        # and store the user's choice to the variable.
        user_choice = main_menu.show()
        # We check what the user chose and change the menu accordingly
        if options_main[user_choice] == "Grid options":
            user_choice = grid_menu.show()
            if options_grid[user_choice] == "Empty grid":
                # For empty grid, we just call reset_grid function
                # to draw a border wall on the grid.
                reset_grid(grid)
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Random pattern":
                reset_grid(grid)
                # For random pattern, we call generate_random_pattern function
                generate_random_pattern(grid)
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Maze with vertical walls":
                reset_grid(grid)
                # For maze with vertical walls,
                # we call generate_maze_vertical_walls function
                generate_vertical_maze(grid)
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Maze with horizontal walls":
                reset_grid(grid)
                # For maze with horizontal walls,
                # we call generate_maze_horizontal_walls function
                generate_horizontal_maze(grid)
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Maze with spiral pattern":
                reset_grid(grid)
                # For maze with spiral pattern,
                # we call generate_maze_spiral_pattern function
                generate_spiral_maze(grid)
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Maze recursive division":
                reset_grid(grid)
                # For maze with recursive division,
                # we call generate_maze_recursive_division function
                # and pass the grid, the start row, the end row,
                # the start column, the end column, and the orientation.
                # start_row and start_col equal to 2,
                # because we want not to touch the border walls and
                # first row and column.
                # end_row equal to HEIGHT - 2,
                # end_col equal to WIDTH - 2,
                # because we want not to touch the border walls and
                # last row and column,
                # orientation equal to "horizontal",
                # because we want to start with creating a horizontal wall.
                generate_maze_recursive_division(
                    grid, 2, HEIGHT - 2, 2, WIDTH - 2, "horizontal"
                )
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Go back":
                # If the user chose to go back, we display the main menu again.
                user_choice = main_menu.show()
        elif options_main[user_choice] == "Place start and end node":
            user_choice = start_end_menu.show()
            if (
                options_start_end[user_choice] != "Go back" and not
                pattern_generated
            ):
                # If the user chose to place start and end node,
                # but the pattern has not been generated yet,
                # we let the user know that pattern must be generated first.
                display_grid(grid)
                print("No pattern generated yet.")
            elif options_start_end[user_choice] == "Place by default":
                # First we partially reset the grid,
                # to clean it after the previous pathfinding algorithm runs,
                # but not touching the pattern.
                reset_grid_partially(grid)
                # If start and end already exist, we reset them.
                if start_node:
                    start_node.reset()
                    start_node = None
                if end_node:
                    end_node.reset()
                    end_node = None
                # By default, we place the start node at the top left corner
                # and the end node at the bottom right corner.
                start_node = grid[1][1]
                end_node = grid[HEIGHT - 2][WIDTH - 2]
                # Calling the function to draw the start and end node
                # and display the grid.
                display_prepared_grid(start_node, end_node, grid)
            elif options_start_end[user_choice] == "Place randomly":
                # First we partially reset the grid,
                # to clean it after the previous pathfinding algorithm runs
                # but not touching the pattern.
                reset_grid_partially(grid)
                # Creating variable to store possible nodes.
                possible_nodes = []
                # If start and end already exist, we reset them.
                if start_node:
                    start_node.reset()
                    start_node = None
                if end_node:
                    end_node.reset()
                    end_node = None
                # Loop to add all empty nodes to the list.
                for row in grid:
                    for node in row:
                        if node.is_empty():
                            possible_nodes.append(node)
                # Randomly choosing start node from the list.
                start_node = random.choice(possible_nodes)
                # Removing the start node from the list.
                possible_nodes.remove(start_node)
                # Randomly choosing end node from the list.
                end_node = random.choice(possible_nodes)
                # Calling the function to draw the start and end node
                # and display the grid.
                display_prepared_grid(start_node, end_node, grid)
            elif options_start_end[user_choice] == "Place manually":
                # First we partially reset the grid,
                # to clean it after the previous pathfinding algorithm runs
                # but not touching the pattern.
                reset_grid_partially(grid)
                # If start and end already exist, we reset them.
                if start_node:
                    start_node.reset()
                    start_node = None
                if end_node:
                    end_node.reset()
                    end_node = None
                # Calling the functions to place nodes manually.
                start_node = place_start_node_manually(grid)
                end_node = place_end_node_manually(grid)
                # Calling the function to draw the start and end node
                # and display the grid.
                display_prepared_grid(start_node, end_node, grid)
            elif options_start_end[user_choice] == "Go back":
                # If the user chose to go back, we display the main menu again.
                user_choice = main_menu.show()
        elif options_main[user_choice] == "Pathfinder algorithms":
            user_choice = pathfinder_menu.show()
            if (
                options_pathfinder[user_choice] != "Go back" and
                (not start_node or not end_node)
            ):
                # If the user chose to run a pathfinder algorithm,
                # but the start and end node have not been placed yet,
                # we let the user know that they must place them first.
                display_grid(grid)
                print("Start and end node not placed yet.")
            elif options_pathfinder[user_choice] == "Dijkstra's algorithm":
                # Calling the function to run Dijkstra's algorithm.
                dijkstra(grid, start_node, end_node)
            elif options_pathfinder[user_choice] == "A* algorithm":
                # Calling the function to run A* algorithm.
                a_star(grid, start_node, end_node)
            elif options_pathfinder[user_choice] == "Bi-directional BFS":
                # Calling the function to run Bi-directional BFS algorithm.
                bidirectional_breadth_first_search(grid, start_node, end_node)
            elif options_pathfinder[user_choice] == "Go back":
                # If the user chose to go back, we display the main menu again.
                user_choice = main_menu.show()
        elif options_main[user_choice] == "Exit":
            # If the user chose to exit, we exit the program.
            app_running = False


# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    main()
