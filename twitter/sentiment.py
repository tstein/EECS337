import json
from urllib2 import urlopen

def getSentiment(text):
    return json.loads(urlopen("http://text-processing.com/api/sentiment/",
        data="text=%s" % text).read())

