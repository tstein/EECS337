#!/usr/bin/env python

import twitter
from time import sleep

from flask import Flask, request

from cathy import getSentimentTweets
from sentiment import allSentiments
from webshit import search_form, wordle_applet


app = Flask(__name__)
api = twitter.Api()
candidates = {"romney":{"firstname":"mitt","mentions":0, "votedfor":0}, "ron paul":{"firstname":"ron","mentions":0, "votedfor":0}, "gingrich":{"firstname":"newt","mentions":0, "votedfor":0}, "santorum":{"firstname":"rick","mentions":0, "votedfor":0}}


@app.route("/")
def mainpage():
    zeitgeist = dict()
    clist = candidates.keys()
    for c in clist:
        print("Scrapin' %s" % c)
        (results, alltext, alltagstext) = getTweets(c)
        sentiment = allSentiments([r.text for r in results])
        zeitgeist[c] = (results, alltext, alltagstext, sentiment)

    page = "<html><head></head><body>"
    for c in clist:
        print("Renderin' %s" % c)
        (results, alltext, alltagstext, sentiment) = zeitgeist[c]
        page += "<h1>%s</h1><br>" % c
        page += "Candidate sentiment: %d<br>" % sentiment
        page += getSentimentTweets(api, c)
        page += "<br>"
        page += "<h1>Word cloud:</h1>"
        page += wordle_applet.format(text=alltext)
        page += "<h1>Tag cloud:</h1>"
        page += wordle_applet.format(text=alltagstext)
        page += "<br>"
    page += "</body></html>"
    return page


@app.route("/search")
def search():
    return search_form


@app.route("/query", methods=['POST'])
def searchresults():
    query = request.form['query']
    (results, alltext, alltagstext) = getTweets(query)
    page = ""
    page += "<h1>Search: %s</h1>" % query
    page += "<h1>Word cloud:</h1>"
    page += wordle_applet.format(text=alltext)
    page += "<h1>Tag cloud:</h1>"
    page += wordle_applet.format(text=alltagstext)
    page += "<br><h1>Sentiment analysis</h1>"
    return page


def getTweets(query):
    results = getSearches(query, 100)
    allwords = []
    for r in results:
        words = [w.lower() for w in r.text.split(" ") if validTweetword(w, query.split(" "))]
        allwords.extend(words)
    alltext = ' '.join(allwords)
    alltags = [w for w in allwords if w and w[0] == "#"]
    alltagstext = ' '.join(alltags)
    return (results, alltext, alltagstext)


def validTweetword(word, banned):
    word = word.lower()
    banned = [b.lower() for b in banned]
    if word and word[0] == "@":
        return False
    if word in banned:
        return False
    if word in ['rt']:
        return False
    return True


def main():
    app.run(port=1025, debug=True)


def performAnalysis():
    searchterm = "#supertuesday"
    results = []
    numbody = 100
    print "Searching twitter:"
    results = getSearches(searchterm, numbody)
    
    countMentions(results, candidates)
    countVotedFors(candidates)   
    output = "< table border = \"1\">\n<tr>\n<th>Candidate</th>\n<th>Mentions</th>\n<th>Voting For</th></tr>"
    for c in candidates:
        output = output + "\n<tr>%s</tr><td>%.1f</td><td>%.1f</td></tr>" %(c, 100.0*float(candidates[c]["mentions"])/float(len(results)), 100.0*candidates[c]["votedfor"]) 
    output = output + "</table>"
    return output

def countMentions(results, candidates):
    # Count mentions of each candidate 
    for status in results:
        for candidate in candidates:
            if candidate in status.text.lower():
                candidates[candidate]["mentions"] = candidates[candidate]["mentions"] + 1
    
def countVotedFors(candidates):
    # Calculate voted for percentage
    timelen = dict.fromkeys(candidates.keys())
    for candidate in candidates:
        searchterm = "(\"i voted for " + candidate + "\" OR \"i voted for " + candidates[candidate]["firstname"] + " " + candidate +"\" OR "
        searchterm = searchterm + "\"im voting for " + candidate + "\" OR \"im voting for " + candidates[candidate]["firstname"] + " " + candidate +"\" OR "
        searchterm = searchterm + "\"i\'m voting for " + candidate + "\" OR \"i\'m voting for " + candidates[candidate]["firstname"] + " " + candidate +"\""
        searchterm = searchterm + ")"
        res = getSearches( searchterm, 15)
        timelen[candidate] = max([s.created_at_in_seconds for s in res]) - min([s.created_at_in_seconds for s in res])
    timesum  = 0.0
    print timelen
    for i in timelen:
        timesum = timesum + 1.0/ float(timelen[i])
    for candidate in candidates:
        candidates[candidate]["votedfor"] = 1.0/float(timelen[candidate]) / float(timesum)

def getSearches(searchterm, num=100):
    """ Search twitter for num searches using searchterm """
    while True:
        try:
            results = []
            pagenum = 1
            per_pagenum = 100
            while num > per_pagenum and pagenum <= 14:
                results.extend(api.GetSearch(searchterm ,per_page=per_pagenum, page=pagenum))
                num = num - per_pagenum
                pagenum = pagenum + 1
            results.extend(api.GetSearch(searchterm, per_page=per_pagenum, page=pagenum))
            last = results[-1].id
            for i in range(len(results) - 2, -1, -1):
                if last == results[i].id:
                    del results[i]
                else:
                    last = results[i].id
            return results
        except twitter.TwitterError:
            sleep(.5)
            continue


if __name__ == "__main__":
    main()

