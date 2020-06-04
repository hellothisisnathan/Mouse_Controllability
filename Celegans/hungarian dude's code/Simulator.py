from Network import Network
import networkx as nx
import time

class Simulator:
    TICKS = 50
    least_muscles_per_quarter = 12
    angle = 30

    def __init__(self):
        self.nw = Network()
        self.nw.read_neuron_data()
        self.curr_tick = 0

        # for creating figures
        self.reached_muscles = set()

    def check_state(self):
        return (not any((len(value.values) for key,value in self.nw.synapses.items()))
                and all((self.curr_tick - self.nw.neurons[node].last_fired
                         for node in self.nw.nodes)))

    def calc_movement_vector(self):
        muscles = self.nw.muscles
        muscle_groups = self.nw.muscle_groups
        mg_counter = self.nw.mg_firing_counter
        direction = mg_counter["LF"] - mg_counter["RF"]
        dist = (mg_counter["LB"] + mg_counter["RB"]) / 10
        return (direction * self.angle, dist)

    # TODO make it more pythonic ffs
    def perform_tick(self):
        G = self.nw.graph
        for node in self.nw.nodes:
            # calculating incoming value:
            # values arriving in the current tick are summed and added to the
            # stored_value of the neuron.
            neuron = self.nw.neurons[node]
            nodeSum = 0
            for neighbor in G.predecessors(node):
                synapse = self.nw.synapses[(neighbor, node)]
                if (len(synapse.values) > 0
                        and synapse.values[0][1] == self.curr_tick):
                    nodeSum += synapse.values[0][0]
                    synapse.next_values.popleft()

            if nodeSum > neuron.stimulus_threshold:
                neuron.values.append((nodeSum, self.curr_tick))
                neuron.stored_value += nodeSum

        for node in self.nw.nodes:
            neuron = self.nw.neurons[node]
            output = neuron.fire(self.curr_tick, self.reached_muscles)
            # calculating outgoing values
            # value of a node is split uniformly among outgoing edges
            if output > 0 and neuron.out_degree > 0:
                neuron.last_fired = self.curr_tick
                value = output / neuron.out_degree
                for neighbor in G.successors(node):
                    synapse = self.nw.synapses[(node, neighbor)]
                    newValue = (synapse.calc_new_value(value),
                                self.curr_tick + synapse.frequency)
                    synapse.next_values.append(newValue)

        self.nw.update(self.curr_tick, self.least_muscles_per_quarter)

    def main(self):
        done = False
        start = time.time()
        # for testing purposes:
      #  self.nw.set_input_data(["AVM", "ALML", "ALMR"],[980, 720, 1150])
      #  self.nw.set_muscle_group_thresholds({"LF":0,"RF":0,"LB":0,"RB":6})
        while (self.curr_tick < self.TICKS and not done):
            # for testing purposes:
            self.perform_tick()

            done = self.check_state();
            self.curr_tick += 1
      #  print("--- %s seconds ---" % (time.time() - start))
        return self.calc_movement_vector()

if __name__ == "__main__":
    sim = Simulator()
    sim.main()
