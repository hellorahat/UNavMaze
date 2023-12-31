import csv
from sys import argv
from os.path import join
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
            if row != "": # If we are not at the beginning of a row, add a space before we add the next entry
                row += " "
            if mazeList[i][j] == "": # If the entry is a blank cell, put a space in its place.
                row += " "
            else:
                row += str(mazeList[i][j]) # Enter the entry in the cell
        mazeFile.write(row + "\n") # Write the row to the txt and proceed to next row.
###

completeName = join(input_folder, "data.csv")
with open(completeName, 'r') as file:
    data = csvToList(file)
    validation = validateMaze(data)
    if validation[0]:
        writeMaze(data)
    else:
        print(validation[1])
        exit()