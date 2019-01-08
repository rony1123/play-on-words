"""Generates an embedding for each of the characters in star wars and stores them in 'star_wars_char_enc.json'

To run the script:
1. python character_enc.py
"""

import tensorflow as tf
import tensorflow_hub as tfhub
import numpy as np
import json

with open('star_wars_characters.json') as json_f:
    g_chars_list = json.load(json_f)

module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
embed = tfhub.Module(module_url)
char_map = {}

# Reduce logging output.
tf.logging.set_verbosity(tf.logging.ERROR)

with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    character_embeddings = session.run(embed(g_chars_list))

    for i, message_embedding in enumerate(np.array(character_embeddings).tolist()):
        char_map[g_chars_list[i]] = message_embedding

# write to json file
json_fname = 'star_wars_char_enc.json'
with open(json_fname, 'w') as json_f:
    json.dump(char_map, json_f)
