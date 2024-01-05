from HydroNetwork import *
from HydroOptimizationIO import *
from pygad import GA
import time
import common
import config
import platform


def fitness_function(ga_instance, solution, solution_idx) -> float:
    """Fitness function to be used for PYGAD genetic algorithm optimization."""
    solution_list = solution.tolist()
    network = HydroNetwork(common.nodes, common.pipes)
    network.set_pipe_diameters(solution_list)
    network.solve_network()
    violations = 0
    fitness = 0
    for pipe in network.get_pipes():
        fitness -= pipe.get_length()*pipe.get_pipe_diameter()
    for node in network.get_nodes():
        if isinstance(node, HydroReservoir):
            continue
        if not node.has_enough_pressure():
            violations += abs(node.get_actual_pressure() - node.get_pressure_demand())
    fitness -= abs(fitness*0.1*violations)
    if config.print_solution:
        print_solution(solution_list, fitness)
    return fitness


def print_solution(solution, fitness):
    print('solution:', solution)
    print('fitness:', fitness)
    print('local time:', time.localtime().tm_hour, ':', time.localtime().tm_min, ':', time.localtime().tm_sec)


def is_restriction_satisfied(network) -> bool:
    for node in network.get_nodes():
        if isinstance(nodes, HydroReservoir):
            continue
        if not node.has_enough_pressure():
            return False
    return True


def optimize():
    hydro_read_csv()
    optimization = GA(fitness_func=fitness_function, num_generations=config.num_of_generations,
                      num_parents_mating=config.num_of_parents_mating, sol_per_pop=config.sol_per_pop,
                      num_genes=len(common.pipes), mutation_probability=config.mutation_probability,
                      gene_space=config.available_diameters, gene_type=float, keep_elitism=config.keep_elitism)
    optimization.run()
    optimal_solution, optimal_solution_fitness, temp = optimization.best_solution()
    print('Optimal or near-optimal solution found:', optimal_solution)
    print('Optimal solution fitness:', optimal_solution_fitness)
    optimization.plot_fitness()
    optimal_network = HydroNetwork(common.nodes, common.pipes)
    if not is_restriction_satisfied(optimal_network):
        print("Warning!! some node pressure demand is not satisfied!")
    optimal_network.set_pipe_diameters(optimal_solution)
    optimal_network.solve_network()
    hydro_write_csv(optimal_network)


def main():
    common.os_name = platform.system()
    if not (common.os_name == "Windows" or common.os_name == "Linux"):
        raise OSError("This operating system is not supported. Try Windows or Linux.")
    optimize()


if __name__ == "__main__":
    main()
