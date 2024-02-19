# -*- coding: utf-8 -*-
"""RSS FEED WERA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12IiMkEtdqcd3SK1ZVmanNIdaNDbBDUac
"""

# feed_generator.py

import feedparser
import re
from feedgen.feed import FeedGenerator

def fetch_filtered_articles(rss_feeds, keywords):
    filtered_articles = []
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            if any(re.search(re.escape(keyword), entry.title + ' ' + entry.summary, re.IGNORECASE) for keyword in keywords):
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.summary,
                }
                filtered_articles.append(article)
    return filtered_articles

def generate_rss_feed(filtered_articles):
    fg = FeedGenerator()
    fg.id('https://Stephaniegraceh.github.io/NewsFeed/feed.xml')
    fg.title('NewsFeed')
    fg.link(href='https://Stephaniegraceh.github.io/NewsFeed/feed.xml', rel='alternate')
    fg.description('Filtered Article Feed (WH)')
    for article in filtered_articles:
        fg.add_entry(title=article['title'], link={'href': article['link']}, description=article['summary'])

    fg.rss_file('feed.xml')  # Save the RSS feed to a file

rss_feeds = [
    'https://www.theguardian.com/uk/rss',
    'https://www.gov.uk/search/news-and-communications.atom',
    'https://www.bathecho.co.uk/feed/',
    'https://www.mnrjournal.co.uk/rss',
    'https://www.independent.co.uk/rss',
    'https://www.desmog.com/feed/',
    'https://www.businessgreen.com/feeds/rss',
    'https://www.telegraph.co.uk/rss.xml',
    'https://bylinetimes.com/feed/',
    'https://feeds.bbci.co.uk/news/UK/rss.xml',
    'https://www.economist.com/britain/rss.xml',
    'https://leftfootforward.org/feed/',
    'https://bathnewseum.com/feed/',
    'https://bathvoice.co.uk/feed/',
    'https://feeds.skynews.com/feeds/rss/uk.xml',
    'https://www.reutersagency.com/feed/?best-topics=environment&post_type=best',
    'https://www.standard.co.uk/news/politics/rss',
]

keywords = [
    'climate change', 'harassment', 'dentist', 'train', 'council','bus', 'transport',
    'Wera Hobhouse', 'Lib Dem', 'global warming', 'renewable energy', 'climate',
    'Department for Energy Security and Net Zero', 'Department for Food Environment and Rural affairs',
    'environment', 'community energy', 'Liberal Democrat', 'biodiversity','nuclear',
    'immigration','Rwanda','weather', 'wildfires', 'pre-payment meter', 'Bath',
    'Conservative', 'misogyny','sexual','NHS','Osteoperosis','cycling','Prime Minister',
    'trauma','eating disorder'
]

filtered_articles = fetch_filtered_articles(rss_feeds, keywords)
generate_rss_feed(filtered_articles)
