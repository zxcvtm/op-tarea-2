import networkx as nx
import matplotlib.pyplot as plt
import math, random, sys, time

nodeList = []
pos = {}
labels = {}

totalDistance = 0

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

if(len(sys.argv) != 2):
    print("Error al iniciar el programa, probablemente falta el nombre de archivo a cargar")
    exit(0)
else:
    loadFromFile(sys.argv[1])

edges = []

startTime = time.perf_counter()


visitedNodes = [nodeList[0]]

while(len(visitedNodes) < len(nodeList)):
    minDist = -1
    nextNode = -1
    currentNode = visitedNodes[-1]
    for i in range(len(nodeList)):
        if(i not in visitedNodes):
            x2 = pos[i][0]
            x1 = pos[currentNode][0]
            y2 = pos[i][1]
            y1 = pos[currentNode][1]

            dist = math.hypot(x2 - x1, y2 - y1)

            if(minDist == -1):
                minDist = dist
                nextNode = i
            elif(dist < minDist):
                minDist = dist
                nextNode = i
    if(nextNode != -1):
        totalDistance = totalDistance + minDist
        visitedNodes.append(nextNode)
        edges.append((currentNode, nextNode))

edges.append((visitedNodes[-1], visitedNodes[0]))

endTime = time.perf_counter()

#print(visitedNodes)
print("Total Distance: " + str(totalDistance))

print("------------------------------------------------------")
print("Execution time: " + str(endTime - startTime))


