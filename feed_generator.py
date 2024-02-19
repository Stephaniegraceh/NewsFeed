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
            content = entry.title
            pub_date = entry.get('pubDate', 'No date provided')  # Extract pubDate
            if any(re.search(re.escape(keyword), content, re.IGNORECASE) for keyword in keywords):
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'pubDate': pub_date,  # Store pubDate
                }
                filtered_articles.append(article)
    return filtered_articles


def generate_html_feed(filtered_articles):
    html_content = """
    <html>
    <head>
        <title>NewsFeed</title>
        <link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet'>
        <style>
            body {
                font-family: 'Open Sans', sans-serif;
                margin: 40px;
                font-size: 12px;
            }
            article {
                margin-bottom: 20px;
            }
            h1 {
                font-size: 24px;
            }
            h2 {
                font-size: 14px;
            }
            .pubDate {
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <h1>Filtered Article Feed</h1>
    """

    for article in filtered_articles:
        html_content += f"""
        <article>
            <h2><a href='{article['link']}'>{article['title']}</a></h2>
            <p class="pubDate">{article['pubDate']}</p>
        </article>
        """
    
    html_content += "</body></html>"
    
    # Save the HTML content to a file
    with open('index.html', 'w') as html_file:
        html_file.write(html_content)

        
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
    'climate change', 'harassment', 'dentist', 'train', 'council', 'bus', 'transport',
    'Wera Hobhouse', 'Lib Dem', 'global warming', 'renewable energy', 'climate',
    'Department for Energy Security and Net Zero', 'Department for Food Environment and Rural affairs',
    'environment', 'community energy', 'Liberal Democrat', 'biodiversity', 'nuclear',
    'immigration', 'Rwanda', 'weather', 'wildfires', 'pre-payment meter', 'Bath',
    'Conservative', 'misogyny', 'sexual', 'NHS', 'Osteoporosis', 'cycling', 'Prime Minister',
    'trauma', 'eating disorder'
]

filtered_articles = fetch_filtered_articles(rss_feeds, keywords)
generate_html_feed(filtered_articles)
