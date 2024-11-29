import time
import copy  # Import copy module to create deep copies
import random  # Import random to randomly select neighbors

def stochastic_hill_climbing(initial_cube, objective_function, value_objective, max_iterations=100, replay_data=None):
    initial_cube_copy = copy.deepcopy(initial_cube)

    start_time = time.time()
    
    current_cube = initial_cube.copy()
    current_value = objective_function(current_cube)
    iteration = 0

    replay_data.append(current_cube.copy())

    compare_operator = (lambda x, y: x < y) if value_objective else (lambda x, y: x > y)

    while iteration < max_iterations:
        neighbors = []
        for i in range(len(current_cube)):
            neighbor = current_cube.copy()
            neighbor[i] = (neighbor[i] + 1) % 126  
            neighbor_value = objective_function(neighbor)
            neighbors.append((neighbor, neighbor_value))

        improving_neighbors = [neighbor for neighbor, value in neighbors if compare_operator(value, current_value)]

        if improving_neighbors:
            chosen_neighbor = random.choice(improving_neighbors)
            current_cube = chosen_neighbor
            current_value = objective_function(current_cube)
            replay_data.append(current_cube.copy()) 
        else:
            break

        iteration += 1

    end_time = time.time()
    runtime = end_time - start_time

    return {
        "initial_cube_copy": initial_cube_copy, 
        "final_value": current_value,
        "iterations": iteration,
        "runtime": runtime, 
        "replay_data": replay_data  
    }
