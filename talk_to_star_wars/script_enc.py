"""Reads all the movie dialogues from 'star_wars_movies.json' and uses the universal-sentence-encoder to create
512 dimensional encodings for each dialogue and stores them in one of six json files named:
E01_script_enc.json
E02_script_enc.json
...
E06_script_enc.json

To run the script:
1. python script_enc.py
"""

import tensorflow as tf
import tensorflow_hub as tfhub
import numpy as np
import json

with open('star_wars_movies.json') as json_f:
    movies_map = json.load(json_f)

module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
embed = tfhub.Module(module_url)

# Reduce logging output.
tf.logging.set_verbosity(tf.logging.ERROR)

print("START")
for mov in movies_map:
    print(movies_map[mov])
    dialogues = []
    for scr in movies_map[mov]:
        # print(scr)
        dialogues.append(scr[1])
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        script_embeddings = session.run(embed(dialogues))
        script_embeddings_list = np.array(script_embeddings).tolist()
        # print(len(script_embeddings_list))
        json_fname = mov[:4]+'script_enc.json'
        with open(json_fname, 'w') as json_f:
            json.dump(script_embeddings_list, json_f)

print("END")
