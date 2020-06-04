import csv
import networkx as nx
import pandas as pd
from Neuron import Neuron
from Synapse import Synapse
import random
import copy

class Network:
    INPUT_NODE_NAMES = "./data/name_neurons.txt"
    MUSCLES = './data/name_neurons_muscles.txt'
    INPUT_EDGES = "./data/edge_list.csv" # Input neuron connectivity edge list from https://www.wormatlas.org/neuronalwiring.html#NeuronalconnectivityII
    NODE_TYPES = "./data/NeuronType.csv"
    ADD_MUSCLE_DATA = "./data/AddMuscleData.csv"

    NEUR_CONFIG_FILE = "./config/sample_neur.conf"
    MUSCLE_CONFIG_FILE = "./config/sample_muscle.conf"
#    NEUR_CONFIG_FILE = "./config/test.conf"
#    MUSCLE_CONFIG_FILE = "./config/test_muscle.conf"

    DEFAULT_VALUES_PATH = './config/defaults.csv'
    def __init__(self):
        # Input neuron connectivity edge list from https://www.wormatlas.org/neuronalwiring.html#NeuronalconnectivityII
        edge_list = pd.read_csv(self.INPUT_EDGES, sep = ";", header = None,
                                names = ["source", "target", "type", "number"])
        self.graph = nx.from_pandas_edgelist(edge_list, "source", "target",
                                             ["type", "number"], nx.DiGraph)

        self.nodes = nx.nodes(self.graph)  # List of nodes from neuronalconnectivity
        self.edges = nx.edges(self.graph) # List of edges from neuronalconnectivity
        self.muscles = []
        self.neurons = {node: Neuron(name = node,
                                     in_degree = self.graph.in_degree(node),
                                     out_degree = self.graph.out_degree(node))
                        for node in self.nodes}
        self.synapses = {edge: Synapse(source = edge[0],
                                       target = edge[1],
                                       type = self.graph.get_edge_data(edge[0], edge[1])
                                              ["type"],
                                       number = float(self.graph.get_edge_data(edge[0],
                                                                               edge[1])
                                                      ["number"]))
                         for edge in self.edges}

        self.default_values = {}
        self.set_default_values()

        self.muscle_groups = {}
        self.mg_firing_counter = {}

        self.mg_firing_counter["LF"] = 0
        self.mg_firing_counter["RF"] = 0
        self.mg_firing_counter["LB"] = 0
        self.mg_firing_counter["RB"] = 0
        self.muscle_groups["LF"] = []
        self.muscle_groups["RF"] = []
        self.muscle_groups["LB"] = []
        self.muscle_groups["RB"] = []


    def set_default_values(self):
        with open(self.DEFAULT_VALUES_PATH, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                defval = {}
                defval["threshold"] = float(row[1])
                defval["stored_value"] = float(row[2])
                defval["fatigue_limit"] = float(row[3])
                defval["stimulus_threshold"] = float(row[4])
                defval["fatigue_rate"] = float(row[5])
                self.default_values[row[0]] = defval

    def read_neuron_data(self):
        with open(self.INPUT_NODE_NAMES, 'r') as f:
            for line in f:
                if line.split()[0] in self.nodes:
                    self.neurons[line.split()[0]].type = line.split()[2]
                elif (line.split()[0][:-1] + "0" + line.split()[0][-1:]) in self.nodes:
                    self.neurons[(line.split()[0][:-1] + "0" + line.split()[0][-1:])].type\
                        = (line.split()[2])

        with open(self.MUSCLES, 'r') as f:
            for line in f:
                words = line.split();
                self.neurons[words[0]].type = words[2]

        with open(self.NODE_TYPES, 'r') as f:
            for line in f:
                words = line.split(';');
                self.neurons[words[0]].position = float(words[1])
                self.neurons[words[0]].region = words[2]

        with open(self.ADD_MUSCLE_DATA, 'r') as f:
            for line in f:
                words = line.split(';');
                self.neurons[words[1]].position = float(words[2])

        for name, neuron in self.neurons.items():
            neuron.threshold = self.default_values[neuron.type.split('/')[0]]["threshold"]
            neuron.stored_value = self.default_values[neuron.type.split('/')[0]]["stored_value"]
            neuron.fatigue_limit = self.default_values[neuron.type.split('/')[0]]["fatigue_limit"]
            neuron.stimulus_threshold = self.default_values[neuron.type.split('/')[0]]["stimulus_threshold"]
            neuron.fatigue_rate = self.default_values[neuron.type.split('/')[0]]["fatigue_rate"]
            #print(name + "  " + neuron.type + " " + str(neuron.threshold))

        #setting configuration
        with open(self.NEUR_CONFIG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                self.neurons[row[0]].threshold = float(row[2])
                self.neurons[row[0]].fatigue_limit = float(row[4])
                self.neurons[row[0]].stimulus_threshold = float(row[5])
                if row[1] == "se":
                    self.neurons[row[0]].last_fired = 0
                    # setting input values
                    self.neurons[row[0]].stored_value = float(row[3])

        with open(self.MUSCLE_CONFIG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                self.neurons[row[0]].threshold = float(row[1])
                self.neurons[row[0]].fatigue_limit = float(row[2])
                self.neurons[row[0]].stimulus_threshold = float(row[3])

        self.muscles = [node for node in self.nodes if self.neurons[node].is_muscle()]
        self.muscles.remove("MANAL")
        self.muscles.remove("MVULVA")
        self.set_muscle_groups()

    # for testing purposes
    def set_input_data(self, neurons, values):
        for i in range(len(neurons)):
            self.neurons[neurons[i]].stored_value = values[i]
            self.neurons[neurons[i]].last_fired = 0

    def set_muscle_groups(self):
        neurons = self.neurons
        for muscle in self.muscles:
            side = muscle[2]
            horizontal = "F" #front
            if neurons[muscle].position > 0.5:
                horizontal = "B" #back
            self.muscle_groups[side + horizontal].append(muscle)
        for key,value in self.muscle_groups.items():
            self.muscle_groups[key] = sorted(value)

    def set_muscle_thresholds(self, thresholds):
        for key,value in thresholds.items():
            self.neurons[key].threshold = value

    def set_muscle_group_thresholds(self, thresholds):
        for key,value in thresholds.items():
            for muscle in self.muscle_groups[key]:
                self.neurons[muscle].threshold = value

    def update(self, curr_tick, least_muscles_per_quarter):
        for name, synapse in self.synapses.items():
            synapse.values = copy.deepcopy(synapse.next_values)

        for muscle in self.muscles:
            cell = self.neurons[muscle]
            cell.all_values.append(cell.stored_value)
            if cell.stored_value > 0:
                if cell.first_reached == -1:
                    cell.first_reached = curr_tick
                cell.reached_values.append(cell.stored_value)
            if cell.last_fired == curr_tick:
                cell.fire_values.append(cell.stored_value)

        act_counter = {}
        act_counter["LF"] = 0
        act_counter["RF"] = 0
        act_counter["LB"] = 0
        act_counter["RB"] = 0
        for key,value in self.muscle_groups.items():
            act_counter[key] = len([muscle for muscle in value if self.neurons[muscle].last_fired == curr_tick])
        for key,val in act_counter.items():
            if key == "RF":
                if act_counter[key] > least_muscles_per_quarter \
                and act_counter["LF"] < least_muscles_per_quarter:
                    self.mg_firing_counter[key] += 1
            elif key == "LF":
                if act_counter[key] > least_muscles_per_quarter \
                and act_counter["RF"] < least_muscles_per_quarter:
                    self.mg_firing_counter[key] += 1
            elif key == "RB":
                if act_counter[key] > least_muscles_per_quarter \
                and act_counter["LB"] < least_muscles_per_quarter:
                    self.mg_firing_counter[key] += 1
            elif key == "LB":
                if act_counter[key] > least_muscles_per_quarter \
                and act_counter["RB"] < least_muscles_per_quarter:
                    self.mg_firing_counter[key] += 1
