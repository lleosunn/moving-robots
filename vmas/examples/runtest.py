from leovmas4 import run_planning
from leovmas2 import run_no_planning
import csv
import random
from helpers import generate_random_positions

grid_scale_factor = 5

# dictionary of seeds for each number of agents
seeds = {
    # 2: [6629, 1431, 304, 995, 8338, 3657, 1490, 6943, 7270, 1843, 6933, 2212, 8839, 5120, 9144, 2679], 
    # 3: [841, 9095, 2805, 8310, 1369, 6562, 9952, 6862, 9764, 7693, 7811, 9982, 6300, 8866, 499, 1354], 
    # 4: [3143, 4285, 5838, 5949, 6317, 5077, 1865, 4134, 3849, 5492, 5952, 6082, 8377, 9391, 8192, 2939], 
    # 5: [461, 6240, 7047, 535, 8503, 421, 3639, 6999, 712, 6361, 3348, 9949, 1681, 9010, 3614, 2917], 
    # 6: [1277, 4485, 603, 7102, 4530, 8164, 5639, 9864, 852, 8421, 7524, 6034, 3420, 5564, 4618, 7465], 
    # 7: [7803, 7881, 3930, 2745, 7614, 8992, 5966, 2980, 3100, 3602, 9943, 109, 4395, 5599, 2941, 3958], 
    # 8: [141, 8215, 655, 4055, 1901, 5913, 8955, 8251, 2536, 391, 5283, 4578, 1935, 3760, 8639, 8228], 
    # 9: [7821, 8024, 5796, 4303, 7288, 2656, 7353, 4773, 753, 4559, 5406, 8440, 7292, 3507, 4669, 8535], 
    # 10: [4176, 468, 60, 447, 2158, 9142, 4355, 6886, 2267, 3952, 3281, 7131, 7729, 965, 9173, 9342], 
    # 11: [4225, 642, 6842, 7065, 9641, 1521, 6631, 3260, 9505, 9124, 5693, 6037, 6308, 9229, 2636, 280], 
    # 12: [2546, 506, 622, 1195, 6807, 8764, 3279, 6217, 1610, 5786, 3098, 5115, 4435, 8874, 8058, 2043], 
    # 13: [3472, 8753, 9814, 6458, 9513, 4029, 1175, 6666, 5828, 5302, 1351, 5447, 2323, 1483, 5119, 5088], 
    # 14: [2944, 7143, 5991, 2880, 490, 3426, 7994, 7270, 7952, 2938, 928, 9735, 5591, 7486, 3905, 5364], 
    15: [1587, 3677, 126, 5903, 6006, 4582, 3299, 7085, 4853, 3615, 8461, 2403, 8209, 2659, 8206, 7612],
}

starts = []
goals = []


for k, v in seeds.items():
    for seed in v:
        starts, goals = generate_random_positions(seed, k)

        collision_count, sim_time = run_planning(scenario_name="leoscenario", render=False, save_render=False, random_action=False, continuous_actions=True, n_agents=k,)

        with open("results.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["planning", seed, k, collision_count, f"{sim_time:.2f}"])
            
        collision_count, sim_time = run_no_planning(scenario_name="leoscenario", render=False, save_render=False, random_action=False, continuous_actions=True, n_agents=k,)

        with open("results.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["no_planning", seed, k, collision_count, f"{sim_time:.2f}"])
