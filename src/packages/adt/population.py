from ..adt.magicCube import buildRandomMagicCube, functionDict, fitnessDict, functionValueDict, swapMagicCube
import copy

class Individual:
    def __init__(self, magicCube, objectiveFunction, fitnessFunction):
        self.magicCube = magicCube
        self.value = objectiveFunction(magicCube)
        self.fitness = fitnessFunction(magicCube)
        self.next = None

    def display(self):
        print(f"Magic Cube Start Value: {self.magicCube[0]}, Objective Value: {self.value}")

class Population:
    def __init__(self):
        self.head = None
        self.tail = None
        self.totalValue = 0
        self.totalFitness = 0
        self.count = 0
        self.bestState = None

    def append(self, magicCube, objectiveFunction, fitnessFunction, isValue):
        compareOperator = (lambda x, y: x > y) if isValue else (lambda x, y: x < y)
        newNode = Individual(magicCube, objectiveFunction, fitnessFunction)

        if not self.head:
            self.head = newNode
            self.bestState = newNode
        else:
            self.tail.next = newNode
            if compareOperator(newNode.value, self.bestState.value):
                self.bestState = newNode
        self.tail = newNode
        self.totalValue += newNode.value
        self.totalFitness += newNode.fitness
        self.count += 1

    def merge(self, otherPopulation, isValue):
        compareOperator = (lambda x, y: x > y) if isValue else (lambda x, y: x < y)

        if self.head and otherPopulation.head:
            self.tail.next = otherPopulation.head
            self.tail = otherPopulation.tail
            self.totalValue += otherPopulation.totalValue
            self.totalFitness += otherPopulation.totalFitness
            self.count += otherPopulation.count
            if compareOperator(otherPopulation.bestState.value, self.bestState.value):
                self.bestState = otherPopulation.bestState

        elif not self.head:
            self.head = otherPopulation.head
            self.tail = otherPopulation.tail
            self.totalValue = otherPopulation.totalValue
            self.totalFitness = otherPopulation.totalFitness
            self.count = otherPopulation.count
            self.bestState = otherPopulation.bestState

    def indexSearch(self, index):
        if index < self.count:
            current = self.head
            for _ in range(index):
                current = current.next
            return current
        return None

    def weightedSearch(self, selection):
        selection *= self.totalFitness
        current = self.head
        cumulative_fitness = current.fitness

        while cumulative_fitness < selection and current.next:
            current = current.next
            cumulative_fitness += current.fitness

        return current

    def display(self):
        print(f"Population Count: {self.count}, Best State Value: {self.bestState.value}")
        current = self.head
        while current:
            print(f"{current.magicCube[0]}: {current.value}", end=" -> ")
            current = current.next
        print("None")

    def deepcopy(self, objectiveFunction, fitnessFunction, isValue):
        populationCopy = Population()
        current = self.head
        while current:
            populationCopy.append(copy.deepcopy(current.magicCube), objectiveFunction, fitnessFunction, isValue)
            current = current.next
        return populationCopy

    def countDuplicate(self):
        current = self.head
        cubes_seen = []
        duplicates = 0
        while current:
            if current.magicCube in cubes_seen:
                duplicates += 1
            else:
                cubes_seen.append(current.magicCube)
            current = current.next
        return duplicates

    def checkChildren(self, child1, child2):
        current = self.head
        found1 = False
        found2 = False
        while current and (not found1 or not found2):
            if not found1 and current.magicCube == child1:
                found1 = True
            if not found2 and current.magicCube == child2:
                found2 = True
            current = current.next
        return found1, found2

if __name__ == "__main__":
    function = "var"
    objective = functionDict[function]
    fitness = fitnessDict[function]
    value = functionValueDict[function]

    testPopulation = Population()
    for _ in range(5):
        testPopulation.append(buildRandomMagicCube(), objective, fitness, value)
    testPopulation.display()

    otherPopulation = Population()
    for _ in range(3):
        otherPopulation.append(buildRandomMagicCube(), objective, fitness, value)
    otherPopulation.display()

    testPopulation.merge(otherPopulation, value)
    testPopulation.display()

    copyPopulation = testPopulation.deepcopy(objective, fitness, value)
    swapMagicCube(testPopulation.head.magicCube, 0, 1)
    print("\nAfter swapping first cube in testPopulation:")
    testPopulation.display()
    print("\nCopy of the original population:")
    copyPopulation.display()
