import twitter
from time import sleep


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





def getSentimentTweets(api, query):
    while True:
        try:
            table = "<table border=\"1\">"

            # searching for positive sentiment
            happySearchTerm = query+" :)"
            happyResults = api.GetSearch(happySearchTerm)

            table += "<td>POSITIVE TWEETS</td>"
            table += "<td>"
            table += "<ul>"
            table += "<br>".join(list({"<li>" + r.text + "</li>" for r in happyResults}))
            table += "</ul>"
            table += "</td><tr>"


            # searching for negative sentiment
            madSearchTerm = query+" :("
            madResults = api.GetSearch(madSearchTerm)

            table += "<td>NEGATIVE TWEETS</td>"
            table += "<td>"
            table += "<ul>"
            table += "<br>".join(list({"<li>" + r.text + "</li>" for r in madResults}))
            table += "</ul>"
            table += "</td><tr>"



            # searching for questions
            qSearchTerm = query+" ?"
            qResults = api.GetSearch(qSearchTerm)

            table += "<td>INQUISITIVE TWEETS</td>"
            table += "<td>"
            table += "<ul>"
            table += "<br>".join(list({"<li>" + r.text + "</li>" for r in qResults}))
            table += "</ul>"
            table += "</td><tr>"


            # searching for surprise ("omg" "wow" "whoa" "can't believe")
            wowSearchTerm = query+" (omg OR wow OR whoa OR \"can't believe\" OR \"cannot believe\")"
            wowResults = api.GetSearch(wowSearchTerm)

            table += "<td>SHOCKED TWEETS</td>"
            table += "<td>"
            table += "<ul>"
            table += "<br>".join(list({"<li>" + r.text + "</li>" for r in wowResults}))
            table += "</ul>"
            table += "</td><tr>"


            # searching for links shared
            linkSearchTerm = query+" filter:links"
            linkResults = api.GetSearch(linkSearchTerm)


            table += "<td>LINKFUL TWEETS</td>"
            table += "<td>"
            table += "<ul>"
            table += "<br>".join(list({"<li>"+r.text+"</li>" for r in linkResults}))
            table += "</ul>"
            table += "</td><tr>"

            # searching for info about lines
            lineSearchTerm = "(\"long line\" OR \"short line\" OR \"no line\" OR \"no lines\" OR \"short lines\" OR \"long lines\") (poll OR polls OR polling OR voting OR vote OR voters OR #gop2012 OR #supertuesday)"
            lineResults = api.GetSearch(lineSearchTerm)

            table += "<td>TWEETS ABOUT LINES</td>"
            table += "<td>"
            table += "<ul>"
            table += "<br>".join(list({"<li>"+r.text+"</li>" for r in lineResults}))
            table += "</ul>"
            table += "</td><tr>"

            table += "</table>"

            return table
        except twitter.TwitterError:
            sleep(.5)
            continue

