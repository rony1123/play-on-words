"""A simple check to make sure 'merged_graph.json' is not corrupted. 
Also calculates, the size of the Vocabulary, the number of 'dead ends' and the average degree of each node
in the word graph.
"""

import json

graph_file = 'merged_graph.json'

with open('merged_graph.json') as json_f:
    g_temp = json.load(json_f)

with open('map_idx_word.json') as json_f:
    words_list = json.load(json_f)

dud_counter = 0
neighbor_counter = 0
for k in g_temp:
    print(words_list[int(k)], end=": ")
    neighbor_counter += len(g_temp[k])
    if len(g_temp[k]) == 0:
        dud_counter += 1
    for w in g_temp[k]:
        print(words_list[w], end=', ')
    print("")


print(len(g_temp))
print(dud_counter)
print(neighbor_counter/len(g_temp))
