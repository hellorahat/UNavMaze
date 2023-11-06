from os import getenv
from pathlib import Path
import csv
from sys import argv
from os.path import join
import networkx as nx
import matplotlib.pyplot as plt

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
        exportCSV(data, output_folder, "mazePath.csv")
            
    else:
        print(validation[1])
        exit()