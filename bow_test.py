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
import nltk
import sys
import logging
import pickle
import os.path

SMALL_VALUE = 1e-300

if len(sys.argv) < 4:
    print('[USAGE] %s <TEST-SET CSV> <TRAINED PICKLE> <TYPE>' % sys.argv[0])
    exit()
else:
    IN_FILE = sys.argv[1]
    PICKLE_FILE = sys.argv[2]
    OUT_NAME = os.path.splitext(IN_FILE)[0] + '-bag-words-' + sys.argv[3]

def encode_tagged(word_tag):
    return '##'.join(word_tag)

classes = range(1,6)
    
counters = pickle.load(open(PICKLE_FILE, 'rb'))

# Reading the review dataset
f = open('yelp_academic_dataset_review.json','r')
reviews = []
for line in f:
    review_obj = json.loads(line)
    reviews.append(review_obj)
f.close()

src = csv.DictReader(open(IN_FILE, 'r+', encoding='utf8'))
dst = open(OUT_NAME + '-occur.dat', 'w+', encoding='utf8')
cc = 0
nc = 0
for i, row in enumerate(src):
    if i > 300:
        break
    try:
        rid = int(row['review_id'])
        text = reviews[rid]['text']
        
        occur = {}
        count = {}
        # Sentence Tokenize
        sents = nltk.tokenize.sent_tokenize(text)
        for sent in sents:
            # Word Tokenize
            words = nltk.tokenize.word_tokenize(sent)
            # PoS Tagging
            tagged_words = nltk.pos_tag(words)
            # Add in
            if sys.argv[3] != 'pos':
                for word in words:
                    word = word.lower()
                    occur[word] = 1
                    count[word] = count.get(word, 0) + 1
            else:
                for tagged_word in tagged_words:
                    tagged_word = list(tagged_word)
                    tagged_word[0] = tagged_word[0].lower()
                    word = encode_tagged(tagged_word)
                    occur[word] = 1
                    count[word] = count.get(word, 0) + 1
        
        # Calculate Likelihood
        print(rid, end='\t', file=dst)
        bc = 0
        pc = SMALL_VALUE
        for c in classes:
            p = 1
            for word in occur.keys():
                if word not in counters[c]:
                    continue
                p *= counters[c][word][0] / counters[c]['#total'][0]
            p += SMALL_VALUE
            if p > pc:
                bc = c
            print(p, end='\t', file=dst)
        print(file=dst)
        # Compare correctness if only use this...
        flag = ''
        if int(row['true_stars']) == int(bc):
            flag = 'T'
            cc += 1
        nc += 1
        print('Tokenized %d %s' % (rid, flag))
    except:
        logging.exception('Tokenizing Failed %d' % rid)
dst.close()
print('Correctness: %.2f%%' % (cc / nc * 100))