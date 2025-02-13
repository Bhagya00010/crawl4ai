# Import required libraries
import asyncio  # For async/await functionality
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig  # Main crawler components

async def main():
    # Configure crawler to respect robots.txt
    config = CrawlerRunConfig(
        check_robots_txt=True  # Enable robots.txt checking and compliance
    )

    # Initialize crawler and attempt to crawl
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            "https://bhagya-patel-portfolio.vercel.app",
            config=config
        )

        # Check if access was denied by robots.txt
        if not result.success and result.status_code == 403:
            print("Access denied by robots.txt")

# Standard Python entry point
if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function