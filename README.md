# Maze
Create unique mazes either in GUI or directly into a numpy array!

## Usage
To get a numpy array of the maze use `mazes.py` as shown below...
```python
import mazes
# n_x and n_y are the number of squares in the x and y direction respectively
newMaze = mazes.Maze.make_maze(n_x, n_y, maze_type='Prim')
```
Currently, the finished mazes types are only Prim and Kruskal type mazes,
however, I hope to add more soon.

To view the maze in the gui simply run `app.py` once all the dependencies
are installed.