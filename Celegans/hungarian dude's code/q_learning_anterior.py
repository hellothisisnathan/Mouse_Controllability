from Simulator import Simulator
import numpy as np
import itertools
import sys
import random
import time
import datetime

num_muscle_groups = 4
max_threshold = 25 # actually 24
min_threshold = 3
possible_thresholds = [3, 6, 9, 12, 15, 17, 20]
num_thresholds = len(possible_thresholds)
#action_space_size = (max_threshold)**num_muscle_groups
#action_space_size = num_thresholds**num_muscle_groups
action_space_size = 2233
Q = np.zeros(action_space_size)
alpha = 0.5
discount_factor = 1.0

curr_dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
TRACE_PATH = "./trace_ql_anterior_" + curr_dt

# configurations are numbered lexicografically
#def calc_config(n):
#    config = []
#    num = n
#    for i in reversed(range(num_muscle_groups)):
#        pn = num // (max_threshold**i)
#        config.append(pn)
#        num = num - pn * (max_threshold**i)
#
#    return config

def calc_config(n):
    config = []
    num = n
    for i in reversed(range(num_muscle_groups)):
        pn = num // (num_thresholds**i)
        config.append(possible_thresholds[pn])
        num = num - pn * (num_thresholds**i)

    return config

def calc_config_number(config):
    number = 0
    for i in range(num_muscle_groups):
        number += possible_thresholds.index(config[i]) * num_thresholds**i
    return number

def get_config_thersholds(config):
    thresholds = {}
    thresholds["LF"] = config[0]
    thresholds["RF"] = config[1]
    thresholds["LB"] = config[2]
    thresholds["RB"] = config[3]
    return thresholds

#action: muscle configurations
def perform_eps_greedy(Q, epsilon, num_of_actions):
    rnd = random.randint(1,100)
    action = 0
    # exploring
    if rnd <= epsilon * 100:
        action = random.randint(0, action_space_size - 1)
    else:
        action = np.argmax(Q)
    return action

def calc_reward(direction, dist):
    if dist == 0:
        return -5
    if direction == 0:
        return dist

    return -1 * dist * (abs(direction) / 360)

epsilon = 0.9
num_of_episodes = 200
start_time = time.time()
with open(TRACE_PATH, 'a') as f:
    for i_episode in range(num_of_episodes):
        direction = 0
        dist = 0

        to_print = ""
        if i_episode >= 0 and i_episode % 50 == 0:
            print("episode " + str(i_episode))
        if i_episode >= 0 and i_episode % 500 == 0:
            epsilon = max(epsilon - 0.1, 0.2)
        to_print += "episode " + str(i_episode) + "\n"

        # Simulator initialization
        sim = Simulator()
        inp = np.random.normal(1000, 200, 3)
        to_print += "input: " + "\n"
        to_print += str(inp)
        to_print += "\n"
        sim.nw.set_input_data(["AVM", "ALML", "ALMR"], inp)

        # choosing action to perform, i.e. muscle threshold config
        action = perform_eps_greedy(Q, epsilon, action_space_size)
        to_print += "action " + str(action) + "\n"
        thresholds = get_config_thersholds(calc_config(action))
        to_print += "thresholds: " + "\n"
        to_print += str(thresholds.items())
        to_print += "\n"
        sim.nw.set_muscle_group_thresholds(thresholds)

        # running simulation
        direction, dist = sim.main()
        to_print += "dir: " + str(direction) + ", dist: " + str(dist) + "\n"

        # reward based on the result
        reward = calc_reward(direction, dist)
        to_print += "REWARD: " + str(reward) + "\n"

        # TD update
        to_print += str(Q[action]) + "\n"
        Q[action] += alpha * (reward + discount_factor * Q[action] - Q[action])
        to_print += str(Q[action]) + "\n"
        f.write(to_print)
        del sim

    action = perform_eps_greedy(Q, 0, action_space_size)
    thresholds = get_config_thersholds(calc_config(action))
    to_write = str(action) + " " + str(Q[action]) + "\n" + str(thresholds.items()) + "\n"
    f.write(to_write)

    to_write = "=====================\n"
    for i in range(num_thresholds):
        to_write += str(i) + " " + str(Q[i]) + "\n"
    f.write(to_write)
    f.write("--- %s seconds ---" % (time.time() - start_time))
