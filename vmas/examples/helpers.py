import torch

num_agents = 15
grid_scale_factor = 5
kp = 0.8
margin_of_error = 0.1
num_steps = 400
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