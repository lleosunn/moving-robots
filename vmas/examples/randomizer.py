import random
from helpers import grid_scale_factor, num_agents

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