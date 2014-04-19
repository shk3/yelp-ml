'''
Created on Apr 14, 2014

@author: Amod Samant
@updated: George Hongkai Sun
'''
##### THIS SCRIPT ONLY VALID FOR TRAINING #####
from __future__ import print_function
from __future__ import unicode_literals
import json
from pprint import pprint
import re
from string import punctuation
import csv
import sys
import logging
import pickle
import os.path

if len(sys.argv) < 4:
    print('[USAGE] %s <CSV INPUT> <TOKENIZATION PICKLE> <TYPE>' % sys.argv[0])
    exit()
else:
    IN_FILE = sys.argv[1]
    TOKEN_FILE = sys.argv[2]
    OUT_NAME = os.path.splitext(IN_FILE)[0] + '-bag-words-' + sys.argv[3]

def decode_tagged(s):
    r = s.split('##', 1)
    if len(r) < 2:
        r.append(None)
    return r

classes = range(1,6)
SKIP_TAGS = []
    
bow_tag_list = pickle.load(open(TOKEN_FILE, 'rb'))
words = {}

# MLE for the features
counters = {}
for i in classes:   # init
    counter = {
        '#total': [0, 0],
    }
    counters[i] = counter

src = csv.DictReader(open(IN_FILE, 'r+', encoding='utf8'))
for i, row in enumerate(src):
    if i > 300:
        break
    true_rating = int(row['true_stars'])
    
    for k, v in bow_tag_list[i].items():
        if k == 'review_id':
            continue
        w, t = decode_tagged(k)
        if t not in SKIP_TAGS:
            words[k] = None
            if k not in counters[true_rating]:
                counters[true_rating][k] = [0, 0]
            if v > 0:
                counters[true_rating][k][0] += 1
                counters[true_rating][k][1] += v
                counters[true_rating]['#total'][0] += 1
                counters[true_rating]['#total'][1] += v

# Print out estimated results
words = sorted(list(words.keys()))
    # occur
dst = open(OUT_NAME + '-occur.dat', 'w+', encoding='utf8')
for word in words:
    print(word, end='\t', file=dst)
    for c in classes:
        if word not in counters[c]:
            counters[c][word] = [0, 0]
        print(counters[c][word][0] / counters[c]['#total'][0], end='\t', file=dst)
    print(file=dst)
dst.close()
    # count
dst = open(OUT_NAME + '-count.dat', 'w+', encoding='utf8')
for word in words:
    print(word, end='\t', file=dst)
    for c in classes:
        if word not in counters[c]:
            counters[c][word] = [0, 0]
        print(counters[c][word][1] / counters[c]['#total'][1], end='\t', file=dst)
    print(file=dst)
dst.close()

# Dump as pickle for further Python use
pickle.dump(counters, open(OUT_NAME + '.pickle', 'wb'))