import json
import unicodedata
from urllib2 import urlopen

def getSentiment(text):
    return json.loads(urlopen("http://text-processing.com/api/sentiment/",
        data="text=%s" % text).read())

def allSentiments(results):   
    allTweets = ' '.join(results)
    sentVal = 0
    rating = 0
    text = unicodedata.normalize('NFKD', allTweets).encode('ascii','ignore')
    
    sentDict = getSentiment(text)
    sent = sentDict['label']
   
    if sent ==  'pos':
        rating = sentDict['probability']['pos']
        if rating > .75: 
            sentiment = "strongly positive"
        else:
            sentiment = "slightly positive"
        
    elif sent == 'neg':
        rating = sentDict['probability']['neg']   
        if rating > .75:
            sentiment = "strongly negative"
        else:
            sentiment = "slightly negative"
    else:    
        sentiment = "neutral"
     
    return sentVal
 
