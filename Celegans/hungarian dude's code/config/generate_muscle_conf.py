import random

muscles = []

with open('muscle_list', 'r') as f:
    muscles = [line.split(',')[0] for line in f]

output = "Muscle,Threshold,Fatigue_limit,Stimulus_threshold\n"

# threshold: se: 6, mu: 2, rest: 20
# fatigue: mu: 2, rest: 0
# stimulus_threshold: 0,01
for muscle in muscles:
    threshold = 2
    fatigue_limit = 2
    stimulus_threshold = 0.01

    output += muscle + "," +  str(threshold) + "," + str(fatigue_limit) + "," \
              + str(stimulus_threshold) + "\n"

with open('sample_muscle.conf', 'w') as f:
    f.write(output)
