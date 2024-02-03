# UNavMaze: Maze Solver App
{ csv }
## Display the Shortest Path in Weighted Mazes Effortlessly
UNavMaze quickly gives visualizations of the shortest path for mazes. Simply provide a csv file as input and the application will display the shortest path for you.

## Using UNavMaze
In order to use UNavMaze, first create a csv file for the maze.
- Include a start point by placing "S" in a cell.
- Include an end point by placing "E" in a cell.
- Weighted cells can be denoted by using integers.
- Empty cells automatically default to a weight of 1.

Here's a simple example for the input csv maze:
|   |   |   |   |   |
|---|---|---|---|---|
| S |   | 2 | 5 | 2 |
| 2  | 3 |   | 3  |  3 |
|   |   | 2  | 3  |   |
|   | 6  | 2 |   | E |

After providing the csv input to UNavMaze, the app will output the visualization of the maze with the calculated path as a png file.
