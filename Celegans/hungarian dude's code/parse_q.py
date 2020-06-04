import sys
import numpy as np
from matplotlib import pyplot as plt

INPUT_FILE = "./" + sys.argv[1]
Q = np.zeros(2233)

act_id = 0
rewards = []
counter = 0
with open(INPUT_FILE, 'r') as f:
    for line in f:
        counter += 1
        splitted = line.strip().split()
        if splitted[0] == "action":
            act_id = int(splitted[1])
            counter = 0
        elif counter == 6:
            Q[act_id] = float(line.strip())

        if splitted[0] == "REWARD:":
            rewards.append(float(splitted[1]))

print(Q)
print(np.max(Q))
print(np.mean(rewards))

index = np.array([x for x in np.arange(2233)])
fig = plt.figure(figsize = (6, 5), dpi = 200)
ax = plt.subplot(111)
ax.bar(index, Q, width = 1, color = 'r', align = 'center')

plt.xlabel("Actions")
plt.ylabel("Value", rotation = 90, labelpad = 10)
plt.title("Action-Value graph")
plt.savefig("actval_" + sys.argv[1] + ".png", dpi = 200)
plt.close(fig)

index = np.array([x for x in np.arange(20000)])
fig = plt.figure(figsize = (7, 5), dpi = 400)
plt.plot(index, rewards, color = 'b')

plt.xlabel("Episodes")
plt.ylabel("Reward", rotation = 90, labelpad = 10)
plt.title("Rewards over time")
plt.savefig("rewards_" + sys.argv[1] + ".png", dpi = 200)
#plt.show()
plt.close(fig)
