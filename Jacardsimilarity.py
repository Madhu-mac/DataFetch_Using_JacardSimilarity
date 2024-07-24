from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_jaccard_similarity(text1, text2):
    # Tokenize the titles into words
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    # Calculate Jaccard similarity
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

# Fetch and print RSS headlines
all_entries = []
for url in rss_urls:
    entries = fetch_rss_feed(url)
    recent_entries = filter_recent_entries(entries)
    all_entries.extend(recent_entries)
    for entry in recent_entries:
        print(entry.title)

# Fetch and print API data
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
