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
happySearchTerm = query+" :)"
happyResults = api.GetSearch(happySearchTerm)

print "POSITIVE TWEETS ABOUT ", query
for status in happyResults:
    print status.text
    print "\n"



# searching for negative sentiment
madSearchTerm = query+" :("
madResults = api.GetSearch(madSearchTerm)

print "NEGATIVE TWEETS ABOUT ", query
for status in madResults:
    print status.text
    print "\n"



# searching for questions
qSearchTerm = query+" ?"
qResults = api.GetSearch(qSearchTerm)

print "QUESTIONS ABOUT ", query
for status in qResults:
    print status.text
    print "\n"


# searching for surprise ("omg" "wow" "whoa" "can't believe")
wowSearchTerm = query+" (omg OR wow OR whoa OR \"can't believe\" OR \"cannot believe\")"
wowResults = api.GetSearch(wowSearchTerm)

print "SURPRISED TWEETS ABOUT ", query
for status in wowResults:
    print status.text
    print "\n"


# searching for links shared
linkSearchTerm = query+" http"
linkResults = api.GetSearch(linkSearchTerm)

print "LINKS SHARED ABOUT ", query
for status in linkResults:
    print status.text
    print "\n"
    
