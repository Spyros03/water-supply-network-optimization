"""
Configuration file for the water supply network optimization.
The provided default values has been defined though various tests they might not be optimal and the might need to be
altered depending on the problem that is being optimized.
"""

# Default values.
num_of_generations = 1000000  # 100000
sol_per_pop = 100  # 100
num_of_parents_mating = 5  # 5
mutation_probability = 1e-7  # 1e-7
keep_elitism = 10  # 10
available_diameters = [55.4, 66.0, 79.2, 96.8, 110.2, 123.4, 141.0, 158.6, 176.2, 198.2, 220.4, 246.8, 277.6, 312.8,
                       352.6, 396.6, 440.6, 493.6, 555.2]

# [55.4, 66.0, 79.2, 96.8, 110.2, 123.4, 141.0, 158.6, 176.2, 198.2, 220.4, 246.8, 277.6, 312.8,
# 352.6, 396.6, 440.6, 493.6, 555.2]

print_solution = True
