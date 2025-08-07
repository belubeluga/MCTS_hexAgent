"""NO COMMITEAR CAMBIOS EN ESTE ARCHIVO!"""

"""swiss torunament for gomoku_udesa"""
import glob
import importlib
import inspect
import os
import random
from threading import Timer

import gymnasium as gym
import tqdm
import trueskill
from tournament_utils import (
    HiddenPrints,
    competition_match,
    evaluate_agent_moves,
    evaluate_code_quality,
    print_disqualified_agents,
    print_final_results,
    print_full_final_table,
    set_seeds,
)

import hex_udesa

set_seeds()

from agents.test_agents.adjacent import AdjacentAgent
from agents.test_agents.anti import AntiAgent
from agents.test_agents.bad import BadAgent
from agents.test_agents.center import CenterAgent
from agents.test_agents.first import FirstAgent
from agents.test_agents.half import HalfAgent
from agents.test_agents.human import HumanAgent
from agents.test_agents.randy import RandomAgent
from agents.test_agents.cross import CrossAgent
from agents.test_agents.gandalf import GandalfAgent
from agents.test_agents.smart1 import SmartAgent1

AGENTS = [
    RandomAgent(),
    RandomAgent(),
    RandomAgent(),
    RandomAgent(),
    RandomAgent(),
    FirstAgent(),
    AdjacentAgent(),
    CenterAgent(),
    AntiAgent(),
    HalfAgent(),
    BadAgent(),
    CrossAgent(),
    GandalfAgent(),
    SmartAgent1(),
]
RENDERED = False
ROUNDS = 5
REPEAT_SWISS = 3
MAX_ALLOWED_TIME = 0.1  # seconds
SIZE = 13


def timeout_handler():
    raise TimeoutError()


timer = Timer(2.0, timeout_handler)

print("Loading agents")
for agent_path in tqdm.tqdm(os.listdir("scripts" + os.sep + "agents")):
    try:
        with HiddenPrints():
            timer.start()
            if agent_path == "test_agents":
                continue
            agents_path = "agents" + os.sep + agent_path
            path = "scripts" + os.sep + agents_path
            modules = [
                os.path.basename(f)[:-3]
                for f in glob.glob(path + os.sep + "*.py")
                if not (os.path.basename(f)[0] == "_" or os.path.basename(f)[0] == ".")
            ]
            stripped_path = os.path.relpath(agents_path).replace(os.sep, ".")
            for module in modules:
                try:
                    mod = importlib.import_module(stripped_path + "." + module)
                except Exception:
                    continue
                for name, obj in inspect.getmembers(mod):
                    try:
                        if inspect.isclass(obj) and hasattr(obj, "action"):
                            AGENTS.append(obj())
                    except Exception:
                        continue
    except TimeoutError:
        print(f"Timeout for: {agent_path}")
    finally:
        timer.cancel()
        timer = Timer(2.0, timeout_handler)

print("Evaluating agents coding quality")
evaluate_code_quality(AGENTS)

for agent in AGENTS:
    if agent.notes == "":
        agent.notes = "OK"
    agent.matches = 0
    agent.errors = 0
    agent.timeouts = 0

    env = gym.make(
        "hex_udesa/Hex-v0",
        render_mode="human" if RENDERED else None,
        max_episode_steps=SIZE * SIZE + 1,
        board_size=SIZE,
    )

working_agents = []

for agent in AGENTS:
    agent.rating = trueskill.Rating()
    if agent.notes == "OK":
        working_agents.append(agent)

print("Start competition")

unique_legajos = set([a.name()["legajo"] for a in working_agents])
assert len(unique_legajos) > ROUNDS, f"Too many rounds ({ROUNDS}) for this few agents"

for tournament in range(REPEAT_SWISS):
    print(f"\n--Swiss Tournament N°{tournament + 1}--")
    already_played_matches = {id(a): [] for a in working_agents}
    for round in range(ROUNDS):
        print(f"Round {round + 1}")
        # sort agents by rating
        working_agents.sort(
            key=lambda x: x.rating.mu - 3 * x.rating.sigma, reverse=True
        )
        # play against each other in a swiss tournament
        for i, j in tqdm.tqdm(
            # list(zip(range(len(working_agents)), range(1, len(working_agents))))
            list(
                zip(range(0, len(working_agents), 2), range(1, len(working_agents), 2))
            )
        ):
            agent_i = working_agents[i]
            agent_j = working_agents[j]
            if len(already_played_matches[id(agent_i)]) == len(working_agents) - 1:
                continue

            while id(agent_j) in already_played_matches[id(agent_i)] or int(
                agent_i.name()["legajo"]
            ) == int(agent_j.name()["legajo"]):
                j = (j + 1) % len(working_agents)
                agent_j = working_agents[j]
            competition_match(agent_i, agent_j, env, MAX_ALLOWED_TIME, RENDERED)
            competition_match(agent_j, agent_i, env, MAX_ALLOWED_TIME, RENDERED)

            already_played_matches[id(agent_i)].append(id(agent_j))
            already_played_matches[id(agent_j)].append(id(agent_i))


        for agent in AGENTS:
            if agent.matches > 5:
                total_ratio = (agent.errors + agent.timeouts) / agent.matches
                error_ratio = agent.errors / agent.matches
                timeout_ratio = agent.timeouts / agent.matches
                if total_ratio > 0.2:
                    # Decide which category is causing disqualification
                    if error_ratio > 0.2 and timeout_ratio <= 0.2:
                        agent.notes = (
                            f"Disqualified: error rate {error_ratio:.2%} (>20%) after {agent.matches} matches."
                        )
                    elif timeout_ratio > 0.2 and error_ratio <= 0.2:
                        agent.notes = (
                            f"Disqualified: timeout rate {timeout_ratio:.2%} (>20%) after {agent.matches} matches."
                        )
                    else:
                        # Both rates above 20%, or just total ratio above 20% combined
                        agent.notes = (
                            "Disqualified: combined error+timeout rate "
                            f"{total_ratio:.2%} (>20%) after {agent.matches} matches "
                            f"(errors={error_ratio:.2%}, timeouts={timeout_ratio:.2%})."
                        )


        working_agents = [a for a in working_agents if a.notes == "OK"]

    working_agents.sort(key=lambda x: x.rating.mu - 3 * x.rating.sigma, reverse=True)
    print_final_results(working_agents)

for agent in AGENTS:
    if agent.matches > 5 and (agent.errors + agent.timeouts) / agent.matches > 0.2:
        agent.notes = "Error + timeout rate > 20%"

disqualified_agents = []
working_agents = []

for agent in AGENTS:
    if agent.notes != "OK":
        disqualified_agents.append(agent)
    else:
        working_agents.append(agent)
print("\n--Final results--")
print_final_results(working_agents)
print_full_final_table(working_agents)
print_disqualified_agents(disqualified_agents)
