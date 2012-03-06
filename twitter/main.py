#!/usr/bin/env python

import twitter

def main():
    api = twitter.Api()
    candidates = {"romney":{"firstname":"mitt","mentions":0, "votedfor":0}, "paul":{"firstname":"ron","mentions":0, "votedfor":0}, "gingrich":{"firstname":"newt","mentions":0, "votedfor":0}, "santorum":{"firstname":"rick","mentions":0, "votedfor":0}}
    
    searchterm = "#supertuesday"
    results = []
    
    print "Searching twitter:"
    results = getSearches(api, searchterm, 100)
    
    # Count mentions of each candidate 
    for status in results:
        for candidate in candidates:
            if candidate in status.text.lower():
                candidates[candidate]["mentions"] = candidates[candidate]["mentions"] + 1
    
    # Calculate voted for percentage
    timelen = dict.fromkeys(candidates.keys())
    for candidate in candidates:
        searchterm = "\"i voted for " + candidate + "\" OR \"i voted for " + candidates[candidate]["firstname"] + " " + candidate +"\""
        res = getSearches( api, searchterm, 15)
        timelen[candidate] = max([s.created_at_in_seconds for s in res]) - min([s.created_at_in_seconds for s in res])
    timesum  = 0
    print timelen
    for i in timelen:
        timesum = timesum + timelen[i]
    for candidate in candidates:
        candidates[candidate]["votedfor"] = float(timelen[candidate]) / float(timesum)
    
    print candidates

def getSearches(api, searchterm, num):
    """ Search twitter for num searches using searchterm """
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

    

if __name__ == "__main__":
    main()                
