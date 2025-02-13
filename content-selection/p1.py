# Import required libraries
import asyncio  # For async/await functionality
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig  # Main crawler components

async def main():
    # Configure crawler to select specific content using CSS selector
    config = CrawlerRunConfig(
        # Select only first 30 items from Hacker News using CSS selector
        css_selector=".athing:nth-child(-n+30)"  # Limits content to first 30 news items
    )

    # Initialize crawler and execute
    async with AsyncWebCrawler() as crawler:
        # Crawl Hacker News newest page with configured selector
        result = await crawler.arun(
            url="https://news.ycombinator.com/newest", 
            config=config
        )
        # Print length of cleaned HTML to verify content selection
        print("Partial HTML length:", len(result.cleaned_html))

# Standard Python entry point
if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function