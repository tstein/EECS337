import json
import unicodedata
from urllib2 import urlopen

def getSentiment(text):
    return json.loads(urlopen("http://text-processing.com/api/sentiment/",
        data="text=%s" % text).read())

def allSentiments(results):   
    posTotal = 0
    negTotal = 0
    for s in results:
        text = unicodedata.normalize('NFKD', s.text).encode('ascii','ignore')
        
        sentDict = getSentiment(text)
        sent = sentDict['label']
        
        if sent == 'pos':
            posTotal += 1
           # posTweets.add(text)
        elif sent == 'neg':
            negTotal += 1
           # negTweets.add(text)
     
    return posTotal - negTotal
 
