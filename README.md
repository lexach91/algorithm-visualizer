# Path-finding algorithms visualizer
[Path-finding algorithms visualizer](https://python-algorithm-visualizer.herokuapp.com/) is a python terminal application that allows the user to understand how the path-finding algorithms work by visualizing them in the terminal.

User can generate different types of patterns and mazes on the provided grid, place the start and end points, and then run the algorithms to find the shortest path between them.
![Am I Responsive screenshot](assets/documentation/am-i-responsive.png)

---

### How to use    

- Open this [link](https://python-algorithm-visualizer.herokuapp.com/) or copy it here: `https://python-algorithm-visualizer.herokuapp.com/`, paste it in your browser's address bar, and press enter.
- When the page is loaded, click the "RUN PROGRAM" button.
- Navigate through the menu options using the arrow keys on your keyboard, press enter to choose an option.
- First, you will need to choose the type of pattern you want to generate in the "Grid options".
- Then, you will need to place the start and end points on the grid in the "Place start and end node".
- Finally, you will need to choose which algorithm you want to run in "Pathfinder algorithms".

---

### User stories

- As a first time visitor, I want to be able to understand the main purpose of the application.
- As a first time visitor, I want to be able to see the instructions on how to use the application.
- As a first time visitor, I want to be able to see the different types of patterns that can be generated.
- As a first time visitor, I want to be able to see the different algorithms that can be used to find the shortest path between the start and end points.
- As a user, I want to be able to see how the algorithms work with different patterns and different start and end nodes placement on the grid.
- As a user, I want to be able to change the pattern type, start and end nodes placement, and algorithm without restarting the application.

---

### Features
- ##### The welcome message.
After the application is loaded, the user can see the welcome message and short instructions on how to use the application.
![Welcome message screenshot](assets/documentation/startup-screen.png)
- ##### Main menu.
Under the welcome message, the user can see the main menu.
![Main menu screenshot](assets/documentation/main-menu.png)
- ##### Grid options menu.
The first option in the main menu is the "Grid options". Here, the user can choose the type of pattern that will be generated on the grid.
![Grid options menu screenshot](assets/documentation/grid-menu.png)

1. Empty grid: The grid will be empty with the wall border around it.
![Empty grid screenshot](assets/documentation/empty-grid.png)
2. Random pattern: The grid will be filled with random walls and empty spaces.
![Random grid screenshot](assets/documentation/random-pattern.png)
3. Maze with vertical walls: The grid will be filled with vertical walls with one random passage in each of them.
![Maze with vertical walls screenshot](assets/documentation/vertical-maze.png)
4. Maze with horizontal walls: The grid will be filled with horizontal walls with one random passage in each of them.
![Maze with horizontal walls screenshot](assets/documentation/horizontal-maze.png)
5. Maze with spiral pattern: The wall on the grid will be generated in a spiral pattern.
![Maze with spiral pattern screenshot](assets/documentation/spiral-maze.png)
6. Maze recursive division: The maze on the grid will be generated using recursive division algorithm.
![Maze recursive division screenshot](assets/documentation/recursive-maze.png)

- ##### Place start and end node menu.
The second option in the main menu is the "Place start and end node". Here, the user can place the start and end points on the grid.
![Place start and end node menu screenshot](assets/documentation/start-end-menu.png)

1. Place by default: The start node will be placed in the top left corner and the end node will be placed in the bottom right corner.
![Place by default screenshot](assets/documentation/place-by-default.png)
2. Place randomly: The start and the end node will be placed randomly in empty spaces on the grid.
![Place randomly screenshot](assets/documentation/place-randomly.png)
3. Place manually: The user will be able to place the start and end node on the grid using the arrow keys on their keyboard.
![Place start node manually screenshot](assets/documentation/place-start-manually.png)
![Place end node manually screenshot](assets/documentation/place-end-manually.png)

- ##### Pathfinder algorithms menu.
The third option in the main menu is the "Pathfinder algorithms". Here, the user can choose which algorithm will be used to find the shortest path between the start and end points.
![Pathfinder algorithms menu screenshot](assets/documentation/pathfinder-menu.png)

1. Dijkstra's algorithm: The algorithm will find the shortest path between the start and end points using the Dijkstra's algorithm. In our case, it works as the breadth-first search algorithm because all the nodes on the grid are connected and have the same weight (distance equal to 1). As we can see in the screenshots, the algorithm starts from the start node and explores the grid in all directions until it reaches the end node.
![Dijkstra's algorithm screenshot](assets/documentation/dijkstra.png)
![Dijkstra's algorithm path screenshot](assets/documentation/dijkstra-path-found.png)
2. A* (A star) algorithm: This algorithm is very similar to the Dijkstra's and Breadth-first search algorithms. The difference is that the algorithm uses the heuristic function to calculate the distance between the start and end points. The heuristic function is the distance between the start and end points. In our case, the heuristic function is the Manhattan distance. As we can see in the screenshots, the algorithm starts from the start node and explores the grid in directions that have the shortest distance to the end node.
![A* algorithm screenshot](assets/documentation/a-star.png)
![A* algorithm path screenshot](assets/documentation/a-star-path-found.png)
3. Bi-directional BFS (breadth-first search): This algorithm is running in both directions. It starts from the start node and the end node simultaneously and explores the grid in all directions until it finds the intersection between the two paths. 
![Bi-directional BFS algorithm screenshot](assets/documentation/bi-directional.png)
![Bi-directional BFS algorithm path screenshot](assets/documentation/bi-directional-path-found.png)

- ##### Exit.
The last option in the main menu is the "Exit". Here, the user can exit the application and see the bye message.
![Exit menu screenshot](assets/documentation/bye-message.png) 

---
### Flowchart
In the following flowchart, you can see the basic logic of the application.
![Flowchart](assets/documentation/flowchart.png)

---
### Technologies used

###### Languages
- [Python](https://www.python.org/): The main language used to develop the application.
- [JavaScript](https://www.javascript.com/): The language used by the Code Institute to run mock terminal in the browser.
- [HTML](https://www.w3schools.com/html/): The language used by the Code Institute to create the layout needed to run the mock terminal in the browser.

###### Frameworks, libraries, and packages
- [random](https://docs.python.org/3/library/random.html): used to generate random numbers.
- [numpy](https://docs.scipy.org/doc/numpy/reference/): used to generate a 2d array used to represent the grid.
- [time](https://docs.python.org/3/library/time.html): sleep function from the time library was used to make every step of the grid update visible to the user.
- [blessed](https://pypi.org/project/blessed/): used to manipulate the terminal output.
- [simple-term-menu](https://pypi.org/project/simple-term-menu/): used to create the terminal menu for the application.

###### Other tools
- [Git](https://git-scm.com/): used to manage the application source code.
- [GitHub](https://github.com/): used to host the application source code.
- [Visual Studio Code](https://code.visualstudio.com/): used to edit the application source code.
- [Chrome](https://www.google.com/chrome/): used to run the application in the browser.
- [Draw.io](https://www.draw.io/): used to create the flowchart.

---
### Bugs and issues
- ###### Solved bugs
1. After deploying the application to heroku, I noticed that the grid was not displayed correctly, all emojis used to represent the walls were overlapping each other. It was because the emojis were wider than the standard character width in the mock terminal provided by the Code Institute.
    + *Solution*: 
        - I changed the code in the `display_grid` function:
        from this:
        `print("".join(str(node) for node in row))`
        to this:
        `print(" ".join(str(node) for node in row))`
        
        - Also, when running the app on the desktop, I used the ideographic space unicode character (U+3000) instead of the standard space character (U+0020) as an empty space on the grid, because its width equals the width of the wall emojis. But for correct display on the mock terminal, I used the standard space character (U+0020).

2. There were a bug the function `generate_vertical_maze(grid)`. Some walls were left without passages and some had more then one.
    + *Solution*:
        - Instead of using the built-in python list for the grid, I used a numpy array. It was easier to make sure that I don't skip any walls, using numpy array slicing: `grid[:, col][i].make_wall()` - gives us the whole column.

3. There were many minor bugs during the development of the application, that have been solved by manual testing and tweaking.

- ###### Unsolved bugs
1. The mock terminal that has been provided by the Code Institute freezes sometimes and all you can do is run the application again.

---
