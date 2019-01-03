"""Creates a Vocabulary of ~50K words for use in the program.
This is done by applying several constraints to a very large Vocabulary provided by Spacy (~1.1m).

The output is stored in two json files:
1. map_idx_word.json
2. map_word_idx.json
"""

import nltk
import spacy
import json

brown_set = set(s.strip().lower() for s in nltk.corpus.brown.words())
reuters_set = set(s.strip().lower() for s in nltk.corpus.reuters.words())
gutenberg_set = set(s.strip().lower() for s in nltk.corpus.gutenberg.words())
plain_words_set = set(s.strip().lower() for s in nltk.corpus.words.words())
stopwords_set = set(s.strip().lower() for s in nltk.corpus.stopwords.words())

nlp = spacy.load('en_vectors_web_lg')
voc = nlp.vocab


def word_constraints(s):
    filter_3s = False
    if len(s) <= 3 and voc[s].prob < -19.4:
        filter_3s = False
    else:
        filter_3s = True

    c_list = [s.isalpha(),
              len(s) > 2,
              len(s) < 20,
              # s not in stopwords_set,
              # s in plain_words_set or s in brown_set or s in gutenberg_set or s in reuters_set,
              s in plain_words_set or s in gutenberg_set,
              voc[s].prob > -19.6,
              filter_3s
              ]

    for c in c_list:
        if not c:
            return False
    return True


def start():
    words_list = []
    words_set = set()
    for s in voc.strings:
        ls = s.strip().lower()
        if word_constraints(ls):
            if ls not in words_set:
                words_set.add(ls)
                words_list.append(ls)

    words_list.sort()
    # print(len(words_list))

    map_word_idx = {}
    for idx in range(0, len(words_list)):
        map_word_idx[words_list[idx]] = idx

    with open('map_idx_word.json', 'w') as json_f:
        json.dump(words_list, json_f)

    with open('map_word_idx.json', 'w') as json_f:
        json.dump(map_word_idx, json_f)


start()
