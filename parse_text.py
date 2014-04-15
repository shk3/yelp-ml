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

if len(sys.argv) < 2:
    print('[USAGE] %s <CSV INPUT>' % sys.argv[0])
    exit()
else:
    IN_FILE = sys.argv[1]
    file_text = IN_FILE.split('.')
    file_text[-2] = file_text[-2] + '-bag-words'
    OUT_FILE1 = '.'.join(file_text)
    file_text[-2] = file_text[-2] + '-pos'
    OUT_FILE2 = '.'.join(file_text)

def encode_tagged(word_tag):
    return '##'.join(word_tag)

# Reading the review dataset
f = open('yelp_academic_dataset_review.json','r')

dicts = {}
dicts_tag = {}

reviews = []
for line in f:
    review_obj = json.loads(line)
    reviews.append(review_obj)
f.close()

# Read the source CSV
src_f = open(IN_FILE, 'r+', encoding='utf8')
src = csv.DictReader(src_f)

bow_list = []
bow_tag_list = []
# Tag in
for row in src:
    try:
        rid = int(row['review_id']) - 1
        # if rid > 100:
            # break
        text = reviews[rid]['text']
        bow_row = {
            'review_id': rid + 1
        }
        bow_tag_row = {
            'review_id': rid + 1
        }
        
        # Sentence Tokenize
        sents = nltk.tokenize.sent_tokenize(text)
        for sent in sents:
            # Word Tokenize
            words = nltk.tokenize.word_tokenize(sent)
            # PoS Tagging
            tagged_words = nltk.pos_tag(words)
            # Add in
            for word in words:
                word = word.lower()
                if word not in bow_row:
                    bow_row[word] = 0
                    if word not in dicts:
                        dicts[word] = [0, 0]
                    dicts[word][1] += 1
                bow_row[word] += 1
                dicts[word][0] += 1
            for tagged_word in tagged_words:
                tagged_word = list(tagged_word)
                tagged_word[0] = tagged_word[0].lower()
                word = encode_tagged(tagged_word)
                if word not in bow_tag_row:
                    bow_tag_row[word] = 0
                    if word not in dicts_tag:
                        dicts_tag[word] = [0, 0]
                    dicts_tag[word][1] += 1
                bow_tag_row[word] += 1
                dicts_tag[word][0] += 1
        bow_list.append(bow_row)
        bow_tag_list.append(bow_tag_row)
        print('Tokenized %d' % rid)
    except:
        logging.exception('Tokenizing Failed %d' % rid)
src_f.close()
# Print Stat
f1 = open('dict.dat', 'w+', encoding='utf8')
f2 = open('dict-tag.dat', 'w+', encoding='utf8')
print('word\tcount\toccurrence', file=f1)
print('word\ttag\tcount\toccurrence', file=f2)
for k, v in dicts.items():
    print('%s\t%d\t%d' % (k, v[0], v[1]), file=f1)
    
for k, v in dicts_tag.items():
    ks = k.split('##')
    print('%s\t%s\t%d\t%d' % (ks[0], ks[1], v[0], v[1]), file=f2)
f1.close()
f2.close()
    
# Output BoW CSV
headers = [
    'review_id',
]
headers.extend(dicts.keys())
with open(OUT_FILE1, 'w', encoding='utf8') as csvfile:
    csvwriter = csv.DictWriter(csvfile, 
        fieldnames=headers, 
        delimiter=',',
        quotechar='"', 
        quoting=csv.QUOTE_MINIMAL,
        lineterminator='\n')
    csvwriter.writeheader()
    
    for row in bow_list:
        try:
            for h in headers:
                if h not in row:
                    row[h] = 0
            csvwriter.writerow(row)
        except:
            logging.exception('')
# Output Tagged BoW CSV
headers = [
    'review_id',
]
headers.extend(dicts_tag.keys())
with open(OUT_FILE2, 'w', encoding='utf8') as csvfile:
    csvwriter = csv.DictWriter(csvfile, 
        fieldnames=headers, 
        delimiter=',',
        quotechar='"', 
        quoting=csv.QUOTE_MINIMAL,
        lineterminator='\n')
    csvwriter.writeheader()
    
    for row in bow_tag_list:
        try:
            for h in headers:
                if h not in row:
                    row[h] = 0
            csvwriter.writerow(row)
        except:
            logging.exception('')

