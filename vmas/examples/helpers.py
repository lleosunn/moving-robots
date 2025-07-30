import random


seed = 12
num_agents = 13
grid_scale_factor = 5
kp = 0.8
following_distance = 0.15
num_steps = 500
avoid_radius = 0.15
repulse_strength = 0.05
max_force = 0.3
spline_error = 0

def detect_collision(env):
    for i, a in enumerate(env.agents):
        for j, b in enumerate(env.agents):
            if j <= i:
                continue
            if env.scenario.world.collides(a, b):
                return True
            

def generate_random_positions(seed, agents):
    """
    seed (int): random seed
    agents (int): number of agents that need starts and goals

    generates random starts and goals for n agents
    """
    random.seed(seed)
    used_positions = set()
    starts = []
    goals = []
    for _ in range(agents):
        x = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
        y = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
        while (x, y) in used_positions:
            x = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
            y = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
        used_positions.add((x, y))
        starts.append([x, y])
    for _ in range(agents):
        x = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
        y = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
        while (x, y) in used_positions:
            x = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
            y = round(random.randint(-grid_scale_factor, grid_scale_factor) / grid_scale_factor, 2)
        used_positions.add((x, y))
        goals.append([x, y])
    return starts, goals

# starts, goals = generate_random_positions(6666, 13)
# print(f"starts = {starts}")
# print(f"goals = {goals}")