
import numpy as np
import copy
class Block:
    north = 0
    south = 0
    east = 0
    west = 0
    best = 0
    isObstacle = False
    direction = None
    isGoal = False
    def __init__(self, north, south, east, west):
        self.north = north
        self.south = south
        self.east = east
        self.west = west
    
    def updateScores(self, dN, dS, dE, dW):
        self.north += dN
        self.south += dS
        self.east += dE
        self.west += dW
        self.best = max(self.north, self.south, self.east, self.west)
    
    def turIntoObstacle(self):
        self.best = -100
        self.isObstacle = True
    
    def turIntoGoal(self):
        self.best = 100
        self.isGoal = True
   
    def getScore(self):
        return self.best   
    
    def updateScore(self, didChange):
        oldBest = self.best
        if self.best < self.north:
            self.best = self.north
            self.direction = "N"
        if self.best < self.south:
            self.best = self.south
            self.direction = "S"
        if self.best < self.east:
            self.best = self.east
            self.direction = "E"
        if self.best < self.west:
            self.best = self.west
            self.direction = "W"
        if self.best != oldBest:
            return True
        else:
            return didChange
# a class for a location object
class Location:
    x = None 
    y = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY





def buildDriveMap(size):
    driveMap = [[None] * size for i in range(size)]
    for x in range(size):
        for y in range(size):
            driveMap[x][y] = Block(0,0,0,0)
            if y == 0:
                driveMap[x][y].updateScores(-2, 0, 0, 0)
            if y == (size - 1):
                driveMap[x][y].updateScores(0, -2, 0, 0)
            if x == 0:
                driveMap[x][y].updateScores(0, 0, 0, -2)
            if x == (size - 1):
                driveMap[x][y].updateScores(0, 0, -2, 0)

    return driveMap

def addObstacle(coords, driveMap):
    x = int(coords[0])
    y = int(coords[1])
    driveMap[x][y].turIntoObstacle()
    
def addGoal(coords, driveMap):
    x = int(coords[0])
    y = int(coords[1])
    driveMap[x][y].turIntoGoal()


def getDirections(dirMap, goal, size):
    didChangeScores = True
    block = None
    dirMap[goal.x][goal.y].turIntoGoal()
    while didChangeScores:
        didChangeScores = False
        for x in range(size - goal.x):
            x += goal.x
            for y in range(size):
                block = dirMap[x][y]
                if block.isObstacle == False:
                    if y > 0:
                        block.north = dirMap[x][y - 1].getScore()-1
                    if y < (size - 1):
                        block.south = dirMap[x][y + 1].getScore()-1
                    if x <size - 1:
                        block.east = dirMap[x + 1][y].getScore()-1
                    if x > 0:
                        block.west =dirMap[x-1][y].getScore()-1
                    didChangeScores = block.updateScore(didChangeScores)
        for x in reversed(range(goal.x)):
            for y in range(size):
                block = dirMap[x][y]
                if block.isObstacle == False:
                    if y > 0:
                        block.north = dirMap[x][y - 1].getScore()-1
                    if y < (size - 1):
                        block.south = dirMap[x][y + 1].getScore()-1
                    if x <size - 1 :
                        block.east = dirMap[x + 1][y].getScore()-1
                    if x > 0:
                        block.west = dirMap[x-1][y].getScore()-1
                    didChangeScores = block.updateScore(didChangeScores)

def printMap(dirMap):
    size = len(dirMap)
    for y in range(size):
        print("| ")
        for x in range(size):
            if dirMap[x][y].isObstacle:
                print(" X | ", end = "")
            elif dirMap[x][y].isGoal:
                print(" G | ", end = "")
            else:
                print(" ", dirMap[x][y].direction, " | ", end = "")
        print("")
def printMapScores(dirMap):
    size = len(dirMap)
    for y in range(size):
        print("| ")
        for x in range(size):
            if dirMap[x][y].isObstacle:
                print(" X | ", end = "")
            elif dirMap[x][y].isGoal:
                print(" 100 | ", end = "")
            else:
                print(" ", dirMap[x][y].best, " | ", end = "")
        print("")
            
def simulateCars(startLocations, endLocations, dirMap):
    numCars = len(endLocations)
    driveMap = None
    for car in range(numCars):
        driveMap = copy.deepcopy(dirMap)
        getDirections(driveMap, endLocations[car], boardSize)
        printMap(driveMap)
        print("_______-_________--________-_________________--____________")
        printMapScores(driveMap)
        print("MOVING THE , ", car, " CAR -----------------------------")
        simulateCar(startLocations[car], endLocations[car], driveMap)
        driveMap = None
        



def simulateCar(start, goal, dirMap):
    totalBalance = 0

    for i in range(10):
        location = Location(start.x, start.y)
        balance = 0
        np.random.seed(i)
        randDistr = np.random.random_sample(1000000)
        k = 0

        while not ((location.x == goal.x) and (location.y == goal.y)):
            swerve = randDistr[k]
            balance += moveCar(swerve, location, dirMap, goal)
            
            k+=1

        totalBalance += (balance + 100)
    
    
    mean = np.floor((totalBalance/10))
    print(mean)

def moveCar(swerve, currentLoc, dirMap, goal):
    direction = dirMap[currentLoc.x][currentLoc.y].direction

    if direction == "N":
        return moveNorth(currentLoc, dirMap, swerve, goal)
    elif direction == "S":
        return moveSouth(currentLoc, dirMap, swerve, goal)
    elif direction == "E": 
        return moveEast(currentLoc, dirMap, swerve, goal)
    elif direction == "W":
        return moveWest(currentLoc, dirMap, swerve, goal)
    return 0
    

def moveNorth(currentLoc, dirMap, swerve, goal):
    y = currentLoc.y
    x = currentLoc.x
    if y == 0:
        return -1
    elif dirMap[x][y-1].isObstacle:
        return -101
    else:
        if swerve <= 0.7:
            currentLoc.y -= 1
            return -1
        elif swerve <= 0.8:
            return moveWest(currentLoc, dirMap, 0, goal)
        elif swerve <= 0.9:
            return moveEast(currentLoc, dirMap, 0, goal)
        elif swerve <= 1:
            return moveSouth(currentLoc, dirMap, 0, goal)
    return 0

def moveSouth(currentLoc, dirMap, swerve, goal):
    y = currentLoc.y
    x = currentLoc.x
    if y == (len(dirMap) - 1):
        return -1
    elif dirMap[x][y+1].isObstacle:
        return -101
    else:
        if swerve <= 0.7:
            currentLoc.y += 1
            return -1
        elif swerve <= 0.8:
            return moveEast(currentLoc,  dirMap, 0, goal)
        elif swerve <= 0.9:
            return moveWest(currentLoc,dirMap, 0, goal)
        elif swerve <= 1:
            return moveNorth(currentLoc, dirMap, 0, goal)
    return 0

def moveEast(currentLoc, dirMap, swerve, goal):
    y = currentLoc.y
    x = currentLoc.x
    if x == (len(dirMap) - 1):
        return -1
    elif dirMap[x+1][y].isObstacle:
        return -101
    else:
        if swerve <= 0.7:
            currentLoc.x += 1
            return -1
        elif swerve <= 0.8:
            return moveNorth(currentLoc, dirMap, 0, goal)
        elif swerve <= 0.9:
            return moveSouth(currentLoc, dirMap, 0, goal)
        elif swerve <= 1:
            return moveWest(currentLoc, dirMap, 0, goal)
    return 0

def moveWest(currentLoc, dirMap, swerve, goal):
    y = currentLoc.y
    x = currentLoc.x
    if x == 0:
        return -1
    elif dirMap[x-1][y].isObstacle:
        return -101
    else:
        if swerve <= 0.7:
            currentLoc.x -= 1
            return -1
        elif swerve <= 0.8:
            return moveSouth(currentLoc, dirMap, 0, goal)
        elif swerve <= 0.9:
            return moveNorth(currentLoc, dirMap, 0, goal)
        elif swerve <= 1:
            return moveEast(currentLoc, dirMap, 0, goal)
    return 0

#opening and reading the input file
rawInput = open("input1.txt",'r')
boardSize = int(rawInput.readline()) 
numCars = int(rawInput.readline())
numObstacles = int(rawInput.readline())

#Initializing the board
driveMap = buildDriveMap(boardSize)



#Mark Obstacles
for i in range(numObstacles):
    coords = rawInput.readline().split(',')
    addObstacle(coords, driveMap)
#taking the start locations of the Cars
startLocations = []
for i in range(numCars):
    coords = rawInput.readline().split(',')
    startLocations.append(Location(int(coords[0]), int(coords[1])))
#taking the end locations of the Cars
endLocations = [] 
for i in range(numCars):
    coords = rawInput.readline().split(',')
    endLocations.append(Location(int(coords[0]), int(coords[1])))


simulateCars(startLocations, endLocations, driveMap)

print("Done!")


































