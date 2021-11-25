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
- ##### Pathfinder algorithms menu.
The third option in the main menu is the "Pathfinder algorithms". Here, the user can choose which algorithm will be used to find the shortest path between the start and end points.
![Pathfinder algorithms menu screenshot](assets/documentation/pathfinder-menu.png)
