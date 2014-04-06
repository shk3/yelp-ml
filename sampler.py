from __future__ import print_function
from __future__ import unicode_literals
import os, random, sys
from pprint import pprint

if len(sys.argv) < 2:
    print('USAGE: %s <size of training set>' % sys.argv[0])
    print('This script only samples review dataset csv.')
    exit(2)

TRAINING_SIZE = int(sys.argv[1])

src = open('feature_review.csv', 'r+')
training = open('feature_review_training.csv', 'w+')
testing = open('feature_review_testing.csv', 'w+')

population = 0
for line in src:
    population += 1
population -= 1 # Ignore the headers
src.seek(0, os.SEEK_SET)
print('Total: %d' % population)

samples = random.sample(xrange(population), TRAINING_SIZE)
for i, line in enumerate(src):
    line_str = str(line).strip()
    if i % 1000 == 0:
        print('[%d]' % (i + 1))
    if i == 0:
        print(line_str, file=training)
        print(line_str, file=testing)
    else:
        if (i - 1) in samples:
            print(line_str, file=training)
        else:
            print(line_str, file=testing)

src.close()
training.close()
testing.close()
