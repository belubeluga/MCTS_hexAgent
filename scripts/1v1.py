"""NO COMMITEAR CAMBIOS EN ESTE ARCHIVO!"""

""" 1v1 between two agents """

import time

import gymnasium as gym
from tournament_utils import process_names

# **Import the agents HERE!**
from agents.test_agents.half import HalfAgent
from agents.test_agents.human import HumanAgent
from agents.test_agents.randy import RandomAgent
from agents.test_agents.click import ClickAgent
from agents.test_agents.first import FirstAgent
from agents.test_agents.center import CenterAgent
from agents.test_agents.cross import CrossAgent
from agents.test_agents.anti import AntiAgent
from agents.test_agents.gandalf import GandalfAgent
from agents.test_agents.smart1 import SmartAgent1
from agents.test_agents.randomLine import RandomLine


import hex_udesa

# **Add your agents HERE!**
agent1 = RandomLine()
agent2 = CenterAgent()

ROUNDS = 1
SIZE = 7
names = process_names(agent1, agent2)

env = gym.make(
    "hex_udesa/Hex-v0",
    render_mode="human",  # use "console" if nice graphics not working
    max_episode_steps=SIZE * SIZE + 1,
    board_size=SIZE,
)

board, _ = env.reset(options=names)
env.render()
terminated, truncated = False, False
n = 0
while not terminated and not truncated:
    if n % 2 == 0:
        if isinstance(agent1, ClickAgent):
            action = agent1.action(board, env)
        else:
            action = agent1.action(board)

        board, reward1, terminated, truncated, info = env.step(action)
    else:
        # 1) Transpose and flip signs so agent2 sees itself as +1 left–right
        board_for_agent2 = board.T * -1

        # 2) Ask agent2 for a move index in [0..SIZE*SIZE-1]
        if isinstance(agent2, ClickAgent):
            action_transposed = agent2.action(board_for_agent2, env)
        else:
            action_transposed = agent2.action(board_for_agent2)

        # 3) Convert that move index (in the transposed board) to (row_t, col_t)
        row_t, col_t = divmod(action_transposed, SIZE)

        # 4) "Untranspose" => (row_env, col_env) in the real board
        row_env, col_env = col_t, row_t
        action_env = row_env * SIZE + col_env

        # 5) Step in the real environment using the environment-based action
        board, reward2, terminated, truncated, info = env.step(action_env)

    n += 1
    env.render()
    time.sleep(0.2)
if reward1:
    print(f"{str(agent1)} won!")
elif reward2:
    print(f"{str(agent2)} won!")
else:
    print("It's a tie!")
time.sleep(1)
