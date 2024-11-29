import time
import copy  

def steepest_ascent_hill_climbing(initial_cube, objective_function, is_value, replay_data):
    start_time = time.time()
    
    current_cube = initial_cube.copy()
    current_value = objective_function(current_cube)
    iteration = 0

    replay_data.append(current_cube.copy())

    while True:
        best_neighbor = None
        best_value = current_value

        for i in range(len(current_cube)):
            neighbor = current_cube.copy()
            neighbor[i] = (neighbor[i] + 1) % 126 
            neighbor_value = objective_function(neighbor)

            if is_value:
                if neighbor_value < best_value:  
                    best_neighbor = neighbor
                    best_value = neighbor_value
            else:
                if neighbor_value > best_value:  
                    best_neighbor = neighbor
                    best_value = neighbor_value

        if best_neighbor is None or best_value == current_value:
            break

        current_cube = best_neighbor
        current_value = best_value
        iteration += 1

        replay_data.append(current_cube.copy())

    end_time = time.time()
    runtime = end_time - start_time

    return {
        "final_cube": current_cube,
        "final_value": current_value,
        "iterations": iteration,
        "runtime": runtime,
        "replay_data": replay_data
    }
