import copy
import time
import math

def random_restart_hill_climbing(initial_cube, objective_function, max_restarts=3, max_iterations_per_restart=100, replay_data=None):
    initial_cube_copy = copy.deepcopy(initial_cube)

    start_time = time.time()
    
    best_solution = None
    best_value = math.inf  
    total_iterations = 0

    replay_data = replay_data or []

    for restart in range(max_restarts):
        current_cube = initial_cube.copy()
        current_value = objective_function(current_cube)
        iteration = 0
        sideways_moves = 0
        max_sideways_moves = 20  

    
        replay_data.append(copy.deepcopy(current_cube))

        while iteration < max_iterations_per_restart:
            best_neighbor = None
            best_neighbor_value = current_value

            for i in range(len(current_cube)):
                neighbor = current_cube.copy()
                neighbor[i] = (neighbor[i] + 1) % 126  
                neighbor_value = objective_function(neighbor)

                if neighbor_value < best_neighbor_value:
                    best_neighbor = neighbor
                    best_neighbor_value = neighbor_value

            if best_neighbor and best_neighbor_value < current_value:
                current_cube = best_neighbor
                current_value = best_neighbor_value
                sideways_moves = 0  
                replay_data.append(copy.deepcopy(current_cube))
            else:
                sideways_moves += 1
                if sideways_moves >= max_sideways_moves:
                    break  
                else:
                    pass

            iteration += 1
            total_iterations += 1

   
            if current_value < best_value:
                best_value = current_value
                best_solution = copy.deepcopy(current_cube)


    end_time = time.time()
    runtime = end_time - start_time

    return {
        "initial_cube_copy": initial_cube_copy,
        "final_cube": best_solution,
        "final_value": best_value,
        "iterations": total_iterations,
        "runtime": runtime,
        "replay_data": replay_data  
    }
