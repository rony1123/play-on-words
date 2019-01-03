"""Stitches together all sub-graphs found in graph_assembly/*.json

To run the script:
1. python gen_wordgraph_merged.py
2. The output JSON file is 'merged_graph.json'.
"""

import os
import json

cwd = os.getcwd()
use_dir = 'graph_assembly'
os.chdir(use_dir)

g_temp = {}
graph_merged = {}
for root, dirs, files in os.walk('.'):
    for filename in files:
        with open(filename) as json_f:
            g_temp = json.load(json_f)
            for k in g_temp:
                if k in graph_merged:
                    print("Duplicate Found!")  # abort!
                    exit(0)
                else:
                    graph_merged[k] = g_temp[k]

os.chdir(cwd)

# write to file
with open('merged_graph.json', 'w') as json_f:
    json.dump(graph_merged, json_f)

