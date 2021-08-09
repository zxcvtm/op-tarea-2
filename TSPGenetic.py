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

popSize = 100
mutationProb = 0.05
nCanditates = 5

if(len(sys.argv) != 5):
    print("Error al iniciar el programa, probablemente falta el nombre de archivo a cargar")
    exit(0)
else:
    loadFromFile(sys.argv[1])
    popSize = int(sys.argv[2])
    nCanditates = int(sys.argv[3])
    mutationProb = float(sys.argv[4])

startTime = time.perf_counter()


population = []

#Inicialización de la población
for i in range(popSize):
    genes = nodeList.copy()
    del genes[0]
    random.shuffle(genes)
    distance = findDistance(genes)
    population.append([genes, distance])

generations = 0

bestDistance = math.inf
bestGenes = []

#"El algoritmo genético"
while((time.perf_counter() - startTime) < 200):
    parents = []
    midPoint = 0
    generations = generations + 1

    #Selección de los padres por torneo
    participants = population.copy()
    for i in range(popSize):
        random.shuffle(participants)
        candidates = participants[0:(nCanditates-1)]
        candidates.sort(key = sorting)

        selected = candidates[0]

        parents.append(selected)

    population = []
    #Operación de cruza con operador OX
    # P1 = (3 4 8 ∣ 2 7 1 ∣ 6 5)
    # P2 = (4 2 5 | 1 6 8 | 3 7)
    # 
    # O1 = (X X X | 2 7 1 | X X)
    # O2 = (X X X | 1 6 8 | X X)
    # 
    # O1 = (5 6 8 | 2 7 1 | 3 4)
    # O2 = (4 2 7 | 1 6 8 | 5 3)  
    for i in range(0, len(parents) - 1, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        crossPoint1 = random.randint(0, len(parent1[0]) - 2)
        crossPoint2 = crossPoint1 + random.randint(1, len(parent1[0]) - crossPoint1 - 1)
        genes1 = []
        genes2 = []
        for j in range(len(parent1[0])):
            if(crossPoint1 <= j <= crossPoint2):
                genes1.append(parent1[0][j])
                genes2.append(parent2[0][j])
            else:
                genes1.append(None)
                genes2.append(None)

        k = crossPoint2 + 1
        p = k
        for j in range(len(parent1[0])):
            if(k >= len(parent1[0])):
                k = 0
            if(p >= len(parent1[0])):
                p = 0
            if(parent2[0][k] not in genes1):
                genes1[p] = parent2[0][k]
                k = k + 1
                p = p + 1
            else:
                k = k + 1
            
            if(None not in genes1):
                break

        k = crossPoint2 + 1
        p = k
        for j in range(len(parent2[0])):
            if(k >= len(parent2[0])):
                k = 0
            if(p >= len(parent2[0])):
                p = 0
            if(parent1[0][k] not in genes2):
                genes2[p] = parent1[0][k]
                k = k + 1
                p = p + 1
            else:
                k = k + 1
            
            if(None not in genes2):
                break

        #Mutación con una probablilidad de 0.05 (5%)
        if(random.random() < mutationProb):
            swap1 = random.randint(0, len(genes1) - 1)
            swap2 = random.randint(0, len(genes1) - 1)

            aux = genes1[swap1]
            genes1[swap1] = genes1[swap2]
            genes1[swap2] = aux
        
        if(random.random() < mutationProb):
            swap1 = random.randint(0, len(genes2) - 1)
            swap2 = random.randint(0, len(genes2) - 1)

            aux = genes2[swap1]
            genes2[swap1] = genes2[swap2]
            genes2[swap2] = aux

        if(findDistance(genes1) < bestDistance):
            bestDistance = findDistance(genes1)
            bestGenes = genes1

        if(findDistance(genes2) < bestDistance):
            bestDistance = findDistance(genes2)
            bestGenes = genes2

        #Agregamos los hijos a la nueva población de la siguiente generación, junto con su fitness
        population.append([genes1, findDistance(genes1)])
        population.append([genes2, findDistance(genes2)])
    
    print("Best distance on generation " + str(generations) + ": " + str(bestDistance))

endTime = time.perf_counter()

#Mostramos los datos del mejor camino de la última generación
bestRoad = [0] + bestGenes + [0]

#print("Best road over " + str(generations) + " generations: " + str(bestRoad))
print("Road distance: " + str(findDistance(bestRoad)))

print("------------------------------------------------------")
print("Execution time: " + str(endTime - startTime))


