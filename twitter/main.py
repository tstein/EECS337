#!/usr/bin/env python

import twitter

from flask import Flask, request

from webshit import search_form, wordle_applet


app = Flask(__name__)


@app.route("/")
def mainpage():
    return search_form


@app.route("/query", methods=['POST'])
def search():
    query = request.form['query']
    return wordle_applet.format(text=query)


def main():
    app.run(port=1025, debug=True)
    api = twitter.Api()
    candidates = {"romney":0,"paul":0, "gingrich":0, "santorum":0}
    searchterm = "#supertuesday"
    results = []
    
    print "Searching twitter:\n"
    results = getSearches(api, searchterm, 150)
    for status in results:
        for candidate in candidates:
            if candidate in status.text.lower():
                candidates[candidate] = candidates[candidate] + 1
    print candidates


def getSearches(api, searchterm, num):
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

