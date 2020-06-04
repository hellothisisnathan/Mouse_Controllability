from collections import deque
import csv

class Neuron:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.type = kwargs.get("type", "")
        self.position = kwargs.get("position", 0.0)
        self.region = kwargs.get("region", "")
        self.threshold = 0
        self.values = deque()
        self.in_degree = kwargs.get("in_degree", 0)
        self.out_degree = kwargs.get("out_degree", 0)
        self.stored_value = 0.0
        self.last_fired = -1
        self.firing_counter = 0
        self.stimulus_threshold = pow(10, -2)

        # currently relevant for muscles only
        self.fatigue_limit = 2
        self.fatigue_rate = 1

        # for creating figures
        self.first_fired = -1
        self.first_reached = -1
        self.fire_values = []
        self.reached_values = []
        self.all_values = []
        #self.value_sum = 0
        #self.value_fire_sum = 0
        #self.reached_num = 0
        #self.fired_num = 0

    def is_muscle(self):
        return self.type == "mu"

    def is_sensor(self):
        return self.type.split("/")[0] == "se"

    def fire(self, curr_tick, reached_muscles):
        output = 0
        if self.type.split('/')[0] == "se" and self.stored_value >= self.threshold:
            output = self.stored_value
            self.stored_value = 0
            self.values.clear()
        elif self.type == "mu" and self.stored_value >= self.threshold:
            if self.first_fired == -1:
                self.first_fired = curr_tick
            #reached_muscles.add(self.name)
            if self.firing_counter == self.fatigue_limit:
                self.stored_value = 0
                self.values.clear()
                self.firing_counter = 0
            else:
                self.last_fired = curr_tick
                self.stored_value *= self.fatigue_rate
                self.firing_counter += 1
        elif self.type != "mu" and self.stored_value >= self.threshold:
            output = self.stored_value
            self.stored_value = 0
            self.values.clear()
            self.firing_counter += 1
        else:
            self.firing_counter = 0

        return output

    def trace(self):
        print("Neuron name, type: " + self.name + ", " + self.type)
        print("\tPosition, region: " + str(self.position) + ", " + self.region)
        print("\tStored value: " + str(self.stored_value))
        print("\tFiring counter: " + str(self.firing_counter))
