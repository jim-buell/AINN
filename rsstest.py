import feedparser
rssNames = ["https://www.japantimes.co.jp/feed"]
for item in rssNames:
	rssSources='{}'.format(item)
	rssHeadlines = feedparser.parse(rssSources)

headlineList = []

Headlines = rssHeadlines['entries']
if Headlines:
		for entries in Headlines:
			#b = articles['title'][::-1].index("-")
			if "news" in (entries['title']).lower():
				headlineList.append(f"{entries['title']}.")
			else:
				headlineList.append(f"{entries['title']}.")
print(headlineList)