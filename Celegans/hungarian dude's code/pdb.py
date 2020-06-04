from Network import Network
import networkx as nx
import copy
import operator
from matplotlib import pyplot as plt

def bfs(s, G):
    H = copy.deepcopy(G)
    nodes = nx.nodes(G)
    H.add_node("ARTIF_INP")
    toDelete = set()
    layers = []
    actLayer = set()

    for node in nodes:
        if s.neurons[node].type.split("/")[0] == "se":
            actLayer.add(node);
            for neighbor in G.successors(node):
                if ("ARTIF_INP", neighbor) not in nx.edges(H):
                    H.add_edge("ARTIF_INP", neighbor,
                               number = G.get_edge_data(node, neighbor)["number"])
            for neighbor in G.predecessors(node):
                if (neighbor, "ARTIF_INP") not in nx.edges(H):
                    H.add_edge(neighbor, "ARTIF_INP",
                               number = G.get_edge_data(neighbor, node)["number"])
            toDelete.add(node)
    H.remove_nodes_from(toDelete)
    tree_H = nx.bfs_tree(H, source = "ARTIF_INP");
    layers.append(actLayer)

    nodesToProcess = set([node for node in nx.nodes(G) if node not in actLayer])
    # NOTE: nodes 'PVDR' AND  VC06 are not reachable
    nodesToProcess.difference_update(["PVDR", "VC06", "AINR", "AINL", "URAVL", "URAVR"])
    prevLayer = set(actLayer)
    while (len(nodesToProcess) > 0):
        actLayer = set((neighbor for node in prevLayer for neighbor in G.successors(node)
                        if neighbor in nodesToProcess))
        layers.append(actLayer)
        nodesToProcess.difference_update(actLayer)
        prevLayer = copy.deepcopy(actLayer)
        actLayer = set()

    return layers

nw = Network()
nw.read_neuron_data()

G = nw.graph
#print(G.has_edge("VB11", "MVL23"))
##exit()
W = copy.deepcopy(G)

#nodes = [node for node in nw.nodes if not nw.neurons[node].is_muscle() and node != "PVDR" and node != "VC06"]
#muscles = [node for node in nw.nodes if nw.neurons[node].is_muscle()]

spec_sensors = ["ALML", "AVM", "ALMR"]
sensors =[node for node in nw.nodes if  nw.neurons[node].is_sensor()]
oldsensors = copy.deepcopy(sensors)
oldsensors.remove("ALML")
oldsensors.remove("ALMR")
oldsensors.remove("AVM")
spec_motors = ["VB11", "VD13", "PDB", "VA12", "VD12"]
spec_muscles = ["MVL23", "MVR22", "MVL22", "MVR21", "MVL21", "MVR23", "MVR24"]

#asd = set()
#for mus in spec_muscles:
#    for nb in G.predecessors(mus):
#        asd.add(nb)
#
#print(asd)
#exit()

oldmuscles = [node for node in G.nodes if nw.neurons[node].is_muscle()]
muscles = copy.deepcopy(oldmuscles)
for mot in spec_muscles:
    oldmuscles.remove(mot)

W.remove_nodes_from(oldsensors)
W.remove_nodes_from(oldmuscles)
W.remove_nodes_from(["PVDR", "VC06", "AINL","AINR","URAVL","URAVR"])
for node in G.nodes:
    if node in W.nodes and node not in spec_motors and node not in spec_muscles and W.out_degree(node) == 0:
        W.remove_node(node)

print(len(W.nodes))

color_map = []
for node in W:
    if nw.neurons[node].type.split("/")[0] == 'se':
        color_map.append('blue')
    elif nw.neurons[node].type.split("/")[0] == 'in':
        color_map.append('orange')
    elif nw.neurons[node].type.split("/")[0] == 'mo':
        color_map.append('yellow')
    elif nw.neurons[node].type.split("/")[0] == 'mu':
        color_map.append('purple')

dpi = 300
plt.figure(figsize=(5,5), dpi = dpi)
posdict = {}
x = 10
y = 0
for mus in spec_muscles:
    posdict[mus] = (x, y)
    plt.text(x,y-0.02,s=mus, horizontalalignment='center', fontweight = 'bold', fontsize = 5)
    x += 20

y = 0.1
x = 30
for mot in spec_motors:
    posdict[mot] = (x, y)
    plt.text(x,y-0.02,s=mot, horizontalalignment='center', fontweight = 'bold', fontsize = 5)
    x += 20

y = 0.5
for layer in bfs(nw, W):
    x = 0
    incr = 150 / len(layer)
    print(incr)
    for node in layer:
        if node not in spec_motors and node not in spec_muscles:
            posdict[node] = (x, y)
            x += incr
    y -= 0.1

posdict["ALML"] = (25, 0.5)
posdict["AVM"] = (75, 0.5)
posdict["ALMR"] = (125, 0.5)
plt.text(25,0.5+0.01,s="ALML", horizontalalignment='center', fontweight = 'bold', fontsize = 5)
plt.text(75,0.5+0.01,s="AVM", horizontalalignment='center', fontweight = 'bold', fontsize = 5)
plt.text(125,0.5+0.01,s="ALMR", horizontalalignment='center', fontweight = 'bold', fontsize = 5)

posdict["AIML"] = (posdict["AIML"][0], 0.3)
posdict["AIMR"] = (posdict["AIMR"][0], 0.3)
posdict["URBL"] = (posdict["URBL"][0], 0.3)

layout = nx.spring_layout(W,iterations=10, pos = posdict)
nx.draw(W,node_color=color_map,pos=posdict,width=0.3,node_size=12, with_labels = False, arrowsize = 4)
plt.savefig("pdb_1.png", dpi = dpi, bbox_inches = 'tight')

#
#
#with open('paths_7.txt', 'a') as f:
#    for path in paths:
#        f.write(str(path) + "\n")
