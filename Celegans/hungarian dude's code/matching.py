from Network import Network
import networkx as nx

nw = Network()
nw.read_neuron_data()
G = nw.graph

print(len([muscle for muscle in nw.nodes if nw.neurons[muscle].is_muscle()]))
print(len([muscle for muscle in nw.nodes if not nw.neurons[muscle].is_muscle()]))
print(len(nw.nodes))

H = nx.Graph()

pos_nodes = []
neg_nodes = []

for node in nw.nodes:
    pos_node = node + "_P"
    neg_node = node + "_N"
    H.add_node(pos_node)
    H.add_node(neg_node)
    pos_nodes.append(pos_node)
    neg_nodes.append(neg_node)

for node in nw.nodes:
    pos_node = node + "_P"
    for neighbor in G.successors(node):
        neg_node = neighbor + "_N"
        H.add_edge(pos_node, neg_node)

#print(pos_nodes)
matching = nx.algorithms.bipartite.hopcroft_karp_matching(H, pos_nodes)
#print(matching)
print(len(matching))


matched_nodes = set()
for key,val in matching.items():
    splitted = key.split("_")
#    print(splitted)
    if splitted[1] == "N":
        real_node = splitted[0]
        matched_nodes.add(real_node)

#print(matched_nodes)
print(len([muscle for muscle in matched_nodes if nw.neurons[muscle].is_muscle()]))
print(len([muscle for muscle in matched_nodes if nw.neurons[muscle].is_sensor()]))
print(len([muscle for muscle in matched_nodes if not nw.neurons[muscle].is_muscle()]))
print(len(matched_nodes))
