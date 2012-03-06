#!/usr/bin/env python

import twitter

def main():
    api = twitter.Api()
    candidates = [("romney", 0), ("paul",0), ("gingrich",0), ("santorum",0)]
    searchterm = "#supertuesday"
    print "Searching twitter:\n"
    results = api.GetSearch(searchterm,per_page=100)
    
    for status in results:
        for i in range(len(candidates)):
            if candidates[i][0] in status.text.lower():
                candidates[i] = (candidates[i][0], candidates[i][1] +1)
    print candidates









    # dictionary for states
    states = {"Alaska":"(#alaska OR #alaskaprimary OR #alaska2012 OR #akprimary OR #ak2012)",
              "Georgia":"(#georgia OR #georgiaprimary OR #georgia2012 OR #gaprimary OR #ga2012)",
              "Idaho":"(#idaho OR #idahoprimary OR #idaho2012 OR #idprimary OR #id2012)",
              "Massachusetts":"(#massachusetts OR #massachusettsprimary OR #massachusetts2012 OR #maprimary OR #ma2012)",
              "North Dakota":"(#northdakota OR #northdakotaprimary OR #northdakota2012 OR #ndprimary OR #nd2012)",
              "Ohio":"(#ohio OR #ohioprimary OR #ohio2012 OR #ohprimary OR #oh2012)",
              "Oklahoma":"(#oklahoma OR #oklahomaprimary OR #oklahoma2012 OR #okprimary OR #ok2012)",
              "Tennessee":"(#tennessee OR #tennesseeprimary OR #tennessee2012 OR #tnprimary OR #tn2012)",
              "Vermont":"(#vermont OR #vermontprimary OR #vermont2012 OR #vtprimary OR #vt2012)",
              "Virginia":"(#virginia OR #virginiaprimary OR #virginia2012 OR #vaprimary OR #va2012)",
              "Wyoming":"(#wyoming OR #wyomingprimary OR #wyoming2012 OR #wyprimary OR #wy2012)"}


             











    # searching for positive sentiment
    happySearchTerm = searchterm+" :)"
    happyResults = api.GetSearch(happySearchTerm)
    
    print "POSITIVE TWEETS ABOUT ", searchterm
    for status in happyResults:
        print status.text
        print "\n"



    # searching for negative sentiment
    madSearchTerm = searchterm+" :("
    madResults = api.GetSearch(madSearchTerm)

    print "NEGATIVE TWEETS ABOUT ", searchterm
    for status in madResults:
        print status.text
        print "\n"



    # searching for questions
    qSearchTerm = searchterm+" ?"
    qResults = api.GetSearch(qSearchTerm)
 
    print "QUESTIONS ABOUT ", searchterm
    for status in qResults:
        print status.text
        print "\n"


    # searching for surprise ("omg" "wow" "whoa" "can't believe")
    wowSearchTerm = searchterm+" (\"omg\" OR \"wow\" OR \"whoa\" OR \"can't believe\" OR \"cannot believe\")"
    wowResults = api.GetSearch(wowSearchTerm)

    print "SURPRISED TWEETS ABOUT ", searchterm
    for status in wowResults:
        print status.text
        print "\n"



if __name__ == "__main__":
    main()                
