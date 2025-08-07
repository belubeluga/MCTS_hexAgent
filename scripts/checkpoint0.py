"""NO COMMITEAR CAMBIOS EN ESTE ARCHIVO!"""

"""Test file for checkpoint 0.
tests methods:
    - action
    - name
    - reset
    - __str__"""

import time
from itertools import permutations
import os
import glob
import importlib
import inspect
import gymnasium as gym
import tqdm
import trueskill
from tournament_utils import print_results
import hex_udesa
from agents.test_agents.adjacent import AdjacentAgent
from agents.test_agents.anti import AntiAgent
from agents.test_agents.bad import BadAgent
from agents.test_agents.center import CenterAgent
from agents.test_agents.first import FirstAgent
from agents.test_agents.half import HalfAgent
from agents.test_agents.randy import RandomAgent

AGENTS = {
    RandomAgent(),
    FirstAgent(),
    AdjacentAgent(),
    CenterAgent(),
    AntiAgent(),
    HalfAgent(),
    # BadAgent(),
}
RENDERED = True

script_dir = os.path.dirname(os.path.abspath(__file__))
agents_dir = os.path.join(script_dir, "agents")

for agent_dir in os.listdir(agents_dir):
    if agent_dir == "test_agents":
        continue
    agents_path = os.path.join(agents_dir, agent_dir)
    modules = [
        os.path.basename(f)[:-3]
        for f in glob.glob(os.path.join(agents_path, "*.py"))
        if not (os.path.basename(f)[0] == "_" or os.path.basename(f)[0] == ".")
    ]
    stripped_path = os.path.relpath(agents_path, script_dir).replace(os.sep, ".")
    for module in modules:
        mod = importlib.import_module(stripped_path + "." + module)
        for name, obj in inspect.getmembers(mod):
            try:
                if inspect.isclass(obj) and hasattr(obj, "action"):
                    AGENTS.add(obj())
            except Exception:
                continue

for agent in AGENTS:
    # test __str__
    agent.notes = ""
    if not hasattr(agent, "__str__"):
        agent.notes += "No __str__ method implemented. "
    else:
        if not isinstance(agent.__str__(), str):
            agent.notes += "__str__ should return a string. "

    # test method name()
    try:
        if not hasattr(agent, "name"):
            if not hasattr(agent, "names"):
                agent.notes += "No name() method implemented. "
            else:
                agent.notes += "rename names() to name(). "
        else:
            if not isinstance(agent.name(), dict):
                agent.notes += "name() should return a dict. "
            else:
                if not agent.name()["legajo"]:
                    agent.notes += "name() should return a dict with legajo. "
    except:
        agent.notes += "agent.name() failed. "

    # test action
    if not hasattr(agent, "action"):
        agent.notes += "No action() method implemented. "

    # test reset
    if not hasattr(agent, "reset"):
        agent.notes += "No reset() method implemented. "

    # test no invalid moves

    SIZE = 15

    env = gym.make(
        "hex_udesa/Hex-v0",
        render_mode=None,
        max_episode_steps=15 * 15 + 1,
        board_size=15,
    )
    obs, _ = env.reset()
    terminated, truncated = False, False
    while not terminated and not truncated:
        num_non_zero = len(obs[obs != 0])
        action = agent.action(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        if num_non_zero == len(obs[obs != 0]):
            agent.notes += "Agent takes invalid moves."
            break

    # test smaller board 3x3
    SIZE = 3
    env = gym.make(
        "hex_udesa/Hex-v0",
        render_mode=None,
        max_episode_steps=3 * 3 + 1,
        board_size=3,
    )
    obs, _ = env.reset()
    terminated, truncated = False, False
    try:
        while not terminated and not truncated:
            action = agent.action(obs)
            if action is None or action > SIZE * SIZE:
                agent.notes += "Agent fails in smaller boards."
                break
            obs, reward, terminated, truncated, info = env.step(action)
    except:
        agent.notes += "Agent fails in smaller boards."

    if agent.notes == "":
        agent.notes = "OK"

# print errors
for agent in AGENTS:
    print(f"{str(agent):30} {agent.notes}")
