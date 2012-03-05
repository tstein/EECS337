#!/usr/bin/env python

import twitter

def main():
    api = twitter.Api()
    candidates = [("romney", 0), ("paul",0), ("gingrich",0), ("santorum",0)]
    searchterm = "#supertuesday"
    results = []
    
    print "Searching twitter:\n"
    results = getSearches(api, searchterm, 1050)
    for status in results:
        for i in range(len(candidates)):
            if candidates[i][0] in status.text.lower():
                candidates[i] = (candidates[i][0], candidates[i][1] +1)
    print candidates

def getSearches(api, searchterm, num):
    """ Search twitter for num searches using searchterm """
    results = []
    while num > 100:
        results.extend(api.GetSearch(searchterm,per_page=100))
        num = num - 100
    results.extend(api.GetSearch(searchterm,per_page=num))
    return results

    

if __name__ == "__main__":
    main()                
