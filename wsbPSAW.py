#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from psaw import PushshiftAPI
import datetime as dt
import json
from collections import Counter


api = PushshiftAPI()

year = dt.datetime.today().year
month = dt.datetime.today().month
day = dt.datetime.today().day
start_time = int(dt.datetime(year, month, day).timestamp())

submissions = api.search_submissions(after=start_time,
            subreddit='wallstreetbets',
            filter=['url', 'author', 'title', 'subreddit'])

news = []
allCashtags = []

for sub in submissions:
    words = sub.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))

    if len(cashtags) > 0:
        for cashtag in cashtags:
            allCashtags.append(cashtag)
        ref = {
            'cashtag': cashtags,
            'time': dt.datetime.fromtimestamp(sub.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
            'url': sub.url,
            'title': sub.title
        }
        news.append(ref)

cnt = Counter(allCashtags)
cnt = dict(sorted(cnt.items(), reverse=True, key=lambda item: item[1]))

now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(f"WallStreetBets_{now}.json", "a") as file:
    json.dump({"Datetime": now}, file, indent=4)
    json.dump({"Counter": cnt}, file, indent=4)
    json.dump(news, file, indent=4)

