import json
import unicodedata
from urllib2 import urlopen

def getSentiment(text):
    return json.loads(urlopen("http://text-processing.com/api/sentiment/",
        data="text=%s" % text).read())

def allSentiments(results):   
    allTweets = results' '.join(results)
    sentVal = 0
    text = unicodedata.normalize('NFKD', allTweets).encode('ascii','ignore')
    
    sentDict = getSentiment(text)
    sent = sentDict['label']
    
    if sent == 'pos':
        sentVal = 1
       # posTweets.add(text)
    elif sent == 'neg':
        sentVal = -1
       # negTweets.add(text)
     
    return sentVal
 
