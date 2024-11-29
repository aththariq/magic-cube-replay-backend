import random
import copy

MAGIC_CONST = 315


def buildRandomMagicCube():
    magicCube = [x for x in range(1, 126)]
    random.shuffle(magicCube)
    return magicCube

def printMagicCube(magicCube):
    for z in range(5):
        for y in range(5):
            print("[", end="")
            for x in range(5):
                print(magicCube[x + (y * 5) + (z * 25)], end="")
                if x != 4:
                    print(", ", end="")
            print("]")
        if y == 4:
            print("")

def selectorMagicCube(magicCube, x, y, z):
    return magicCube[x + (y * 5) + (z * 25)]

def findNumber(magicCube, n):
    for i in range(125):
        if magicCube[i] == n:
            return i


def lineFunction(magicCube):
    point = 0

    for k in range(5):
        for j in range(5):
            line_sum_1 = sum(magicCube[25 * k + 5 * j + i] for i in range(5))
            line_sum_2 = sum(magicCube[25 * k + 5 * i + j] for i in range(5))
            line_sum_3 = sum(magicCube[25 * j + 5 * i + k] for i in range(5))
            point += (line_sum_1 == MAGIC_CONST) + (line_sum_2 == MAGIC_CONST) + (line_sum_3 == MAGIC_CONST)

    for j in range(5):
        line_sum_1 = sum(magicCube[25 * j + 5 * i + i] for i in range(5))
        line_sum_2 = sum(magicCube[25 * j + 5 * (4 - i) + (4 - i)] for i in range(5))
        line_sum_3 = sum(magicCube[25 * i + 5 * j + i] for i in range(5))
        line_sum_4 = sum(magicCube[25 * (4 - i) + 5 * j + (4 - i)] for i in range(5))
        line_sum_5 = sum(magicCube[25 * i + 5 * i + j] for i in range(5))
        line_sum_6 = sum(magicCube[25 * (4 - i) + 5 * (4 - i) + j] for i in range(5))

        point += (line_sum_1 == MAGIC_CONST) + (line_sum_2 == MAGIC_CONST) + \
                 (line_sum_3 == MAGIC_CONST) + (line_sum_4 == MAGIC_CONST) + \
                 (line_sum_5 == MAGIC_CONST) + (line_sum_6 == MAGIC_CONST)

    # Space diagonals
    line_sum_1 = sum(magicCube[25 * i + 5 * i + i] for i in range(5))
    line_sum_2 = sum(magicCube[25 * i + 5 * i + (4 - i)] for i in range(5))
    line_sum_3 = sum(magicCube[25 * (4 - i) + 5 * i + i] for i in range(5))
    line_sum_4 = sum(magicCube[25 * (4 - i) + 5 * i + (4 - i)] for i in range(5))

    point += (line_sum_1 == MAGIC_CONST) + (line_sum_2 == MAGIC_CONST) + \
             (line_sum_3 == MAGIC_CONST) + (line_sum_4 == MAGIC_CONST)

    return point

def varFunction(magicCube):
    var = 0
    for k in range(5):
        for j in range(5):
            line_sum_1 = sum(magicCube[25 * k + 5 * j + i] for i in range(5))
            line_sum_2 = sum(magicCube[25 * k + 5 * i + j] for i in range(5))
            line_sum_3 = sum(magicCube[25 * j + 5 * i + k] for i in range(5))
            var += (line_sum_1 - MAGIC_CONST) ** 2
            var += (line_sum_2 - MAGIC_CONST) ** 2
            var += (line_sum_3 - MAGIC_CONST) ** 2

    for j in range(5):
        line_sum_1 = sum(magicCube[25 * j + 5 * i + i] for i in range(5))
        line_sum_2 = sum(magicCube[25 * j + 5 * (4 - i) + (4 - i)] for i in range(5))
        line_sum_3 = sum(magicCube[25 * i + 5 * j + i] for i in range(5))
        line_sum_4 = sum(magicCube[25 * (4 - i) + 5 * j + (4 - i)] for i in range(5))
        line_sum_5 = sum(magicCube[25 * i + 5 * i + j] for i in range(5))
        line_sum_6 = sum(magicCube[25 * (4 - i) + 5 * (4 - i) + j] for i in range(5))

        var += (line_sum_1 - MAGIC_CONST) ** 2
        var += (line_sum_2 - MAGIC_CONST) ** 2
        var += (line_sum_3 - MAGIC_CONST) ** 2
        var += (line_sum_4 - MAGIC_CONST) ** 2
        var += (line_sum_5 - MAGIC_CONST) ** 2
        var += (line_sum_6 - MAGIC_CONST) ** 2

    line_sum_1 = sum(magicCube[25 * i + 5 * i + i] for i in range(5))
    line_sum_2 = sum(magicCube[25 * i + 5 * i + (4 - i)] for i in range(5))
    line_sum_3 = sum(magicCube[25 * (4 - i) + 5 * i + i] for i in range(5))
    line_sum_4 = sum(magicCube[25 * (4 - i) + 5 * i + (4 - i)] for i in range(5))

    var += (line_sum_1 - MAGIC_CONST) ** 2
    var += (line_sum_2 - MAGIC_CONST) ** 2
    var += (line_sum_3 - MAGIC_CONST) ** 2
    var += (line_sum_4 - MAGIC_CONST) ** 2

    return var / 109


def varFitness(magicCube):
    return 1 / ((varFunction(magicCube) + 1) ** 8)

def lineFitness(magicCube):
    return (lineFunction(magicCube) + 1) * 2


functionDict = {
    "line": lineFunction,
    "var": varFunction
}

functionValueDict = {
    "line": 109,
    "var": 0
}

fitnessDict = {
    "line": lineFitness,
    "var": varFitness
}


def steepestNeighborMagicCube(magicCube, objectiveFunction, isValue):
    bestCube = copy.deepcopy(magicCube)
    swapMagicCube(bestCube, 0, 1)
    bestValue = objectiveFunction(bestCube)

    compareOperator = (lambda x, y: x >= y) if isValue else (lambda x, y: x <= y)

    for i in range(124):
        for j in range(i + 1, 125):
            swapMagicCube(magicCube, i, j)
            tempValue = objectiveFunction(magicCube)
            if compareOperator(tempValue, bestValue):
                if tempValue != bestValue:
                    bestValue = tempValue
                    bestCube = copy.deepcopy(magicCube)
                elif random.random() < 0.5:
                    bestValue = tempValue
                    bestCube = copy.deepcopy(magicCube)
            swapMagicCube(magicCube, i, j)
    return bestCube

def randomNeighbor(magicCube):
    neighborMagicCube = copy.deepcopy(magicCube)
    i, j = random.sample(range(125), 2)
    swapMagicCube(neighborMagicCube, i, j)
    return neighborMagicCube

def swapMagicCube(magicCube, i, j):
    magicCube[i], magicCube[j] = magicCube[j], magicCube[i]

if __name__ == "__main__":
    testCube = buildRandomMagicCube()
    print("Line Function Value:", lineFunction(testCube))
    print("Variance Function Value:", varFunction(testCube))
