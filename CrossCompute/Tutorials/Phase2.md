# UNavMaze Phase 2 Tutorial
## Synopsis
Phase 1 of UNavMaze will consist of taking a maze CSV file as an input and then outputing a PNG file containing an image of the maze by coloring pixels.
# Table of Contents
- [Iteration 1](#iteration-1)
    - [Goal](#goal)
    - [Configure automate.yml](#configure-automateyml)
        - [Edit Output Variable](#edit-output-variable)
        - [Configure Environment](#configure-environment)
    - [Configure run.py](#configure-runpy)
        - [The createImage Function](#the-createimage-function)
        - [The getMinMax Function](#the-getminandmax-function)
        - [Calculate RGB Value of Brown Based on Interval](#calculate-rgb-value-of-brown-based-on-interval)
        - [The putPixel Function](#the-putpixel-function)
        - [The labelWeights Function](#the-labelweights-function)
- [Iteration 2](#iteration-2)
    - [Goal](#goal-1)
    - [Configure run.py](#configure-runpy-1)
        - [Color Outlines of Squares](#color-outlines-of-squares)
        - [Adjust Scale Depending on Size](#adjust-scale-depending-on-size)

# Iteration 1
## Goal
Our goal for Iteration 1 is to use the Pillow library in order to create an image of a maze by coloring in pixels.

## Configure automate.yml
### Edit Output Variable
The view is changed to **image** in order to output our image. The path will be changed to a **.png**
```yml
# output configuration
output:
  variables:
    - id: mazeImage
      view: image
      path: mazeImage.png
```
### Configure Environment
Our environment also needs to include the Pillow library to be able to create the images.
```yml
environment:
  packages:
    - id: networkx[default]
      manager: pip
    - id: matplotlib==3.7.2
      manager: pip
    - id: Pillow
      manager: pip
```
## Configure run.py
### The createImage Function
This function will create an image from our data and a **scale** parameter; **scale** will determine how large the image will be scaled.
<br/>
We begin by specifying the width and height of our image. We get the width from multiplying our total amount of columns by the scale. Similarly, we get height from multiplying our total amount of rows by the scale.
```py
width = len(data[0])*scale
height = len(data)*scale
img  = Image.new(mode = "RGB", size = (width, height), color=(255,255,255)) # color(255,255,255) specifies the background to be white instead of the default (black)
```
Now, we iterate through our 2D list and color every entry based on what the entry is.
- Walls will be colored black
- Path will be colored blue
- Start will be colored green
- End will be colored red
- Weighted path will be colored with a darker shade of brown the higher weighed it is (compared to the min and max weights of the maze).
<br/>

The weighted path will be slightly more complicated to implement.

We will color a darker shade of brown depening on how highly weighed it is relative to its maximum and minimum weights.<br/>
For example, in a maze with minimum weight of 1 and maximum weight of 100 the shade of brown for weight 50 is equivalent in color to another maze with minimum weight of 1 and maximum weight of 10 with a cell weighed as 5.
<br/>

### The getMinAndMax Function
In order to implement this, we first need to create a function that iterates through the entire list and returns the maximum and minimum weights of the maze:
```py
def getMinAndMax(data):
    """
    Gets the minimum and maximum weight values from a maze.
    :param data: The 2D list to get the information from.
    """
    min = 999999999
    max = 0
    for i in range(len(data)):
        for v in range(len(data[0])):
            entry = data[i][v]
            if entry.isnumeric():
                if int(entry) > 1:
                    if int(entry) < min:
                        min = int(entry)
                    if int(entry) > max:
                        max = int(entry)
    return min,max
```
### Calculate RGB Value of Brown Based on Interval
Using the min and max values obtained from this function, we need to normalize the range so that its between 0 and 1.
<br/>
We use the following equation to implement this:<br/>
`(x-min)/(max-min)`
<br/>

`x` being the weight of the cell currently being inspected.
<br/>
We multiply the normalized value by 255 to get the number in RGB color range.
<br/>
`255*((x-min)/(max-min))`

Our color needs to be darker the higher the value is (it needs to be closer to black:(0,0,0)). This means we need a lower RGB value for a highly weighed number.<br/>

By subtracting 255 from our number we can reverse the effect to get a darker shade.<br/>
`255-(255*((x-min)/(max-min)))`

Shades of brown can be created in the following way:<br/>
`red = x, green = x // 2, blue = green // 2`

One problem to account for is that the min value will map to (0,0,0) (black) using this equation. To circumvent this, we add 50 to the overall equation to get a light shade of brown instead of getting black.<br/>
`50+(255-(255*((x-min)/(max-min))))`

Now we just iterate through the entire 2D list and substitute `x` for `data[i][v]` to account for the current entry.

```py
for i in range(len(data)):
        for v in range(len(data[0])):
            if len(data[i][v]) > 0:
                if data[i][v].isnumeric():
                    if int(data[i][v]) > 1: # color weighted path brown
                        red = 50+(255-(255 * (int(data[i][v])-min) // (max-min)))
                        green = red // 2
                        blue = green // 2
                        putPixel(img, v, i, (red,green,blue), scale)
                if data[i][v].lower() == "w": # if wall, color black
                    putPixel(img, v, i, (0,0,0), scale)
                if (data[i][v].lower())[-1] == "p": # if path, color blue
                    putPixel(img, v, i, (137, 207, 240), scale)
                if data[i][v].lower() == "s": # if start, color green
                    putPixel(img, v, i, (0,255,0), scale)
                if data[i][v].lower() == "e": # if end, color red
                    putPixel(img, v, i, (255,0,0), scale)
```
### The putPixel Function
We will now define the **putPixel** function being referenced here.<br/> **putPixel** will color in a **scale*****scale** box depending on the color. For example, if the scale is 5 and we color black, it will be a 5*5 black square.

```py
def putPixel(img, row, col, color, scale):
    """
    Color a square of pixels with a given color.
    :param img: The image to be colored.
    :param row: Row value.
    :param col: Col value.
    :param color (3-tuple): An rgb color value. 
    """
    for j in range(scale):
        for k in range(scale):
            xPos = (row*scale)+(j)
            yPos = (col*scale)+(k)
            img.putpixel((xPos,yPos), color)
```
### The labelWeights Function
Now, we label the weights for every weighted cell by using a font that is also scaled so that it fits in the boxes.

```py
I1 = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf",scale*.75) # arial must be installed on system
```

Now we iterate through every entry and label all of the weights. We position the numbers in the center of every box based on scale.

```py
def labelWeights(img, data, scale):
    I1 = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf",scale*.75) # arial must be installed on system
    for i in range(len(data)):
        for v in range(len(data[0])):
            entry = data[i][v]
            if len(entry) > 1:
                if entry[-1] == "P":
                    entry = entry[:-1] # remove the last character (P) so we can label only the numerical weight
                I1.text((v*scale+scale*.25,i*scale+scale*.1),entry,font=font,fill=(0,0,0))
            elif entry.isnumeric():
                if int(entry) > 1: # if weighed cell
                    I1.text((v*scale+scale*.25,i*scale+scale*.1),entry,font=font,fill=(0,0,0))
            elif entry.lower() == "s": # if start
                I1.text((v*scale+scale*.25,i*scale+scale*.1),entry,font=font,fill=(0,0,0))
            elif entry.lower() == "e": # if end
                I1.text((v*scale+scale*.25,i*scale+scale*.1),entry,font=font,fill=(0,0,0))
```
Now we modify the end of our `run.py` to include the **createImage** function:
```py
completeName = join(input_folder, "data.csv")
with open(completeName, 'r') as file:
    data = csvToList(file)
    validation = validateMaze(data)
    if validation[0]:
        # writeMaze(data)
        G = listToNetworkXGraph(data, display=False)
        startPoint, endPoint = locateStartAndEnd(data)
        shortestPath = calculatePath(G, startPoint, endPoint)
        mazeSolution(data, shortestPath)
        createImage(data, 15) # <- Added function
    else:
        print(validation[1])
        exit()
```

Upon running the `crosscompute` command, we can now input a CSV maze and a maze image will be outputted.

# Iteration 2
## Goal
Our goal in Iteration 2 is to color the outlines of the squares so we can discern between each cell. Additionally, we will scale each maze so that larger mazes are scaled smaller, and smaller mazes are scaled larger, so overall they will cover approximately the same amount of space on the screen.
## Configure run.py
### Color Outlines of Squares
In order to discern between each box, we now color the outlines of every box darker than it's original color.<br/>
With the following line, we can determine the outline of every square:
```py
if j == 0 or k == 0 or j == scale-1 or k == scale-1:
```
In other words, if the row is the minimum number, or if the row is the maximum number, or if the column is the minimum number, or if the column is the maximum number; if any of those cases are true, then the position is an outline of the square.
<br/>
We adjust the `putPixel` function accordingly:
```py
def putPixel(img, row, col, color, scale):
    """
    Color a square of pixels with a given color.
    :param img: The image to be colored.
    :param row: Row value.
    :param col: Col value.
    :param color (3-tuple): An rgb color value. 
    """
    for j in range(scale):
        for k in range(scale):
            xPos = (row*scale)+(j)
            yPos = (col*scale)+(k)
            if j == 0 or k == 0 or j == scale-1 or k == scale-1: # check to see if we are at an outline pixel
                if color == (255,255,255): # if white, we color outline with gray instead (empty cells)
                    img.putpixel((xPos,yPos), (225,225,225))
                else: # color darker shade of color to discern the outline
                    img.putpixel((xPos,yPos), (int(color[0]*.85),int(color[1]*.85),int(color[2]*.85)))
            else: # if we are not on at an outline pixel, color with normal color
                img.putpixel((xPos,yPos), color)
```
### Adjust Scale Depending on Size
We adjust scale automatically depending on size so that large mazes are scaled down to fit the entire screen, and small mazes and scaled up to increase resolution as much as possible.

To do this, we first determine a maximum scale that the smallest maze would be able to scale up to. For this application, 50 will be used as the maximum. The following equation will be used to determine scale:<br/>
`scale = maxScale - (maxScale * (mazeMax//maxScale))`<br/>
This equation ensures that larger mazes are scaled down, and smaller mazes are scaled up. Now we implement this equation into a function:
```py
def determineScale(data):
    mazeMin,mazeMax = getMinAndMax(data)
    maxScale = 50
    scale = maxScale - (maxScale * (mazeMax//maxScale))
    return scale
```

Now we edit the end of `run.py` to include the new functions:
```py
completeName = join(input_folder, "data.csv")
with open(completeName, 'r') as file:
    data = csvToList(file)
    validation = validateMaze(data)
    if validation[0]:
        # writeMaze(data)
        G = listToNetworkXGraph(data, display=False)
        startPoint, endPoint = locateStartAndEnd(data)
        shortestPath = calculatePath(G, startPoint, endPoint)
        mazeSolution(data, shortestPath)
        scale = determineScale(data) # <- Added function
        createImage(data, scale)
    else:
        print(validation[1])
        exit()
```
Upon running the `crosscompute` command, we can now input any size CSV maze file and it will output an automatically scaled PNG maze image.