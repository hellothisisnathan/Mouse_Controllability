import random

neurons = {}

with open('neuron_list', 'r') as f:
    for line in f:
        words = line.strip().split(',')
        neurons[words[0]] = words[1].split('/')[0]

output = "Neuron,Type,Threshold,Input,Fatigue_limit,Stimulus_threshold\n"
inp_min = 100
inp_max = 200

# threshold: se: 6, mu: 2, rest: 20
# fatigue: mu: 2, rest: 0
# stimulus_threshold: 0,01
for key,value in neurons.items():
    typ = value.split('/')[0]
    threshold = 0
    inp = 0
    fatigue_limit = 0
    stimulus_threshold = 0.01

    if typ == "se":
        threshold = 6
        inp = float(random.randint(inp_min, inp_max))
    else:
        threshold = 20

    output += key + "," + typ + "," + str(threshold) + "," + str(inp) + "," \
              + str(fatigue_limit) + "," + str(stimulus_threshold) + "\n"

with open('sample_neur.conf', 'w') as f:
    f.write(output)
