# Maze
Create unique mazes either in GUI or directly into a numpy array!

## Installation
```shell
git clone https://github.com/rpowel/maze
cd maze
pip install -r requirements.txt
```

## Usage

### Gui Based
Running app.py (after installing requirements) will open a window where you can select
the size and type of maze you would like to use, as well as a seed setting if you would
like to specify the maze seed.

### CLI Based

Maze generation returns a numpy array of 0's and 1's.

```python
# n_x and n_y are the number of squares in the x and y direction respectively
from processors.maze_selection_processor import MazeSelectionProcessor

newMaze = MazeSelectionProcessor(10, 10, maze_type='Prim').process()
# will return a numpy array like:
# [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
#     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 3],
#     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
#     [2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# ]
# '0' is a passage
# '1' is a wall
# '2' is the entrance
# '3' is the exit.
```

### Known Issues
#### Random maze generation is slow:
The 'random' maze option is not really a maze, it is a randomly generated array.
Before returning the maze array, it is checked for an open path from entrance
(2 or green) to exit (3 or red), and if there is no path it will try again.

Given the nature of the random maze generation it might need to try several times, hence it is slow.

#### Bricking when clicking 'Draw' Too Rapidly
If one tries to click the draw button in the gui in too rapid of succession, the program can freeze up needed a restart.

## Testing
```shell
# Install pytest
pip install pytest
# from maze or maze/app directory
pytest
```
