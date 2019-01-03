"""Generates a 'word graph' in batches.

This script allows the user to generate a JSON file that contains a graph/sub-graph.
The nodes covered by running the script is specified by the global variable, batch_nos = [x, y].
i.e generate the graph for nodes x to y (x <= y) inclusive.

The script is meant to be run as multiple processes preferably on multiple machines. The JSON files generated,
can later be stitched together.

To run the script:
1. Change the value of batch_nos = [x, y] to the preferred range.
2. Then, run:
    python gen_wordgraph_batch__.py
3. Save the output JSON file.

"""

import nltk
import spacy
import json
from datetime import datetime

brown_set = set(nltk.corpus.brown.words())
reuters_set = set(nltk.corpus.reuters.words())
gutenberg_set = set(nltk.corpus.gutenberg.words())
plain_words_set = set(nltk.corpus.words.words())

stopwords_set = set(nltk.corpus.stopwords.words())

nlp = spacy.load('en_vectors_web_lg')
voc = nlp.vocab

batch_nos = [0, 5000]  # change start and end node for which edges will be sorted (run as parallel processes)
length_limit = 75  # maximum adjacent edges saved.


def cross_check(w1, w2):
    """Checks if two words share any character.
    
    :param w1: word 1 (string).
    :param w2: word 2 (string).
    :return: True if a character is shared, False otherwise.
    """
    for c in w1:
        if c in w2:
            return True
    return False


def start():
    """For each node, computes length_limit=75 closest neighbors.
    Stores the result in a JSON file as an adjacency list.
    
    :return: None
    """
    words_list = []
    with open("map_idx_word.json") as json_f:
        words_list = json.load(json_f)
    # print(len(words_list))

    words_in_use = {}
    counter = 0
    for i in range(batch_nos[0], batch_nos[1]):
        w1 = words_list[i]
        words_in_use[i] = []
        # print(str(i)+": ", end='')
        for j in range(0, len(words_list)):
            w2 = words_list[j]
            if voc[w2].similarity(voc[w1]) <= 0.92 and voc[w2].similarity(voc[w1]) >= 0.36 and (w2 not in w1) and (
                        w1 not in w2) and cross_check(w2, w1):
                words_in_use[i].append(j)

        words_in_use[i].sort(key=lambda x: voc[words_list[x]].similarity(voc[w1]), reverse=True)
        words_in_use[i] = words_in_use[i][:length_limit]

        counter += 1
        if counter % 50 == 0:
            print(counter, end=' - ')
            print(datetime.now().time())

        if counter % 200 == 0:  # take a snapshot every 200 words
            json_fname = 'graph_' + str(batch_nos[0]) + '_' + str(batch_nos[0]+len(words_in_use)) + ".json"
            with open(json_fname, 'w') as json_f:
                json.dump(words_in_use, json_f)

    json_fname = 'graph_' + str(batch_nos[0]) + '_' + str(batch_nos[1]) + ".json"
    with open(json_fname, 'w') as json_f:
        json.dump(words_in_use, json_f)


start()
