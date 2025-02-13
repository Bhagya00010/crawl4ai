from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LXMLWebScrapingStrategy

async def main():
    config = CrawlerRunConfig(
        scraping_strategy=LXMLWebScrapingStrategy()  # Faster alternative to default BeautifulSoup
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://bhagya-patel-portfolio.vercel.app", 
            config=config
        )