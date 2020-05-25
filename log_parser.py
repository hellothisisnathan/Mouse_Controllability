"""
Usage:
# Create CSV file from log data:
python log_parser.py -i LOG_FILE_NAME.txt -o OUTPUT_FILE_NAME.csv
"""

import re
import csv
import argparse
import os
from xml.dom import minidom
import urllib.request
from collections import Counter
import pandas as pd
from pandas import ExcelWriter

log_pattern = r"control nodes:\s*\((?P<control_nodes>.+)\)\s*terminal nodes:\s*\((?P<terminal_nodes>.+)\)\s*rank:\s*(?P<rank>.+)"
# test = ["control nodes: (72,226) terminal nodes: (210,470) rank: 0", "--", "control nodes: (72,226) terminal nodes: (210,470) rank: 0"]
# file_name = "log_2_2_CentralsRemoved.txt"

control_nodes = []  # List of control nodes
terminal_nodes = []  # List of terminal ndoes
rank = []  # List of ranks
node_names = {}  # List of names for all nodes used
count = None  # Count data for controllable nodes

def read_log_file(log):
    with open(log) as f:
        for line in f:
            if len(line) < 4:
                continue
            m = re.match(log_pattern, line)
            control_nodes.append(list(int(s) for s in m.groupdict()['control_nodes'].split(',')))  # Add pair of control nodes as list to the control_nodes list
            terminal_nodes.append(list(int(s) for s in m.groupdict()['terminal_nodes'].split(',')))  # Add pair of terminal nodes as list to the terminal_nodes list
            rank.append(int(m.groupdict()['rank']))  # Add rank to list

    # Get names of nodes from their ids and store in a dict for lookup later if needed
    unique_nodes = set().union(*terminal_nodes, *control_nodes)  # Don't want to repeat nodes so make a set from the terminal and control nodes
    for node in unique_nodes:
        atlas_url = "http://api.brain-map.org/api/v2/data/Structure/{}.xml".format(node)
        dom = minidom.parse(urllib.request.urlopen(atlas_url))
        node_names[node] = dom.getElementsByTagName('name')[0].firstChild.nodeValue

    
def to_csv(output):

    # Write CSV
    """
    Control Node 1  | Control Node 2  | ... | Terminal Node 1 | Terminal Node 2 | ... |  Rank  | Control Node 1 Name  | Control Node 2 Name  | ... | Terminal Node 1 Name | Terminal Node 2 Name | ...
        cnode1      |      cnode2     | ... |    tnode1       |   tnode2        | ... |  rank1 |     cnode1 name      |     cnode1 name      | ... |     tnode1 name      |     tnode1 name      | ...
        cnode3      |      cnode4     | ... |    tnode3       |   tnode4        | ... |  rank2 |     cnode3 name      |     cnode4 name      | ... |     tnode3 name      |     tnode4 name      | ...
        cnode5      |      cnode6     | ... |    tnode5       |   tnode6        | ... |  rank3 |     cnode5 name      |     cnode6 name      | ... |     tnode5 name      |     tnode6 name      | ...
        ...         |      ...        | ... |    ...          |   ...           | ... |   ...  |         ...          |         ...          | ... |         ...          |         ...          | ...
    """
    # Compose title row as above
    cnode_title = ["Control Node {}".format(x) for x in range(len(control_nodes[0]))]
    tnode_title = ["Terminal Node {}".format(x) for x in range(len(terminal_nodes[0]))]
    rank_title = ["Rank"]
    cnode_name_title = ["Control Node {} Name".format(x) for x in range(len(control_nodes[0]))]
    tnode_name_title = ["Terminal Node {} Name".format(x) for x in range(len(terminal_nodes[0]))]
    header_row = cnode_title + tnode_title + rank_title + cnode_name_title + tnode_name_title

    with open(output, 'w') as f:
        wtr = csv.writer(f, delimiter = ',', lineterminator = '\n')
        wtr.writerow(header_row)  # Write header row once
        for (cn, tn, r) in (zip(control_nodes, terminal_nodes, rank)):  # cn = control nodes, tn = terminal nodes, r = rank
            # Get node values for row
            node_row_values = [*cn, *tn]
            names = []  # List for node names
            # Build list of node names for remainder of row
            for node in node_row_values:
                names.append(node_names[node])
            wtr.writerow([*node_row_values, r, *names])

def count_data(output):
    controllable_nodes = []
    for cnode_set, r in zip(control_nodes, rank):
        if r >= 2:  # Find controllable sets
            controllable_nodes.extend(cnode_set)
    count = Counter(controllable_nodes)
    print(count)
    header_row = ["Control Node", "Name", "Count"]
    with open(output, 'w') as f:
        wtr = csv.writer(f, delimiter = ',', lineterminator = '\n')
        wtr.writerow(header_row)  # Write header row once
        for key, value in count.items():
            wtr.writerow([key, node_names[key], value])
        


def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Simulation Log file to CSV converter")
    parser.add_argument("-i",
                        "--inputDir",
                        help="Path to the folder where the input log files are stored",
                        type=str)
    parser.add_argument("-o",
                        "--outputFile",
                        help="Name of output .csv file (including path)", type=str)
    args = parser.parse_args()

    if(args.inputDir is None):
        args.inputDir = os.getcwd()
    if(args.outputFile is None):
        args.outputFile = args.inputDir + "/nodes.csv"

    assert(os.path.exists(args.inputDir))

    # Collect data and write to csv
    read_log_file(args.inputDir)
    to_csv(args.outputFile)
    print('CSV file created!! :)')

    # Count controlling nodes
    count_data_file = args.outputFile[:-4] + "_count_data.csv"
    count_data(count_data_file)
    print('Count data file added!')

if __name__ == "__main__":
    main()