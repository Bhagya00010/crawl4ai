# Import required libraries
import asyncio  # For async/await functionality
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode  # Main crawler components
from typing import List  # For type hints

async def crawl_multiple_urls(urls: List[str]):
    # Configure crawler settings for multiple URL crawling
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,  # Disable caching for fresh results
        stream=True,  # Enable streaming mode for parallel processing
        verbose=True  # Enable detailed logging
    )

    # Initialize crawler with configuration
    async with AsyncWebCrawler() as crawler:
        # Stream results as they complete (parallel processing)
        async for result in await crawler.arun_many(urls, config=config):
            if result.success:
                # Process successful crawls
                print(f"[SUCCESS] {result.url}")
                print(f"- Content length: {len(result.markdown)}")
                print(f"- Links found: {len(result.links.get('internal', []))}")
            else:
                # Handle failed crawls
                print(f"[ERROR] {result.url} => {result.error_message}")

async def main():
    # List of URLs to crawl
    urls = [
        "https://www.example.com",
        "https://www.python.org",
        "https://www.github.com"
    ]

    # Execute parallel crawling
    print(f"Starting crawl of {len(urls)} URLs...")
    await crawl_multiple_urls(urls)
    print("Crawling complete!")

# Standard Python entry point
if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function
