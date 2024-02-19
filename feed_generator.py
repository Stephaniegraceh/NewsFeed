import feedparser
import re
import requests
from bs4 import BeautifulSoup

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
            margin: 0;
            padding: 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 25px;
        }
        a {
            text-decoration: none; /* Removes the underline from links */
        }
        .article-tile, .team-wera-tile {
            position: relative;
            width: 300px; /* Adjusted width of tile for 4 per row */
            height: 168px; /* Adjusted height to maintain aspect ratio */
            border-radius: 8px; /* Rounded corners */
            overflow: hidden; /* Ensures content is contained within corners */
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Drop shadow */
        }
        .article-tile img, .team-wera-tile img {
            width: 100%;
            height: 100%;
            object-fit: cover; /* Ensures image covers tile */
            border-radius: 8px; /* Rounded corners */
        }
        .overlay {
            position: absolute;
            bottom: 0;
            background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.7)); /* Gradient overlay */
            color: white;
            width: 100%;
            padding: 10px; /* Adjusted padding */
            box-sizing: border-box;
            border-radius: 0 0 8px 8px; /* Rounded corners for the bottom */
        }
        .overlay .title {
            font-size: 10px; /* Adjusted title font size */
            margin: 0;
            text-shadow: 0px 1px 3px rgba(0, 0, 0, 0.5); /* Text shadow */
        }
        .overlay .date {
            font-size: 10px; /* Adjusted date font size */
            margin: 0;
        }
    </style>
</head>
<body>
"""
    # Add the 'Team Wera' tile
    html_content += f"""
    <div class="team-wera-tile">
        <img src="team_wera.png" alt="Team Wera">
    </div>
"""
    for article in filtered_articles:
        # Wrap the tile with an <a> tag to make it a hyperlink
        html_content += f"""
    <a href="{article['link']}" target="_blank">
        <div class="article-tile">
            <img src="{article['image_url']}" alt="Article image">
            <div class="overlay">
                <h2 class="title">{article['title']}</h2>
                <p class="date">{article['pubDate']}</p>
            </div>
        </div>
    </a>
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
    'immigration', 'Rwanda', 'wildfires', 'pre-payment meter', 'Bath',
    'Conservative', 'misogyny', 'sexual', 'NHS', 'Osteoporosis', 'cycling', 'Prime Minister',
    'trauma', 'eating disorder'
]

filtered_articles = fetch_filtered_articles(rss_feeds, keywords)
generate_html_feed(filtered_articles)
