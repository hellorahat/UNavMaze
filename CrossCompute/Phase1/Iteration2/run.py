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

def writeMaze(mazeList):
    """
    Write out a 2D list in the format in a txt file.
    :param fileName: The name of the file.
    """
    completeName = join(output_folder, "maze.txt")
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
        
def addWeightedEdges(G, mazeList, currentEntry, nextEntry):
    nextEntryValue = mazeList[nextEntry[0]][nextEntry[1]]
    if nextEntryValue == "W":
        G.add_weighted_edges_from([(currentEntry,nextEntry,999999)],weight="weight")
    elif nextEntryValue.isnumeric():
        G.add_weighted_edges_from([(currentEntry,nextEntry,int(nextEntryValue))],weight="weight")
    else:
        G.add_weighted_edges_from([(currentEntry,nextEntry,1)],weight="weight")
        
def listToNetworkXGraph(mazeList, display=False):
    """
    Converts a list to a weighted NetworkX graph.
    :param mazeList (list): The 2D list to be referenced
    :param display (bool): Whether to display the graph. Default is False.
    :return: graph
    """
    G = nx.grid_2d_graph(len(mazeList),len(mazeList[0])) # Create a row X col NetworkX grid.
    for u,v,d in G.edges(data=True):
        if mazeList[u[0]][u[1]] == "W":
            d["weight"] = 999999
        elif isinstance(mazeList[u[0]][u[1]], int):
            d["weight"] = int(mazeList[u[0]][u[1]])
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
        nx.draw_networkx(G,pos, node_color=colorMap, labels=labels, font_size=6)
        plt.axis("off")
        completeName = join(output_folder, "mazeGraph.png")
        plt.savefig(completeName, format="PNG")
    return G
###

completeName = join(input_folder, "data.csv")
with open(completeName, 'r') as file:
    data = csvToList(file)
    validation = validateMaze(data)
    if validation[0]:
        listToNetworkXGraph(data, display=True)
    else:
        print(validation[1])
        exit()