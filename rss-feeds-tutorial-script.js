const Parser = require('rss-parser');
const parser = new Parser({
  timeout: 10000,
  headers: {'User-Agent': 'rss-parser'}
});

const RSS_FEEDS = {
  'BBC News': 'http://feeds.bbci.co.uk/news/rss.xml',
  'TechCrunch': 'https://techcrunch.com/feed/',
  'The Guardian': 'https://www.theguardian.com/world/rss',
  'NPR': 'https://feeds.npr.org/1001/rss.xml',
  'Wired': 'https://www.wired.com/feed/rss'
};

async function fetchAllFeeds(feedsObject) {
  /**
   * Fetch articles from multiple RSS feeds concurrently
   * @param {Object} feedsObject - Object mapping source names to feed URLs
   * @returns {Array} Combined array of all articles
   */
  const feedPromises = Object.entries(feedsObject).map(async ([sourceName, feedUrl]) => {
    console.log(`Fetching ${sourceName}...`);

    try {
      const feed = await parser.parseURL(feedUrl);
      const articles = feed.items.map(item => ({
        title: item.title || 'No title',
        link: item.link || '',
        description: item.contentSnippet || item.description || 'No description',
        published: item.pubDate || item.isoDate || '',
        source: sourceName,
        categories: item.categories || []
      }));

      console.log(`  ✓ Found ${articles.length} articles from ${sourceName}`);
      return articles;

    } catch (error) {
      console.error(`  ✗ Error fetching ${sourceName}:`, error.message);
      return [];
    }
  });

  const resultsArray = await Promise.all(feedPromises);
  return resultsArray.flat();
}

function displayArticles(articles, limit = 10) {
  /**
   * Display articles in readable format
   */
  console.log('\n' + '='.repeat(80));
  console.log(`Displaying ${Math.min(limit, articles.length)} of ${articles.length} total articles`);
  console.log('='.repeat(80) + '\n');

  articles.slice(0, limit).forEach((article, idx) => {
    console.log(`${idx + 1}. [${article.source}] ${article.title}`);
    console.log(`   ${article.link}`);
    console.log(`   Published: ${article.published}`);
    console.log(`   ${article.description.substring(0, 150)}...`);
    console.log();
  });
}

function sortByDate(articles, descending = true) {
  /**
   * Sort articles by publication date
   */
  return articles.sort((a, b) => {
    const dateA = new Date(a.published);
    const dateB = new Date(b.published);
    return descending ? dateB - dateA : dateA - dateB;
  });
}

function filterByKeyword(articles, keyword) {
  /**
   * Basic keyword filtering
   * Note: Very limited compared to News API filtering capabilities
   */
  const keywordLower = keyword.toLowerCase();
  return articles.filter(article =>
    article.title.toLowerCase().includes(keywordLower) ||
    article.description.toLowerCase().includes(keywordLower)
  );
}

// Main execution
(async () => {
  try {
    // Fetch all feeds
    const allArticles = await fetchAllFeeds(RSS_FEEDS);

    // Sort by date
    const sortedArticles = sortByDate(allArticles);

    // Display all
    displayArticles(sortedArticles, 15);

    // Example: Filter for artificial intelligence related news
    const aiNews = filterByKeyword(sortedArticles, 'artificial intelligence');
    console.log(`\nFiltered for "artificial intelligence": ${aiNews.length} articles found`);
    displayArticles(aiNews, 5);

    // Exit explicitly since rss-parser keeps event loop alive
    setTimeout(() => process.exit(0), 100);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
})();
