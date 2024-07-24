import requests
import feedparser
from datetime import datetime, timedelta
from dateutil import parser
import pytz

# Function to fetch RSS feed data
def fetch_rss_feed(url):
    response = requests.get(url)
    feed = feedparser.parse(response.content)
    entries = []
    for entry in feed.entries:
        title = entry.title
        published = entry.published
        entries.append({'title': title, 'published': published})
    return entries

# Function to filter recent entries
def filter_recent_entries(entries):
    tz = pytz.UTC  # or any other timezone if needed
    now = datetime.now(tz)
    recent_entries = [entry for entry in entries 
                       if parser.parse(entry['published']).astimezone(tz) > now - timedelta(days=7)]
    return recent_entries

# Function to fetch API data
def fetch_api_data(url):
    response = requests.get(url)
    return response.json()

# Function to filter recent API entries
def filter_recent_api_entries(entries):
    tz = pytz.UTC  # or any other timezone if needed
    recent_entries = [entry for entry in entries 
                       if 'published' in entry and parser.parse(entry['published']).astimezone(tz) > datetime.now(tz) - timedelta(days=7)]
    return recent_entries

# Function to calculate Jaccard similarity between two texts
def calculate_jaccard_similarity(text1, text2):
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

# Calculate overlap scores using Jaccard similarity
def calculate_overlap_scores(entries):
    scores = []
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            score = calculate_jaccard_similarity(entries[i]['title'], entries[j]['title'])
            scores.append((entries[i]['title'], entries[j]['title'], score))
    return scores

# URLs to fetch data from
rss_urls = [
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://feeds.feedburner.com/ndtvnews-india-news"
]

api_url = "https://hindustantimes-1-t3366110.deta.app/top-india-news"

# Fetch and process RSS headlines
all_entries = []
for url in rss_urls:
    entries = fetch_rss_feed(url)
    recent_entries = filter_recent_entries(entries)
    all_entries.extend(recent_entries)
    for entry in recent_entries:
        print(entry['title'])

# Fetch and process API data
api_data = fetch_api_data(api_url)
recent_api_entries = filter_recent_api_entries(api_data)

# Collect all entries for overlap scoring
for item in recent_api_entries:
    if 'title' in item:
        print(item['title'])
        all_entries.append({'title': item['title'], 'published': item.get('published', '')})

# Calculate and print overlap scores using Jaccard similarity
overlap_scores = calculate_overlap_scores(all_entries)
for title1, title2, score in overlap_scores:
    if score > 0:  # You can adjust this threshold based on your needs
        print(f'Overlap score between:\n"{title1}"\nand\n"{title2}"\nis: {score:.2f}')
