import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import CrawlerRunConfig

async def crawl_web():
    config = CrawlerRunConfig(bypass_cache=True)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://en.wikipedia.org/wiki/apple", 
            config=config
        )
        if result.success:
            print("Markdown Content:")
            print(result.markdown)
        else:
            print(f"Failed to crawl: {result.error_message}")

asyncio.run(crawl_web())