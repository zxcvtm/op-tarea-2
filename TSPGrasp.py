import networkx as nx
import matplotlib.pyplot as plt
import math, random, sys, time

nodeList = []
pos = {}
labels = {}

def loadFromFile(fileName):
    file = open(fileName, "r")
    f = file.readline()
    nodeCount = 0
    while(f):
        line = f.split()
        nodeList.append(nodeCount)
        pos[nodeCount] = (float(line[0]), float(line[1]))
        labels[nodeCount] = str(nodeCount)
        nodeCount = nodeCount + 1
        f = file.readline()
rclSize = 3
if(len(sys.argv) !=3):
    print("Error al iniciar el programa, probablemente falta el nombre de archivo a cargar")
    print("o el numero de candidatos reservados RCL")
    exit(0)
else:
    loadFromFile(sys.argv[1])
    rclSize = int(sys.argv[2])

def sorting(n):
    return n[1]

def findDistance(path):
    distance = 0
    for i in range(len(path) - 1):
        x2 = pos[path[i + 1]][0]
        x1 = pos[path[i]][0]
        y2 = pos[path[i + 1]][1]
        y1 = pos[path[i]][1]

        distance = distance + math.hypot(x2 - x1, y2 - y1)
    return distance

totalDistance = 0
edges = []

startTime = time.perf_counter()

visitedNodes = [0]

while(len(visitedNodes) < len(nodeList)):
    minDist = -1
    nextNode = -1
    currentNode = visitedNodes[-1]
    rcl = []
    for i in range(len(nodeList)):
        if(i != visitedNodes[-1] and i not in visitedNodes):
            x2 = pos[i][0]
            x1 = pos[currentNode][0]
            y2 = pos[i][1]
            y1 = pos[currentNode][1]

            dist = math.hypot(x2 - x1, y2 - y1)

            rcl.append([i, dist])
    
    rcl.sort(key = sorting)

    maxVal = min(len(rcl), rclSize)

    position = random.randint(0, maxVal - 1)

    nextNode = rcl[position][0]
    minDist = rcl[position][1]

    if(nextNode != -1):
        totalDistance = totalDistance + minDist
        visitedNodes.append(nextNode)
        edges.append((currentNode, nextNode))

edges.append((visitedNodes[-1], visitedNodes[0]))
visitedNodes.append(visitedNodes[0])

totalDistance = findDistance(visitedNodes)

rounds = 0

#Start of 2-opt
startNode = visitedNodes[0]
while((time.perf_counter() - startTime) < 200):
    rounds = rounds + 1
    improved = False
    for i in range(len(visitedNodes) - 3):
        tempList = visitedNodes.copy()
        tempList.pop(0)
        tempList.pop()
        tempList[i], tempList[i + 1] = tempList[i + 1], tempList[i]
        tempList.insert(0, startNode)
        tempList.append(startNode)
        newDistance = findDistance(tempList)
        if(newDistance < totalDistance):
            improved = True
            totalDistance = newDistance
            visitedNodes = tempList.copy()
            break
    
    edges.clear()
    for i in range(len(visitedNodes) - 1):
        edges.append((visitedNodes[i], visitedNodes[i + 1]))

    print("Best distance on round " + str(rounds) + ": " + str(findDistance(visitedNodes)))

endTime = time.perf_counter()

#print("Best solution found:")
#print(visitedNodes)
print("Total Distance: " + str(totalDistance))

print("------------------------------------------------------")
print("Execution time: " + str(endTime - startTime))
