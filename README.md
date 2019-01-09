# Play on Words
This repo contains the following apps built on top of word/sentence embedding:

1. **Word Cross:**
   * A take on the traditional crossword puzzle. The ‘hints’ for each word are the word(s) that cross it. 
   * The probabilty of two words crossing is closely tied to the semantic similarity between the words.
   * Text Retrieval/Mining tools used: Spacy, NLTK
   * To start the game (from the console), navigate to word_cross/ and run: `python gen_wordmaze.py`
   
1. **Talk to Star Wars:**
   * A semantic search engine for the script of Star Wars episodes 1 through 6.
   * Lets you 'talk' to your favorite characters from Star Wars!
   * Tools used: TensorFlow, TensorFlow Hub, universal-sentence-encoder (from TF-Hub).
   * To start the game, navigate to talk_to_star_wars/ and run: `python talk_to_SW.py`
  
  
**_For more details (pdf and videos), visit:_** https://www.dropbox.com/sh/okdolpaodki3au0/AADA4vys8AgwLMPFHDGkM715a?dl=0 
