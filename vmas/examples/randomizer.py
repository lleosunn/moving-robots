import random
from helpers import grid_scale_factor, num_agents, seed

random.seed(8954)

used_positions = set()

def generate_unique_position():
    while True:
        x = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
        y = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
        if (x, y) not in used_positions:
            used_positions.add((x, y))
            return [x, y]

starts = [generate_unique_position() for _ in range(num_agents)]
goals = [generate_unique_position() for _ in range(num_agents)]

print(f"starts = {starts}")
print(f"goals = {goals}")

def generate_random_seeds():
    seeds = {}
    used = set()
    for i in range(2, 16):
        seeds[i] = []
        for _ in range(16):
            while True:
                seed_value = random.randint(0, 10000)
                if seed_value not in used:
                    used.add(seed_value)
                    seeds[i].append(seed_value)
                    break

    return seeds

# print(generate_random_seeds())
