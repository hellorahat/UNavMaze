# NavMaze
 
Tool that takes a maze as a CSV file and outputs a path as a CSV file.\

W - Symbol for wall (can not create path through walls).\
S - Symbol for start point.\
E - Symbol for end point.\
P - Symbol for path. If a path needs to be created through a weighted cell, it will be concatenated at the end of the cell; for example, a path through a cell with weight of "3" would appear "3P" instead of "P".\

--

Blank cells have a weight of 1 by default.\
Weighted cells are denoted by integer values, a cell with the integer 2 is worth 2x more than a blank cell.
