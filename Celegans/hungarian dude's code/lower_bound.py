from Network import Network
import networkx as nx
import copy

nw = Network()
nw.read_neuron_data()

# Create network with all nodes/edges read in from C. Elegans connectivity data
starting_graph = nw.graph
few_sensors_graph = copy.deepcopy(starting_graph)

#nodes = [node for node in nw.nodes if not nw.neurons[node].is_muscle() and node != "PVDR" and node != "VC06"]
muscles = [node for node in nw.nodes if nw.neurons[node].is_muscle()]

sensors =[node for node in nw.nodes if  nw.neurons[node].is_sensor()] 
oldsensors = copy.deepcopy(sensors)
oldsensors.remove("ALML")
oldsensors.remove("ALMR")
oldsensors.remove("AVM")
nonsensors =[node for node in nw.nodes if not nw.neurons[node].is_sensor()] 
sensors = ["ALML", "ALMR", "AVM"]  # Sensors selected for the paper which yield z = 89
few_sensors_graph.remove_nodes_from(oldsensors)
few_sensors_graph.remove_nodes_from(["MVULVA","MANAL"])  # few_sensors_graph now  = no sensors except ALML/R, AVM, also remove MVULVA, MANAL (vulva and anal muscles); w/o this change lower bound = 91
base_graph = copy.deepcopy(few_sensors_graph)
base_graph.remove_nodes_from(muscles)
base_graph.remove_nodes_from(["PVDR", "VC06"])  # Excluded as in paper
"""(in addition to the neurons in the
pharyngeal system, CANL/R and VC06, which do not make connections with the rest of
the network, and the specialised muscles for the vulva and anus are excluded)"""

drivers = []  # List of strings; "DRIVER_1", "DRIVER_2", ...
for i in range(80):
    drivers.append("DRIVER_" + str(i))

base_graph.add_nodes_from(drivers)  # Add driver nodes to graph

normal_and_ALT_nodes_graph = nx.Graph()
node_ALT_list = []  # List of every actual node with _ALT appended
for node in base_graph.nodes:
    new_node = node + "_ALT"  # Ex. "ADAR_ALT"
    node_ALT_list.append(new_node)
tmp = copy.deepcopy(list(base_graph.nodes) + node_ALT_list)  # Combine normal nodes + _ALT nodes
normal_and_ALT_nodes_graph.add_nodes_from(tmp)  # At this point graph only has nodes, no edges

for edge in base_graph.edges:
    if edge not in normal_and_ALT_nodes_graph.edges:
        # type 1 edges
        # edge[0] is node1 -> edge[1] is node2
        normal_and_ALT_nodes_graph.add_edge(edge[0], edge[1] + "_ALT", weight = 1)  # Add connection between original node and new _ALT node
    else:
        # This case should never happen?
        pass

# At this point, normal_and_ALT_nodes_graph has same edges as base_graph but with all 2nd nodes going to the _ALT nodes
# what is happening

#type1 rest
j = 0
# Add edges from DRIVER nodes to all sensors_ALT w/ weight @ 1
for sensor in sensors:
    edge1 = ("DRIVER_" + str(j), sensor + "_ALT")  # Add edge from DRIVER_# to sensor_ALT
    normal_and_ALT_nodes_graph.add_edges_from([edge1], weight = 1)
    j += 1

# type 2 edges 
# Connect nodes and _ALT nodes w/ weight 0
for node in base_graph.nodes:
    edge = (node, node + "_ALT")
    if edge not in normal_and_ALT_nodes_graph.edges:
        normal_and_ALT_nodes_graph.add_edges_from([edge], weight = 0)

#type 3:
# Add 90 _ALT drivers to every node in the graph with sensors + muscles w/ edges weighted @ 0
for node in few_sensors_graph.nodes:
    for k in range(90):
        edge = (node, "DRIVER_" + str(k) + "_ALT")
        normal_and_ALT_nodes_graph.add_edges_from([edge], weight = 0)
        
print("matching algo started");
max_weight_matching_set = nx.max_weight_matching(normal_and_ALT_nodes_graph, True)  # Compute a maximum-weighted matching of G.
'''
A matching is a subset of edges in which no node occurs more than once.
The weight of a matching is the sum of the weights of its edges.
A maximal matching cannot add more edges and still be a matching.
The cardinality of a matching is the number of matched edges.
'''
weight_sum = 0
matching_nodes = set()
for edge in max_weight_matching_set:
    # If the first node in the edge is not a DRIVER, add it to matching_nodes
    if len(edge[0].split('_')) != 0 and edge[0].split('_')[0] != "DRIVER":
        matching_nodes.add(edge[0].split('_')[0])

    # If the second node in the edge is not a DRIVER, add it to matching_nodes
    if len(edge[1].split('_')) != 0 and edge[1].split('_')[0] != "DRIVER":
        matching_nodes.add(edge[1].split('_')[0])
    
    # Add weight to running weight sum. If it's a driver node, weight will be 0
    weight_sum += normal_and_ALT_nodes_graph.get_edge_data(edge[0], edge[1])['weight']

muscle_neighbours = set()

# Find all muscle neighbors for each matching node
for node in matching_nodes:
    for neighbor in few_sensors_graph.successors(node):
        if nw.neurons[neighbor].is_muscle():
            muscle_neighbours.add(node)
            break

# Reset the graph?? What the hell
# whatever man
# Add all muscle neighbors to matching nodes + all muscles - MVULVA and MANAL
normal_and_ALT_nodes_graph = nx.Graph()
normal_and_ALT_nodes_graph.add_nodes_from(muscle_neighbours)
normal_and_ALT_nodes_graph.add_nodes_from(muscles)
normal_and_ALT_nodes_graph.remove_nodes_from(["MVULVA", "MANAL"])

for node in muscle_neighbours:
    for neighbor in few_sensors_graph.successors(node):  # Find muscle neighbors of muscle neighbors to matching nodes?
        if nw.neurons[neighbor].is_muscle():
            edge = (node, neighbor)
            if edge not in normal_and_ALT_nodes_graph.edges:  # Basically, create new graph with *matching node* --> *muscle1* --> *muscle2*
                normal_and_ALT_nodes_graph.add_edges_from([edge])

# Basically maximum match muscles -> muscle_neighbors
matching = nx.algorithms.bipartite.hopcroft_karp_matching(normal_and_ALT_nodes_graph, muscle_neighbours)

print("lower bound: " + str(len(matching) / 2))


#print(len(normal_and_ALT_nodes_graph.edges))
#
#print(len(sensors))
#print(len(muscles))
#print(len(nonsensors))
