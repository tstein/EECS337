import twitter
import sentiment

api = twitter.Api()
results = api.GetSearch("Gingrich")

sentNum = sentiment.allSentiments(results)

print sentNum
