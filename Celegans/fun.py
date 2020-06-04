import networkx as nx
import pandas as pd

df = pd.read_csv("NeuronConnect.csv")

print(df)

neurons = set().union(df['Neuron 2'].unique().tolist(),df['Neuron 1'].unique().tolist())

print(neurons)