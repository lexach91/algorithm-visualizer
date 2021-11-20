"""
Module for pathfinding algorithms.
"""
from constants import terminal
from grid_functions import (
    display_grid,
    reset_grid_partially,
    update_all_neighbors,
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
