import math
import random
import copy
import time
from ..adt.magicCube import *

def decision(probability):
    return (random.random() < probability)

def simulatedAnnealingAlgorithm(initial_cube, T, objective_function, value_objective, replay_data):
    try:
        start = time.time()
        magic_cube = copy.deepcopy(initial_cube)

        operator_difference = (lambda x, y: x - y) if value_objective else (lambda x, y: y - x)

        sa_formula_array = []
        value_array = []
        iteration = 0
        current_value = objective_function(magic_cube)
        value_array.append(current_value)
        sa_formula = 0

        replay_data.append(copy.deepcopy(magic_cube))

        while T > 0 and current_value != value_objective:
            index1, index2 = random.sample(range(125), 2)
            swapMagicCube(magic_cube, index1, index2)
            successor_value = objective_function(magic_cube)
            difference = operator_difference(successor_value, current_value)
            
            if difference >= 0:
                current_value = successor_value
                sa_formula_array.append(1)
            else:
                sa_formula = math.exp(difference / T)
                sa_formula_array.append(sa_formula)
                if decision(sa_formula):
                    current_value = successor_value
                else:
                    swapMagicCube(magic_cube, index1, index2)

            value_array.append(current_value)
            iteration += 1
            T *= 0.999  

            if T <= 1e-38:
                T = 0 

            replay_data.append(copy.deepcopy(magic_cube))

        runtime = time.time() - start

        return {
            "final_cube": magic_cube,
            "final_value": current_value,
            "runtime": runtime,
            "iterations": iteration,
            "replay_data": replay_data
        }

    except Exception as e:
        print(f"Error in simulatedAnnealingAlgorithm: {e}")
        raise e 
