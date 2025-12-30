"""
RSS News Aggregator - Complete Standalone Script
Tutorial: How to Build a News Aggregator App with RSS Feeds
Source: https://newsdatahub.com/learning-center/article/building-news-app-with-rss-feeds

This script demonstrates how to fetch, parse, filter, and sort news articles
from multiple RSS feeds using Python.

Requirements:
    pip install feedparser python-dateutil requests

Usage:
    python rss-feeds-tutorial-script.py
"""

import feedparser
from datetime import datetime
from dateutil import parser as date_parser
from typing import List, Dict
import time

# RSS feed sources
RSS_FEEDS = {
    'BBC News': 'http://feeds.bbci.co.uk/news/rss.xml',
    'TechCrunch': 'https://techcrunch.com/feed/',
    'The Guardian': 'https://www.theguardian.com/world/rss',
    'NPR': 'https://feeds.npr.org/1001/rss.xml'
}


def fetch_all_feeds(feed_dict: Dict[str, str]) -> List[Dict]:
    """
    Fetch articles from multiple RSS feeds.

    Args:
        feed_dict (dict): Dictionary mapping source names to RSS URLs

    Returns:
        list: Combined list of articles from all sources
    """
    all_articles = []

    for source_name, feed_url in feed_dict.items():
        print(f"Fetching {source_name}...")

        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                article = {
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', entry.get('description', 'No description')),
                    'published': entry.get('published', entry.get('updated', '')),
                    'source': source_name
                }
                all_articles.append(article)

            print(f"  ✓ Found {len(feed.entries)} articles")

        except Exception as e:
            print(f"  ✗ Error fetching {source_name}: {str(e)}")

        # Be respectful to servers
        time.sleep(0.5)

    return all_articles


def display_articles(articles: List[Dict], limit: int = 10):
    """Display articles in a readable format."""
    print(f"\n{'='*80}")
    print(f"Displaying {min(limit, len(articles))} of {len(articles)} total articles")
    print(f"{'='*80}\n")

    for idx, article in enumerate(articles[:limit], 1):
        print(f"{idx}. [{article['source']}] {article['title']}")
        print(f"   {article['link']}")
        print(f"   Published: {article['published']}")
        print(f"   {article['description'][:150]}...")
        print()


def parse_date(date_string: str) -> datetime:
    """
    Attempt to parse various date formats.

    Args:
        date_string (str): Date string from RSS feed

    Returns:
        datetime: Parsed datetime object, or datetime.min if parsing fails
    """
    try:
        return date_parser.parse(date_string)
    except:
        return datetime.min


def sort_articles_by_date(articles: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Sort articles by publication date.

    Args:
        articles (list): List of article dictionaries
        reverse (bool): Sort descending (newest first) if True

    Returns:
        list: Sorted list of articles
    """
    return sorted(articles, key=lambda x: parse_date(x['published']), reverse=reverse)


def filter_articles(articles: List[Dict], keyword: str) -> List[Dict]:
    """
    Basic keyword filtering.

    Note: This is very limited compared to News APIs which offer
    boolean search, topic filters, country filters, etc.

    Args:
        articles (list): List of article dictionaries
        keyword (str): Keyword to search for in title and description

    Returns:
        list: Filtered list of articles containing the keyword
    """
    keyword_lower = keyword.lower()
    return [
        a for a in articles
        if keyword_lower in a['title'].lower() or keyword_lower in a['description'].lower()
    ]


def main():
    """Main execution function."""
    print("RSS News Aggregator")
    print("=" * 80)
    print()

    # Fetch all articles from RSS feeds
    articles = fetch_all_feeds(RSS_FEEDS)

    # Sort by date (newest first)
    sorted_articles = sort_articles_by_date(articles)

    # Display all articles
    display_articles(sorted_articles, limit=15)

    # Example: Filter for technology news
    tech_news = filter_articles(sorted_articles, 'technology')
    print(f"\n{'='*80}")
    print(f"Filtered for 'technology': {len(tech_news)} articles found")
    print(f"{'='*80}")
    display_articles(tech_news, limit=10)

    # Example: Filter for AI-related news
    ai_news = filter_articles(sorted_articles, 'artificial intelligence')
    print(f"\n{'='*80}")
    print(f"Filtered for 'artificial intelligence': {len(ai_news)} articles found")
    print(f"{'='*80}")
    display_articles(ai_news, limit=5)


if __name__ == '__main__':
    main()
