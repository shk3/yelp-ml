from __future__ import print_function
from __future__ import unicode_literals
import json, shutil, os, sys, time
from pprint import pprint
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.request import URLError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError

# Not Free http://text-processing.com/docs/sentiment.html
# Free https://www.mashape.com/loudelement/free-natural-language-processing-service#!documentation
PRINT_INTERVAL = 10
DST_FILE = 'data/yelp_academic_dataset_review.json'
BAK_FILE = DST_FILE + '.bak'
API_KEY = '0bsd4a9tHdvkvE5iOqkncKk3sigS5pD4'
API_URL = 'https://loudelement-free-natural-language-processing-service.p.mashape.com/nlp-text/'
def getTextFeatures(text):
    headers = {
        'Accept': 'application/json',
        'X-Mashape-Authorization': API_KEY,
    }
    query = {
        'text': text,
    }
    request = Request(API_URL + '?' + urlencode(query), None, headers)
    response = urlopen(request)
    resp = json.loads(response.read().decode('utf-8'))
    return (resp['sentiment-score'], resp['sentiment-text'])
    
# Backup the file
shutil.copy2(DST_FILE, BAK_FILE)
print('Finish backuping the json file.')
src = open(BAK_FILE, 'r+', encoding='utf8')
dst = open(DST_FILE, 'w+', encoding='utf8')

n = 0
skip_flag = False
results = []
for (i, row) in enumerate(src):
    # time.sleep(0.01)
    if i % PRINT_INTERVAL == 0 and not skip_flag:
        print('[%6d] ' % i, end='')
    myrow = json.loads(row)
    if not skip_flag:
        try:
            if 'text_polarity' not in myrow:
                text = myrow['text']
                if text != '':
                    score, label = getTextFeatures(text)
                else:
                    score = 0
                if score is None:
                    score = 0
                score = float(score)
                myrow['text_polarity'] = score
        except KeyboardInterrupt as e:
            skip_flag = True
            print ("Process is being terminated...")
        except:
            if i % PRINT_INTERVAL != 0:
                print('[%6d] ' % i, end='')
                # print('', myrow)
            print ("Unexpected error:", sys.exc_info()[0])
    print(json.dumps(myrow), file=dst)
    if i % PRINT_INTERVAL == 0 and not skip_flag:
        try:
            print('', myrow['text_polarity'])
        except:
            pass
    n = i
src.close()
dst.close()

print('Total: %d' % (n + 1))
