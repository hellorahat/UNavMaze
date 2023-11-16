from os import getenv
from pathlib import Path
import csv
from sys import argv
from os.path import join
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

input_folder, output_folder = argv[1:]

###

def csvToList(f):
    """
    Converts CSV file into 2D list format.
    :param f (str): The CSV to be converted.
    :return: 2D list
    """
    with open(f.name, 'r') as file:
        csvData = list(csv.reader(file))
        rowNum = len(csvData)
        colNum = len(csvData[0])
        mazeList = [[0 for i in range(colNum)] for j in range(rowNum)]
        for i in range(rowNum):
            colNum = len(csvData[i])
            for j in range(colNum):
                mazeList[i][j] = csvData[i][j]
    return mazeList

def validateMaze(mazeList):
    """
    Validates if a 2D list is a maze by checking if the following rules are passed:
    - There must be a start and end point.
    - There can be no more than one start point.
    - There can be no more than one end point.
    :param mazeList: The 2D list to be validated.
    :return: validation (bool), errors (str)
    """
    validation = True
    errors = ""
    startCount = 0
    endCount = 0
    for i in range(len(mazeList)):
        for j in range(len(mazeList[0])):
            if mazeList[i][j] == "S":
                startCount += 1
            elif mazeList[i][j] == "E":
                endCount += 1
    if startCount == 0 or endCount == 0:
        validation = False
        errors += "There must be a start and end point.\n"
    if startCount > 1:
        validation = False
        errors += "There can be no more than one start point.\n"
    if endCount > 1:
        validation = False
        errors += "There can be no more than one end point.\n"
    return validation, errors

def displayMaze(mazeList):
    """
    Print out a 2D list in the format of a Maze.
    :param mazeList: The 2D list to be printed.
    """
    row = ""
    for i in range(len(mazeList)):
        for j in range(len(mazeList[0])):
            if row != "":
                row += " "
            if mazeList[i][j] == "":
                row += " "
            else:
                row += str(mazeList[i][j])
        print(row)
        row = ""

def writeMaze(mazeList, fileName="maze.txt"):
    """
    Write out a 2D list in the format in a txt file.
    :param fileName: The name of the file.
    """
    print("writing")
    completeName = join(output_folder, fileName)
    mazeFile = open(completeName,"a")
    for i in range(len(mazeList)):
        row = ""
        for j in range(len(mazeList[0])):
            if row != "":
                row += " "
            if mazeList[i][j] == "":
                row += " "
            else:
                row += str(mazeList[i][j])
        mazeFile.write(row + "\n")
        
def listToNetworkXGraph(mazeList, display=False):
    """
    Converts a list to a weighted NetworkX graph.
    :param mazeList (list): The 2D list to be referenced
    :param display (bool): Whether to display the graph. Default is False.
    :return: graph
    """
    G = nx.grid_2d_graph(len(mazeList),len(mazeList[0])) # Create a row X col NetworkX grid.
    for u,v,d in G.edges(data=True):
        if mazeList[v[0]][v[1]] == "W":
            d["weight"] = 999999
        elif mazeList[v[0]][v[1]].isnumeric():
            d["weight"] = int(mazeList[v[0]][v[1]])
        else:
            d["weight"] = 1
    nx.write_weighted_edgelist(G, "weighted.edgelist")
    if display==True:
        colorMap = []
        labels = dict()
        pos = dict()
        count = 0
        for i in range(len(mazeList)):
            for j in range(len(mazeList[0])):
                pos[i,j] = j,len(mazeList)-i
                labels[i,j] = mazeList[i][j]
                if mazeList[i][j] == "W":
                    colorMap.append("black")
                elif mazeList[i][j] == "S":
                    colorMap.append("green")
                elif mazeList[i][j] == "E":
                    colorMap.append("red")
                elif mazeList[i][j].isnumeric():
                    colorMap.append("brown")
                else:
                    colorMap.append("white")
        print(len(colorMap))
        # for n in G:
            # if n == (1,0):
            #     colorMap.append('red')
            # else:
            #     colorMap.append('green')
        nx.draw_networkx(G,pos, node_color=colorMap, labels=labels, font_size=6)
        # nx.draw_networkx(G,pos, node_color=colorMap, with_labels=False, font_size=6)
        plt.axis("off")
        completeName = join(output_folder, "mazeGraph.png")
        plt.savefig(completeName, format="PNG")
    return G

def calculatePath(G, startPoint, endPoint):
    return nx.astar_path(G, startPoint, endPoint)

def locateStartAndEnd(mazeList):
    startPoint = (0,0)
    endPoint = (0,0)
    for i in range(len(mazeList)):
        for j in range(len(mazeList[0])):
            if mazeList[i][j] == "S":
                startPoint = i,j
            elif mazeList[i][j] == "E":
                endPoint = i,j
    return startPoint, endPoint

def mazeSolution(data, path):
    """
    Given a path, input the solution into a given list.
    :param data (list): The list being referenced.
    :param path (list): The path that will be added to the list.
    """
    for i in range(1,len(path)-1):
        data[path[i][0]][path[i][1]] += "P"

def exportCSV(data, folder, name):
    """
    Export a csv file given data for contents of the maze
    :param data (list): The list containing information about the maze.
    :param folder: The output folder.
    :param name: The name of the CSV file.
    """
    completeName = join(folder, name)
    with open(completeName,"w",newline="") as pathcsv:
        csvWriter = csv.writer(pathcsv,delimiter=',')
        csvWriter.writerows(data)

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
    if min > max: # If we still have the sentinal value of 999999999 for min, we return 0
        min = 0
    return min,max
        
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
            else: # if we are on at an outline pixel, color with normal color
                img.putpixel((xPos,yPos), color)

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
                if int(entry) > 1:
                    I1.text((v*scale+scale*.25,i*scale+scale*.1),entry,font=font,fill=(0,0,0))
            elif entry.lower() == "s":
                I1.text((v*scale+scale*.25,i*scale+scale*.1),entry,font=font,fill=(0,0,0))
            elif entry.lower() == "e":
                I1.text((v*scale+scale*.25,i*scale+scale*.1),entry,font=font,fill=(0,0,0))
    # I1.text((row*15,col*15),text,fill=(0,0,0))

def createImage(data, scale):
    """
    Create a image of the maze using the PIL library.
    :param data: The 2D list with path to create an image from.
    """
    width = len(data[0])*scale
    height = len(data)*scale
    img  = Image.new(mode = "RGB", size = (width, height), color=(255,255,255))
    min,max = getMinAndMax(data)
    for i in range(len(data)):
        for v in range(len(data[0])):
            if len(data[i][v]) > 0:
                if data[i][v].isnumeric():
                    if int(data[i][v]) > 1:
                        red = 50+(255-(255 * (int(data[i][v])-min) // (max-min))) # scale red from 0 - 255 based on min and max values | add 50 to the scaled value to ensure lightest brown instead of black if value is 0
                        green = red // 2 # green is red / 2 to make brown
                        blue = green // 2 # blue is green / 2 to make brown
                        putPixel(img, v, i, (red,green,blue), scale)
                if data[i][v].lower() == "w": # if wall, color black
                    putPixel(img, v, i, (0,0,0), scale)
                if (data[i][v].lower())[-1] == "p": # if weight concatenated with path, color blue
                    putPixel(img, v, i, (137, 207, 240), scale)
                if data[i][v].lower() == "s": # if start, color green
                    putPixel(img, v, i, (0,255,0), scale)
                if data[i][v].lower() == "e": # if end, color red
                    putPixel(img, v, i, (255,0,0), scale)
            else:
                putPixel(img, v, i, (255,255,255), scale)

    labelWeights(img, data, scale)
    completeName = join(output_folder, "mazeImage.png")
    img.save(completeName)
    
def determineScale(data):
    min,max = getMinAndMax(data)
    maxInterval = 50
    scale = maxInterval - (maxInterval * (max//maxInterval))
    return scale

###
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
        scale = determineScale(data)
        createImage(data, scale)
    else:
        print(validation[1])
        exit()