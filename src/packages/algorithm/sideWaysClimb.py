import time
import copy  

def hill_climbing_with_sideways(initial_cube, objective_function, value_objective, max_sideways_moves=20, replay_data=None):
    
    initial_cube_copy = copy.deepcopy(initial_cube)

    start_time = time.time()
    
    current_cube = initial_cube.copy()
    current_value = objective_function(current_cube)
    iteration = 0
    sideways_moves = 0

    replay_data.append(current_cube.copy())

    compare_operator = (lambda x, y: x < y) if value_objective else (lambda x, y: x > y)

    while True:
        best_neighbor = None
        best_value = current_value

        for i in range(len(current_cube)):
            neighbor = current_cube.copy()
            neighbor[i] = (neighbor[i] + 1) % 126 
            neighbor_value = objective_function(neighbor)

            if compare_operator(neighbor_value, best_value):
                best_neighbor = neighbor
                best_value = neighbor_value

        if best_neighbor is None or best_value == current_value:
            if sideways_moves < max_sideways_moves:
                current_cube = best_neighbor
                current_value = best_value
                sideways_moves += 1
                replay_data.append(current_cube.copy())  
            else:
                break
        else:
            current_cube = best_neighbor
            current_value = best_value
            sideways_moves = 0  
            replay_data.append(current_cube.copy())  
        iteration += 1

    end_time = time.time()
    runtime = end_time - start_time

    return {
        "final_cube": current_cube,
        "final_value": current_value,
        "iterations": iteration,
        "replay_data": replay_data  
    }
