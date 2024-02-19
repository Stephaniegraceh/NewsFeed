import feedparser
import re
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

def extract_social_image_url(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', property='og:image')
        if meta_tag and 'content' in meta_tag.attrs:
            return meta_tag.attrs['content']
    except Exception as e:
        print(f"Error fetching social image from {article_url}: {e}")
    return "default_image_url_here"  # Fallback image URL

def fetch_filtered_articles(rss_feeds, keywords):
    filtered_articles = []
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            content = entry.title
            if any(re.search(re.escape(keyword), content, re.IGNORECASE) for keyword in keywords):
                image_url = extract_social_image_url(entry.link)  # Extract social image URL
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'pubDate': entry.get('published', 'No date provided'),
                    'image_url': image_url,  # Include extracted image URL
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
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        .article-tile {
            width: 300px;
            height: auto;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .article-tile a {
            color: white;
            text-decoration: none;
            display: block;
            height: 100%;
        }
        .article-tile img {
            width: 100%;
            height: auto;
            object-fit: cover;
        }
        .overlay {
            background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.7));
            color: white;
            padding: 20px;
            position: relative;
            bottom: 0;
        }
        .overlay .title {
            font-size: 18px;
        }
        .overlay .date {
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>Filtered Article Feed</h1>
"""
    for article in filtered_articles:
        html_content += f"""
    <div class="article-tile">
        <a href="{article['link']}">
            <img src="{article['image_url']}" alt="Article image">
            <div class="overlay">
                <div class="title">{article['title']}</div>
                <div class="date">{article['pubDate']}</div>
            </div>
        </a>
    </div>
"""
    html_content += "</body></html>"
    
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
