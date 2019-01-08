"""This is the main file that contains the 'game loop'. 
The program takes user queries and converts them to sentence embeddings.
A linear search (that should be parallelized in a future version) takes the dot product
between the query and each of the movie dialogues to compute the cosine 'distance'.

The top 42 results are stored and returned to the user in decreasing order of 'distance'.

To run the script:
1. python talk_to_SW.py
"""

import tensorflow as tf
import tensorflow_hub as tfhub
import numpy as np
import json
import random
import os
import colorama
colorama.init(autoreset=True)

scripts_enc = []
# load all the encoded scripts:
for x in range(1, 7):
    json_fname = 'E0'+str(x)+'_script_enc.json'
    # print(json_fname)
    with open(json_fname) as json_f:
        enc_list = json.load(json_f)
        scripts_enc.append(enc_list)

json_fname = 'star_wars_movies.json'
with open(json_fname) as json_f:
    movies = json.load(json_f)

module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
embed = tfhub.Module(module_url)

# Reduce logging output.
tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def print_help_msg():
    print("*"*100)
    print("COMMANDS: ")
    print("?  -- Show this help message")
    print("q  -- Quit the program")
    print("<any phrase/sentence>  -- Search through the Star Wars scripts. (returns 42 results)")
    print("n  -- Cycle through the search results")
    print("*"*100)


def process_query(query):
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        message_embeddings = session.run(embed(query))
        embedding = np.array(message_embeddings).tolist()
        q_embedding = list(embedding[0])

    max_matches = 42
    matches = []
    loc = []
    for x in range(0, 6):
        counter = 0
        min_val = -100
        for scr in scripts_enc[x]:
            corr = np.inner(q_embedding, scr)
            if len(matches) > 0:
                min_val = min(matches)
            if len(matches) < max_matches:
                matches.append(corr)
                loc.append([x, counter, corr])
            elif corr > min_val:
                idx = matches.index(min_val)
                del matches[idx]
                del loc[idx]
                matches.append(corr)
                loc.append([x, counter, corr])

            counter += 1

    loc.sort(key=lambda k: k[2], reverse=True)
    return loc


def show_result(result, position):
    movie_names = list(movies.keys())
    movie_names.sort()
    mov, scr, corr = result
    mov_name = str(movie_names[mov])
    print("")
    print(position+1, end="/42    ")
    print("["+mov_name+"]")
    print("----------------------------------------------------------------------------------------------------")

    pre = 2
    post = 3
    span = [scr-pre, scr+post+1]

    for scr_ in range(span[0], span[1]):
        if scr_ < len(movies[movie_names[mov]]):
            character = movies[movie_names[mov]][scr_][0]
            dialogue = movies[movie_names[mov]][scr_][1]
            if scr_ == scr:
                print(colorama.Fore.GREEN + character + ": " + dialogue)
            else:
                print(character + ": " + dialogue)
    print("----------------------------------------------------------------------------------------------------")


def start():
    random.seed()
    print("\nUse the Force! (Type ? for help, q to quit)\n")
    current_results = []
    current_pos = 0
    new_search = False
    while True:
        query = input('> ')
        query = query.strip().lower()
        if len(query) == 0:
            continue
        if query == 'q':
            exit(0)
        elif query == '?':
            print_help_msg()
        elif query == 'n':
            if new_search is True:
                current_pos += 1
                if current_pos >= 42:
                    current_pos = 0
                show_result(current_results[current_pos], current_pos)
        else:
            new_search = True
            current_pos = 0
            current_results = process_query([query])
            show_result(current_results[current_pos], current_pos)


start()
