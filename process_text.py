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

if len(sys.argv) < 2:
    print('[USAGE] %s <CSV INPUT>' % sys.argv[0])
    exit()
else:
    IN_FILE = sys.argv[1]
    file_text = IN_FILE.split('.')
    file_text[-2] = file_text[-2] + '-bag-words-pos-occur'
    file_text[-1] = 'dat'
    OUT_FILE1 = '.'.join(file_text)

def decode_tagged(s):
    return s.split('##', 1)

classes = range(1,6)
SKIP_TAGS = []
    
# bow_list = pickle.load(open('bow_list.pickle', 'rb'))
bow_tag_list = pickle.load(open('bow_tag_list.pickle', 'rb'))
words = {}

# MLE for the features
counters = {}
for i in classes:   # init
    counter = {
        '#total': 0,
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
                counters[true_rating][k] = 0
            if v > 0:
                counters[true_rating][k] += 1
                counters[true_rating]['#total'] += 1

# Print out estimated results
dst = open(OUT_FILE1, 'w+', encoding='utf8')
words = sorted(list(words.keys()))
for word in words:
    print(word, end='\t', file=dst)
    for c in classes:
        if word not in counters[c]:
            counters[c][word] = 0
        print(counters[c][word] / counters[c]['#total'], end='\t', file=dst)
    print(file=dst)
dst.close()
