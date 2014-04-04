from __future__ import print_function
from __future__ import unicode_literals
import json
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

print(getTextFeatures('This is an awfully great store.'))