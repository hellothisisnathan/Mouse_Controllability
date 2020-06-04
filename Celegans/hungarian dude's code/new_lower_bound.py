from Network import Network
import networkx as nx
import copy
import cana

nw = Network()
nw.read_neuron_data()

# Create network with all nodes/edges read in from C. Elegans connectivity data
starting_graph = nw.graph
few_sensors_graph = copy.deepcopy(starting_graph)

muscles = [node for node in nw.nodes if nw.neurons[node].is_muscle() and node != "MVULVA" and node != "MANAL"]

sensors =[node for node in nw.nodes if  nw.neurons[node].is_sensor()] 
oldsensors = copy.deepcopy(sensors)
oldsensors.remove("ALML")
oldsensors.remove("ALMR")
oldsensors.remove("AVM")
nonsensors =[node for node in nw.nodes if not nw.neurons[node].is_sensor()] 
sensors = ["ALML", "ALMR", "AVM"]  # Sensors selected for the paper which yield z = 89
few_sensors_graph.remove_nodes_from(oldsensors)  # few_sensors_graph now  = no sensors except ALML/R, AVM, also remove MVULVA, MANAL (vulva and anal muscles); w/o this change lower bound = 91
base_graph = copy.deepcopy(few_sensors_graph)
#base_graph.remove_nodes_from(muscles)
base_graph.remove_nodes_from(["PVDR", "VC06"])  # Excluded as in paper
"""(in addition to the neurons in the
pharyngeal system, CANL/R and VC06, which do not make connections with the rest of
the network, and the specialised muscles for the vulva and anus are excluded)"""

'''
V_S = nodes that recieve external signals
V_M = output nodes (muscles)
V_D = nodes that connect to output (V_M)
'''

V_S = []
for sensor in sensors:
    for neighbor in base_graph.neighbors(sensor):
        if neighbor not in sensors:
            V_S.append(neighbor)

V_M = muscles

V_D = []
for muscle in muscles:
    for neighbor in base_graph.predecessors(muscle):
        if neighbor not in muscles:
            V_D.append(neighbor)