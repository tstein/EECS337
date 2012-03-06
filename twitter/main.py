#!/usr/bin/env python

import twitter

from flask import Flask, request

from webshit import search_form, wordle_applet


app = Flask(__name__)
api = twitter.Api()


@app.route("/")
def mainpage():
    return search_form


@app.route("/query", methods=['POST'])
def search():
    query = request.form['query']
    results = getSearches(query)
    alltext = ""
    for r in results:
        alltext += r.text + " "
    page = ""
    page += "<h1>Search: %s</h1>" % query
    page += wordle_applet.format(text=alltext)
    page += "<br><h1>Sentiment analysis</h1>"
    return page


def main():
    app.run(port=1025, debug=True)


def getSearches(searchterm, num=100):
    """ Search twitter for num searches using searchterm """
    results = []
    pagenum = 1
    per_pagenum = 100
    while num > per_pagenum:
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


if __name__ == "__main__":
    main()

