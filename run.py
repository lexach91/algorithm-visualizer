import random
from simple_term_menu import TerminalMenu
from constants import HEIGHT, WIDTH, terminal
from grid_functions import (
    generate_grid,
    reset_grid,
    display_grid,
    reset_grid_partially,
    display_prepared_grid,
    place_start_node_manually,
    place_end_node_manually
    )
from maze_functions import (
    generate_random_pattern,
    generate_vertical_maze,
    generate_horizontal_maze,
    generate_maze_recursive_division,
    generate_spiral_maze
    )
from pathfinding_algorithms import (
    dijkstra,
    a_star,
    bidirectional_breadth_first_search
    )


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

    # Flag to check if the app is running.
    app_running = True

    print(
        terminal.home +
        terminal.clear +
        terminal.bold +
        terminal.yellow +
        "Welcome to pathfinding algorithms visualizer!\n" +
        terminal.normal
    )

    print(
        terminal.purple +
        "In the menu bellow you can:\n" +
        "   1. generate the grid\n" +
        "   2. place the start and the end node\n" +
        "   3. choose the algorithm to run and visualize\n" +
        terminal.normal
    )

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
                start_node = None
                end_node = None
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Random pattern":
                reset_grid(grid)
                start_node = None
                end_node = None
                # For random pattern, we call generate_random_pattern function
                generate_random_pattern(grid)
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Maze with vertical walls":
                reset_grid(grid)
                start_node = None
                end_node = None
                # For maze with vertical walls,
                # we call generate_maze_vertical_walls function
                generate_vertical_maze(grid)
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Maze with horizontal walls":
                reset_grid(grid)
                start_node = None
                end_node = None
                # For maze with horizontal walls,
                # we call generate_maze_horizontal_walls function
                generate_horizontal_maze(grid)
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Maze with spiral pattern":
                reset_grid(grid)
                start_node = None
                end_node = None
                # For maze with spiral pattern,
                # we call generate_maze_spiral_pattern function
                generate_spiral_maze(grid)
                display_grid(grid)
                # Changing the flag to True
                pattern_generated = True
            elif options_grid[user_choice] == "Maze recursive division":
                reset_grid(grid)
                start_node = None
                end_node = None
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
                # orientation equal to "vertical",
                # because we want to start with creating a vertical wall.
                generate_maze_recursive_division(
                    grid, 2, HEIGHT - 2, 2, WIDTH - 2, "vertical"
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
                print(
                    terminal.red +
                    terminal.underline +
                    "No pattern generated yet." +
                    terminal.normal
                    )
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
                if start_node and end_node:
                    display_prepared_grid(start_node, end_node, grid)
                else:
                    display_grid(grid)
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
                print(
                    terminal.red +
                    terminal.underline +
                    "Start and end node not placed yet." +
                    terminal.normal
                    )
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
            print(
                terminal.home +
                terminal.clear +
                terminal.green +
                terminal.bold +
                "Thank you for using the app!\n" +
                "Have a nice day, bye!" +
                terminal.normal
                )


# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    main()
