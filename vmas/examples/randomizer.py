import random

grid_scale_factor = 5
num_agents = 8
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