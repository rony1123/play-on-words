"""Parses movie scripts from Star Wars episodes 1 to 6 (downloaded from imsdb.com).
Six Parsing functions are written since there is no standard format followed throughout the series.
After parsing and extracting the character names and dialogues for each movie, the data is written to:
1. star_wars_movies.json: contains all the movie dialogues.
2. star_wars_characters.json: contains the names of all characters in Star Wars.

To run the script:
1. python movie_script_parser.py
"""

import os
import re
import json

cur = os.getcwd()
use_dir = '.\movie_scripts'
os.chdir(use_dir)

characters = set()
movie = {}


def parse_e01(filename):
    movie_name = os.path.splitext(os.path.basename(filename))[0]
    script = []
    chars = set()
    pattern = re.compile(r'^[A-Z\s\-0-9]+\s:', re.M)

    f = open(filename)
    # last_pos = f.tell()
    line = f.readline()
    character = ''
    dialogue = ''
    in_conv = False
    while line != '':
        l = line.strip()
        # print(l)

        matches = re.findall(pattern, l)
        if len(matches) > 0:
            if character != '' and dialogue != '':
                # print([character, dialogue])
                characters.add(character)
                script.append([character, dialogue])
            character = matches[0][:-1].strip()
            # print("character = " + character)
            dialogue = l.split(' : ')[1]
            # print(dialogue)
            in_conv = True
        else:
            if in_conv is True:
                if len(l) == 0:
                    in_conv = False
                else:
                    dialogue += (" " + l)

        # last_pos = f.tell()
        line = f.readline()

    movie[movie_name] = script


def parse_e02(filename):
    movie_name = os.path.splitext(os.path.basename(filename))[0]
    script = []
    with open(filename) as f:
        for line in f:
            str_gap = '<b>				'
            if line.startswith(str_gap) and len(line) > len(str_gap) and line[len(str_gap)] != ' ':
                character = line[3:]
                character = character.strip()

                if character.endswith('VOICE'):
                    character = character[:-len('VOICE')]
                    character = character.strip()

                if character.endswith("'S"):
                    character = character[:-len("'S")]
                    character = character.strip()

                if len(character) > 1:
                    # print(character)
                    characters.add(character)
                    full_dialogue = ''
                    for line2 in f:
                        dialogue = line2.strip()
                        if len(dialogue) < 1:
                            break
                        if dialogue.startswith('</b>'):
                            dialogue = dialogue[len('</b>'):]
                        dialogue = dialogue.strip()
                        full_dialogue += ' ' + dialogue
                    full_dialogue = full_dialogue.strip()
                    # print(full_dialogue)
                    comment = [character, full_dialogue]
                    # print(comment)
                    script.append(comment)
    movie[movie_name] = script


def parse_e03(filename):
    movie_name = os.path.splitext(os.path.basename(filename))[0]
    script = []
    pattern = re.compile(r'^[A-Z\s\-0-9]+:', re.M)
    with open(filename) as f:
        for line in f:
            ll = line.strip()
            if ll.startswith('<br>'):
                # clear all <br> tags from the beginning
                l = ll
                while l.startswith('<br>'):
                    l = l[len('<br>'):]
                # clear all <b> and </b> tags
                while l.startswith('<b>'):
                    l = l[len('<b>'):]
                while l.startswith('</b>'):
                    l = l[len('</b>'):]
                l = l.strip()
                if len(l) < 1:
                    continue

                matches = re.findall(pattern, l)
                if len(matches) > 0:
                    # print(matches)
                    character = matches[0][:-1]
                    # print(character)
                    # print(l)
                    if len(character) > 0:
                        characters.add(character)
                        t = l.split(':')
                        dialogue = t[1].strip()
                        for x in range(2, len(t)):
                            dialogue += (' ' + t[x])
                        for line2 in f:
                            x = line2.strip()
                            # clear all <br> tags from the beginning
                            while x.startswith('<br>'):
                                x = x[len('<br>'):]
                            # clear all <b> and </b> tags
                            while x.startswith('<b>'):
                                x = x[len('<b>'):]
                            while x.startswith('</b>'):
                                x = x[len('</b>'):]
                            x = x.strip()
                            if len(x) == 0:
                                break
                            else:
                                dialogue += ' ' + x
                        # print("dialogue = ", end='')
                        # print(dialogue)
                        comment = [character, dialogue]
                        script.append(comment)
    movie[movie_name] = script


def parse_e04(filename):
    movie_name = os.path.splitext(os.path.basename(filename))[0]
    script = []
    with open(filename) as f:
        for line in f:
            str_gap = '<b>                                     '
            if line.startswith(str_gap) and len(line) > len(str_gap) and line[len(str_gap)] != ' ':
                character = line[3:]
                character = character.strip()

                if character.endswith('VOICE'):
                    character = character[:-len('VOICE')]
                    character = character.strip()

                if character.endswith("'S"):
                    character = character[:-len("'S")]
                    character = character.strip()

                if len(character) > 1:
                    # print(character)
                    characters.add(character)
                    full_dialogue = ''
                    for line2 in f:
                        dialogue = line2.strip()
                        if len(dialogue) < 1:
                            break
                        if dialogue.startswith('</b>'):
                            dialogue = dialogue[len('</b>'):]
                        dialogue = dialogue.strip()
                        full_dialogue += ' ' + dialogue
                    full_dialogue = full_dialogue.strip()
                    # print(full_dialogue)
                    comment = [character, full_dialogue]
                    # print(comment)
                    script.append(comment)
    movie[movie_name] = script


def parse_e05(filename):
    movie_name = os.path.splitext(os.path.basename(filename))[0]
    script = []
    with open(filename) as f:
        for line in f:
            str_gap = '<b>				'
            if line.startswith(str_gap) and len(line) > len(str_gap) and line[len(str_gap)] != ' ' and line[len(str_gap)] != '\t':
                character = line[3:]
                character = character.strip()

                if character.endswith('VOICE'):
                    character = character[:-len('VOICE')]
                    character = character.strip()

                if character.endswith("'S"):
                    character = character[:-len("'S")]
                    character = character.strip()

                if len(character) > 1:
                    full_dialogue = ''
                    for line2 in f:
                        dialogue = line2.strip()
                        if len(dialogue) < 1:
                            break
                        if dialogue.startswith('</b>'):
                            dialogue = dialogue[len('</b>'):]
                        dialogue = dialogue.strip()
                        full_dialogue += ' ' + dialogue
                    full_dialogue = full_dialogue.strip()
                    if len(full_dialogue) > 0:
                        # print(full_dialogue)
                        characters.add(character)
                        comment = [character, full_dialogue]
                        # print(comment)
                        script.append(comment)
    movie[movie_name] = script


def parse_e06(filename):
    movie_name = os.path.splitext(os.path.basename(filename))[0]
    script = []
    with open(filename) as f:
        for line in f:
            str_gap = '<b>'
            if line.startswith(str_gap) and len(line) > len(str_gap) and line[len(str_gap)] != ' ' and line[len(str_gap)] != '\t':
                character = line[3:]
                character = character.strip()

                if character.endswith('VOICE'):
                    character = character[:-len('VOICE')]
                    character = character.strip()

                if character.endswith("'S"):
                    character = character[:-len("'S")]
                    character = character.strip()

                if len(character) > 1:
                    full_dialogue = ''
                    for line2 in f:
                        dialogue = line2.strip()
                        if len(dialogue) < 1:
                            break
                        while dialogue.startswith('</b>'):
                            dialogue = dialogue[len('</b>'):]
                        while dialogue.startswith('<b>'):
                            dialogue = dialogue[len('<b>'):]

                        dialogue = dialogue.strip()
                        if len(dialogue) > 0:
                            full_dialogue += ' ' + dialogue
                        else:
                            break

                    full_dialogue = full_dialogue.strip()
                    # print(full_dialogue)
                    if len(full_dialogue) > 0:
                        # print(full_dialogue)
                        characters.add(character)
                        comment = [character, full_dialogue]
                        # print(comment)
                        script.append(comment)

    movie[movie_name] = script


for fname in os.listdir('.'):
    print(fname)
    if 'E01' in fname:
        episode = 1
    elif 'E02' in fname:
        episode = 2
    elif 'E03' in fname:
        episode = 3
    elif 'E04' in fname:
        episode = 4
    elif 'E05' in fname:
        episode = 5
    elif 'E06' in fname:
        episode = 6

    #if episode in [1, 2, 3, 4, 5]:
    #    continue

    if episode == 1:
        parse_e01(fname)
    elif episode == 2:
        parse_e02(fname)
    elif episode == 3:
        parse_e03(fname)
    elif episode == 4:
        parse_e04(fname)
    elif episode == 5:
        parse_e05(fname)
    elif episode == 6:
        parse_e06(fname)


characters_list = list(characters)
characters_list.sort()

os.chdir(cur)

# write to json files
json_fname = 'star_wars_movies.json'
with open(json_fname, 'w') as json_f:
    json.dump(movie, json_f)

json_fname = 'star_wars_characters.json'
with open(json_fname, 'w') as json_f:
    json.dump(characters_list, json_f)

print(movie)
print(characters_list)
print(len(characters_list))
