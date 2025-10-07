import feedparser
from io import BytesIO
import werkzeug
import requests
from bs4 import BeautifulSoup
from .knowledge_base import add_document
from ..models import RssFeed

def _get_article_text(url):
    """Fetches and extracts the main text content from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        # A simple approach to find the main content
        # This can be improved with more sophisticated extraction logic
        paragraphs = soup.find_all('p')
        article_text = '\n'.join([p.get_text() for p in paragraphs])
        return article_text
    except Exception as e:
        print(f"  - Failed to fetch or parse article content from {url}: {e}")
        return None

def run_aggregation_for_all_users():
    """
    Iterates through all stored RSS feeds and adds new entries to the
    knowledge base for each user.
    """
    print("Running scheduled news aggregation...")
    feeds = RssFeed.query.all()
    for feed in feeds:
        print(f"Aggregating feed for user {feed.user_id}: {feed.url}")
        parsed_feed = feedparser.parse(feed.url)
        for entry in parsed_feed.entries:
            # Try to get full article text, fall back to summary
            content = _get_article_text(entry.link)
            if not content or len(content) < len(entry.summary):
                content = entry.summary

            full_content = f"{entry.title}\n\n{content}"
            
            # Sanitize filename
            filename = "".join(c for c in entry.title if c.isalnum() or c in (' ', '.', '_')).rstrip()
            filename = f"{filename}.txt"

            file_obj = werkzeug.datastructures.FileStorage(
                stream=BytesIO(full_content.encode('utf-8')),
                filename=filename
            )
            
            add_document(feed.user_id, file_obj)
            print(f"  - Added: {entry.title}")
