import math
import random
import copy
import time
from ..adt.population import Population
from ..adt.magicCube import (
    buildRandomMagicCube,
    functionDict,
    fitnessDict,
    functionValueDict,
    findNumber,
    swapMagicCube,
    randomNeighbor
)

def crossover(parent1, parent2):
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    split = math.floor(random.normalvariate(125 / 2, 125 / 8))
    while split < 0 or split >= 125:
        split = math.floor(random.normalvariate(125 / 2, 125 / 8))

    for i in range(split):
        childIndex1 = findNumber(child1, parent2[i])
        childIndex2 = findNumber(child2, parent1[i])
        swapMagicCube(child1, childIndex1, i)
        swapMagicCube(child2, childIndex2, i)

    return child1, child2

def mutation(magicCube):
    mutant = copy.deepcopy(magicCube)
    for _ in range(20):
        mutant = randomNeighbor(mutant)
    return mutant

def geneticAlgorithm(initialPopulation, maxIteration, objectiveFunction, fitnessFunction, isValue, replay_data=None):
    """
    Run the Genetic Algorithm to find the best solution.
    Returns the result in a structured format suitable for frontend.
    """
    if replay_data is None:
        replay_data = []

    try:
        start = time.time()
        averageValueHistory = []
        bestValueHistory = []
        population = initialPopulation.deepcopy(objectiveFunction, fitnessFunction, isValue)

        averageValueHistory.append(population.totalValue / population.count)
        bestValueHistory.append(population.bestState.value)

        iteration = 0

        replay_data.append(copy.deepcopy(population.magicCubes))

        while iteration < maxIteration:
            childrenPopulation = Population()
            for _ in range(population.count // 2):
                parent1 = population.weightedSearch(random.random()).magicCube
                parent2 = population.weightedSearch(random.random()).magicCube

                while parent1 == parent2:
                    parent2 = population.weightedSearch(random.random()).magicCube

                child1, child2 = crossover(parent1, parent2)
                if random.random() < 0.5:
                    child1 = mutation(child1)
                if random.random() < 0.5:
                    child2 = mutation(child2)

                childrenPopulation.append(child1, objectiveFunction, fitnessFunction, isValue)
                childrenPopulation.append(child2, objectiveFunction, fitnessFunction, isValue)

            population.merge(childrenPopulation, isValue)
            averageValueHistory.append(population.totalValue / population.count)
            bestValueHistory.append(population.bestState.value)
            replay_data.append(copy.deepcopy(population.magicCubes))  

            print(f"Iteration {iteration}, Time Elapsed: {time.time() - start:.2f}s")
            if population.bestState.value == functionValueDict[objectiveFunction.__name__]:
                break
            iteration += 1

        runtime = time.time() - start
        return {
            "final_population": population,
            "best_magic_cube": population.bestState.magicCube,
            "best_value": population.bestState.value,
            "best_value_history": bestValueHistory,
            "average_value_history": averageValueHistory,
            "population_count": population.count,
            "iterations": iteration,
            "runtime": runtime,
            "replay_data": replay_data
        }

    except Exception as e:
        print(f"Error in geneticAlgorithm: {e}")
        raise e

__all__ = ["geneticAlgorithm"]
