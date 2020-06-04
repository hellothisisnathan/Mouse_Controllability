# simara 70
# 172386
# 1367689
from Network import Network
import networkx as nx
import copy

# Create network with all nodes/edges read in from C. Elegans connectivity data
nw = Network()
nw.read_neuron_data()

starting_graph = nw.graph
useless_graph = copy.deepcopy(starting_graph)

# base_graph is the graph containing entire neural network without extra sensors (nonsensors + ALML, ALMR, AVM sensors)
base_graph = copy.deepcopy(starting_graph)

#nodes = [node for node in nw.nodes if not nw.neurons[node].is_muscle() and node != "PVDR" and node != "VC06"]
muscles = [node for node in nw.nodes if nw.neurons[node].is_muscle() and node != "MVULVA" and node != "MANAL"]  # Exclude MVULVA and MANAL muscles (vulva and anal muscles)

sensors =[node for node in nw.nodes if  nw.neurons[node].is_sensor()] 
oldsensors = copy.deepcopy(sensors)
oldsensors.remove("ALML")
oldsensors.remove("ALMR")
oldsensors.remove("AVM")
nonsensors =[node for node in nw.nodes if not nw.neurons[node].is_sensor()] 
sensors = ["ALML", "ALMR", "AVM"] # Sensors selected for the paper which yield z = 89

base_graph.remove_nodes_from(oldsensors) # base_graph now  = nonsensors + the sensors ALML/R, AVM (such a weird way to do this, but ok man i didn't write this thing)

T = len(base_graph.nodes) - len(sensors)  # T = 297 = N + M + S - S
linking_graph = nx.DiGraph()
linking_graph.add_node("SOURCE")
linking_graph.add_node("TARGET")

# V_A
# Create 300 copies of each node (len(V_A) = (N + M) * (N + M))
for node in base_graph.nodes:  # Includes sensors and muscles as well
    # In this case, node serves as i = 1, 2, ... N + M
    for t in range(1, T + 1):
        act_node = node + "_A_" + str(t)  # Create ~300 copies of each node and add them to the linking graph as ADAL_A_1, ADAL_A_2, ... ADAL_A_300
        linking_graph.add_node(act_node)


VB = []  # 300 copies of each sensor: sensor_B_#
# V_B
for sensor in sensors:  # i.e. ALML, ALMR, AVM
    # In this case, sensor serves as i = 1, 2, ... S
    for t in range(1, (T + 1) - 1):
        act_node = sensor + "_B_" + str(t)  # Add 300 copies of each sensor and add them to the linking graph as ALML_B_0, ALML_B_1, ... ALML_B_299
        linking_graph.add_node(act_node)
        VB.append(act_node)


VC = []  # all muscles: muscle_C_
# V_C
# This is done correctly
for muscle in muscles:
    # In this case, muscle serves as i = 1, 2, ... M
    act_node = muscle + "_C"  # Just add _C on to every muscle and add it to the linking graph
    linking_graph.add_node(act_node)
    VC.append(act_node)

# E_A
# E_A is composed of edges between any node in the graph
for t in range(1, (T + 1) - 1):
    # Checking to see if the edge is in the actual graph effectively checks if a_ij != 0
    for edge in base_graph.edges:  # Makes it impossible for a_ij = 0
        act_edge = (edge[0] + "_A_" + str(t), edge[1] + "_A_" + str(t + 1))  # Create v^A_j,t -> v^A_i,t+1 by creating node1_t -> node2_t+1
        linking_graph.add_edges_from([act_edge])

# E_B
# E_B is composed of edges between sensors
for t in range(1, (T + 1) - 1):
    for sensor in sensors:
        act_edge = (sensor + "_B_" + str(t), sensor + "_A_" + str(t + 1))  # Create v^B_j,t -> v^A_i,t+1 by creating sensor1_t -> node2_t+1
        linking_graph.add_edges_from([act_edge])

# E_C
# E_C is composed of edges between muscles
for muscle in muscles:  # Makes it impossible for c_ij = 0
    act_edge = (muscle + "_A_" + str(T), muscle + "_C")  # Create v^A_j,t -> v^C_i by creating 
    linking_graph.add_edges_from([act_edge])

for node in VB:
    # We're adding a SOURCE node for every sensor, so basically we control every sensor
    linking_graph.add_edge("SOURCE", node)  # Add an edge between SOURCE and every copy of every sensor

for node in VC:
    # We're adding a TARGET node for every muscle, so we're checking the output at each muscle
    linking_graph.add_edge(node, "TARGET")  # Add an edge between every muscle and TARGET


#useless_graph.remove_nodes_from(["PVDR", "VC06"])

linking_size = nx.node_disjoint_paths(linking_graph, "SOURCE", "TARGET")  # Find all disjoint paths between SOURCE and TARGET
# Disjoint paths are paths that only share their first and last nodes
print("upper bound: " + str(len(list(linking_size))))


#print(len(aux.edges))
#
#print(len(sensors))
#print(len(muscles))
#print(len(nonsensors))
