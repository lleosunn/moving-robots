#  Copyright (c) 2022-2024.
#  ProrokLab (https://www.proroklab.org/)
#  All rights reserved.
import random
import time
import math
import torch
from vmas import make_env
from vmas.simulator.core import Agent
from vmas.simulator.utils import save_video
from helpers import (
    num_agents,
    grid_scale_factor,
    kp,
    margin_of_error,
    avoid_radius,
    repulse_strength,
    num_steps,
    max_force,
    detect_collision
)


def use_vmas_env(
    render: bool = False,
    save_render: bool = False,
    num_envs: int = 1,
    n_steps: int = num_steps,
    random_action: bool = False,
    device: str = "cpu",
    scenario_name: str = "waterfall",
    continuous_actions: bool = True,
    visualize_render: bool = True,
    dict_spaces: bool = True,
    **kwargs,
):
    """Example function to use a vmas environment

    Args:
        continuous_actions (bool): Whether the agents have continuous or discrete actions
        scenario_name (str): Name of scenario
        device (str): Torch device to use
        render (bool): Whether to render the scenario
        save_render (bool):  Whether to save render of the scenario
        num_envs (int): Number of vectorized environments
        n_steps (int): Number of steps before returning done
        random_action (bool): Use random actions or have all agents perform the down action
        visualize_render (bool, optional): Whether to visualize the render. Defaults to ``True``.
        dict_spaces (bool, optional): Weather to return obs, rewards, and infos as dictionaries with agent names.
            By default, they are lists of len # of agents
        kwargs (dict, optional): Keyword arguments to pass to the scenario

    Returns:

    """
    assert not (save_render and not render), "To save the video you have to render it"

    env = make_env(
        scenario=scenario_name,
        num_envs=num_envs,
        device=device,
        continuous_actions=continuous_actions,
        dict_spaces=dict_spaces,
        wrapper=None,
        seed=None,
        # Environment specific variables
        **kwargs,
    )
    for agent in env.agents:
        agent.render_action = True

    frame_list = []  # For creating a gif
    init_time = time.time()
    collision_count = 0
    step = 0

    for _ in range(n_steps):
        step += 1
        print(f"Step {step}")

        # VMAS actions can be either a list of tensors (one per agent)
        # or a dict of tensors (one entry per agent with its name as key)
        # Both action inputs can be used independently of what type of space its chosen
        dict_actions = random.choice([True, False])

        actions = {} if dict_actions else []
        for agent in env.agents:
            if not random_action:
                # Simple P controller with collision avoidance
                goal_pos = agent.goal.state.pos
                agent_pos = agent.state.pos
                error = goal_pos - agent_pos
                kp = 0.8
                attractive_force = kp * error

                # Collision avoidance
                repulsive_force = torch.zeros_like(attractive_force)

                for other in env.agents:
                    if other is agent:
                        continue
                    other_pos = other.state.pos
                    vec = agent_pos - other_pos
                    dist = torch.norm(vec)
                    if dist < avoid_radius and dist > 1e-6:
                        repulsive_force += repulse_strength * vec / dist**2

                # Combine and cap force
                force = attractive_force + repulsive_force
                force_norm = torch.norm(force)
                if force_norm > max_force:
                    force = force / force_norm * max_force

                u_range = agent.action.u_range_tensor
                if u_range.dim() == 1:
                    u_range = u_range.view(1, -1)
                action = torch.clamp(force, -u_range, u_range)
            else:
                action = env.get_random_action(agent)
            if dict_actions:
                actions.update({agent.name: action})
            else:
                actions.append(action)

        obs, rews, dones, info = env.step(actions)

        if dones.all():
            print("All agents reached their goals!")
            break

        # Check for collisions
        if detect_collision(env):
            collision_count += 1
            print("Collision detected!")

        if render:
            frame = env.render(
                mode="rgb_array",
                agent_index_focus=None,  # Can give the camera an agent index to focus on
                visualize_when_rgb=visualize_render,
            )
            if save_render:
                frame_list.append(frame)

    total_time = time.time() - init_time
    # print(
    #     f"It took: {total_time}s for {n_steps} steps of {num_envs} parallel environments on device {device} "
    #     f"for {scenario_name} scenario."
    # )
    # print(f"Total collisions detected: {collision_count}")

    print(f"{num_agents} robots, {collision_count} collisions, {total_time:.2f}s")


    if render and save_render:
        save_video(scenario_name, frame_list, fps=1 / env.scenario.world.dt)


if __name__ == "__main__":
    use_vmas_env(
        scenario_name="leoscenario",
        render=True,
        save_render=False,
        random_action=False,
        continuous_actions=True,
        # Environment specific
        n_agents=num_agents,
    )
