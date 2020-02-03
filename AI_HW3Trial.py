
import numpy as np
import copy

    
   
    
# a class for a location object
class Location:
    x = None 
    y = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
def printMap(dirMap):
    size = len(dirMap)
    for y in range(size):
        print("| ")
        for x in range(size):
            if dirMap[x][y] == "X":
                print(" X | ", end = "")
            elif dirMap[x][y] == "G":
                print(" G | ", end = "")
            else:
                print(" ", dirMap[x][y], " | ", end = "")
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
            

def addObstacle(coords, dirMap, driveMap):
    x = int(coords[0])
    y = int(coords[1])
    dirMap[x][y] = -100
    driveMap[x][y] = "X"
    



def getDirections(dirMap, driveMap, goal, size):
    didChangeScores = True
    dirMap[goal.x][goal.y] = 100
    driveMap[goal.x][goal.y] = "G"
    reward = 0
    while didChangeScores:
        didChangeScores = False
        for x in range(size):
            for y in range(size):
                oldVal = dirMap[x][y]
                if goal.x == x and goal.y == y:
                    reward = 99
                elif driveMap[x][y] == "X":
                    reward = -101
                else:
                    reward = -1
                    updateScores(dirMap, x, y, reward)
                if oldVal != dirMap[x][y]:
                    didChangeScores = True        


def updateScores(dirMap, x, y, reward):
    size = len(dirMap)
    discount = 0.9
    if y == 0:
        north = dirMap[x][y] 
    else:
        north = dirMap[x][y - 1]
    if y == size -1:
        south = dirMap[x][y] 
    else:
        south = dirMap[x][y+1]
    if x == 0:
        west = dirMap[x][y] 
    else:
        west = dirMap[x-1][y]
    if x == size-1:
        east = dirMap[x][y] 
    else:
        east = dirMap[x + 1][y]
    '''
    goNorth = (0.7 * north) + (0.1 * (south + east + west)) 
    goSouth = (0.7 * south) + (0.1 * (north + east + west)) 
    goEast = (0.7 * east) + (0.1 * (south + north + west)) 
    goWest = (0.7 * west) + (0.1 * (south + east + north)) 
    '''

    goNorth = (0.1 * (south + east + west)) + (0.7 * north)
    goSouth =(0.1 * (north + east + west)) + (0.7 * south) 
    goEast = (0.1 * (south + north + west)) + (0.7 * east)   
    goWest = (0.1 * (south + east + north)) + (0.7 * west)   
    dirMap[x][y] =  np.floor(discount * (reward + (max(goNorth, goSouth, goEast, goWest))))
'''
    currentVal = dirMap[x][y] 
    goNorth = currentVal + 0.1 * (reward + 0.9 *( (0.7 * north) + (0.1 * (south + east + west) ) ) - currentVal)
    goSouth = currentVal +(reward + 0.9 *( (0.7 * south) + (0.1 * (north + east + west) ) ) - currentVal)
    goEast = currentVal +  (reward + 0.9 *( (0.7 * east) + (0.1 * (south + north + west) ) ) - currentVal)
    goWest =  currentVal + 0.1 * (reward +0.9 *( (0.7 * west) + (0.1 * (south + east + north) ) ) - currentVal)
    
    dirMap[x][y] =  np.floor(((max(goNorth, goSouth, goEast, goWest))))
'''
def createDirMap(dirMap, driveMap):
    size = len(dirMap)
    for x in range(size):
        for y in range(size):
            if driveMap[x][y] == "X":
                continue
            elif driveMap[x][y] == "G":
                continue

            if y == 0:
                north = dirMap[x][y] 
            else:
                north = dirMap[x][y - 1]
            if y == size -1:
                south = dirMap[x][y]
            else:
                south = dirMap[x][y+1] 
            if x == 0:
                west = dirMap[x][y]
            else:
                west = dirMap[x-1][y]
            if x == size-1:
                east = dirMap[x][y] 
            else:
                east = dirMap[x + 1][y]

            maxVal = max(north, south, east, west)
            
            if maxVal == north:
                driveMap[x][y] = "N"
            elif maxVal == south:
                driveMap[x][y] = "S"
            elif maxVal == east:
                driveMap[x][y] = "E"
            elif maxVal == west:
                driveMap[x][y] = "W"
            


def simulateCars(startLocations, endLocations, dirMap, driveMap):
    numCars = len(endLocations)
    for car in range(numCars):
        tempDirMap = copy.deepcopy(dirMap)
        tempDriveMap = copy.deepcopy(driveMap)
        getDirections(tempDirMap, tempDriveMap, endLocations[car], size)
        createDirMap(tempDirMap, tempDriveMap)
        #printMap(tempDriveMap)
        #print("_______-_________--________-_________________--____________")
       # printMapScores(driveMap)
        print("MOVING THE , ", car, " CAR -----------------------------")
        simulateCar(startLocations[car], endLocations[car], tempDirMap, tempDriveMap,)
    
        tempDirMap = None
        tempDriveMap = None
        



def simulateCar(start, goal, dirMap, driveMap):
    totalBalance = 0

    for i in range(10):
        location = Location(start.x, start.y)
        balance = 0
        np.random.seed(i)
        randDistr = np.random.random_sample(1000000)
        k = 0

        while not ((location.x == goal.x) and (location.y == goal.y)):
            swerve = randDistr[k]
            balance += moveCar(swerve, location, dirMap, driveMap, goal)
            
            k+=1

        totalBalance += (balance + 100)
    
    
    mean = np.floor((totalBalance/10))
    print(mean)

def moveCar(swerve, currentLoc, dirMap, driveMap, goal):
    direction = driveMap[currentLoc.x][currentLoc.y]

    if direction == "N":
        return moveNorth(currentLoc, dirMap,driveMap, swerve, goal)
    elif direction == "S":
        return moveSouth(currentLoc, dirMap,driveMap, swerve, goal)
    elif direction == "E": 
        return moveEast(currentLoc, dirMap,driveMap, swerve, goal)
    elif direction == "W":
        return moveWest(currentLoc, dirMap,driveMap, swerve, goal)
    return 0
    

def moveNorth(currentLoc, dirMap, driveMap, swerve, goal):
    y = currentLoc.y
    x = currentLoc.x
  
   
    if swerve > 0.7:
        if swerve > 0.8:
            if swerve > 0.9:
                return moveSouth(currentLoc, dirMap, driveMap, 0, goal)
            return moveEast(currentLoc, dirMap, driveMap, 0, goal)
        return moveWest(currentLoc, dirMap,driveMap, 0, goal)    
    else:
        if y == 0:
            return -1
        elif driveMap[x][y-1] == "X":
            return -101
        else:
            currentLoc.y -= 1
            return -1
    return 0

def moveSouth(currentLoc, dirMap, driveMap, swerve, goal):
    y = currentLoc.y
    x = currentLoc.x

   
    if swerve > 0.7:
        if swerve > 0.8:
            if swerve > 0.9:
                return moveNorth(currentLoc, dirMap,driveMap, 0, goal) 
            return moveWest(currentLoc, dirMap,driveMap, 0, goal)
        return moveEast(currentLoc, dirMap,driveMap, 0, goal)
    else: 
        if y == (len(dirMap) - 1):
            return -1
        elif driveMap[x][y+1] == "X":
            return -101
        else:
            currentLoc.y += 1
            return -1

def moveEast(currentLoc, dirMap, driveMap, swerve, goal):
    y = currentLoc.y
    x = currentLoc.x
  
    if swerve > 0.7:
        if swerve > 0.8:
            if swerve > 0.9:
                return moveWest(currentLoc, dirMap,driveMap, 0, goal)
            return moveSouth(currentLoc, dirMap,driveMap, 0, goal)    
        return moveNorth(currentLoc, dirMap,driveMap, 0, goal)
        
    else:
        if x == (len(dirMap) - 1):
            return -1
        elif driveMap[x+1][y] == "X":
            return -101
        else:
            currentLoc.x += 1
            return -1
    return 0

def moveWest(currentLoc, dirMap, driveMap, swerve, goal):
    y = currentLoc.y
    x = currentLoc.x
    
    
    if swerve > 0.7:
        if swerve > 0.8:
            if swerve > 0.9:
               return moveEast(currentLoc, dirMap,driveMap, 0, goal) 
            return moveNorth(currentLoc, dirMap,driveMap, 0, goal)
        return moveSouth(currentLoc, dirMap,driveMap, 0, goal)       
    else:
        if x == 0:
            return -1
        elif driveMap[x-1][y] == "X":
            return -101
        else:
            currentLoc.x -= 1
            return -1
    return 0



#opening and reading the input file
rawInput = open("input2.txt",'r')
size = int(rawInput.readline()) 
numCars = int(rawInput.readline())
numObstacles = int(rawInput.readline())

#Initializing the board
dirMap = [[0] * size for i in range(size)]
driveMap = [[" "] * size for i in range(size)]



#Mark Obstacles
for i in range(numObstacles):
    coords = rawInput.readline().split(',')
    addObstacle(coords, dirMap, driveMap)
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


simulateCars(startLocations, endLocations, dirMap, driveMap)

print("Done!")


































