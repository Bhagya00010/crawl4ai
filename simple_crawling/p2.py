

import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

async def main():
    browser_config = BrowserConfig()  # Default browser configuration
    run_config = CrawlerRunConfig()   # Default crawl run configuration

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://www.datacamp.com/blog/category/machine-learning",
            config=run_config
        )
       
        # Different content formats
        print(result.html)         # Raw HTML
        print(result.cleaned_html) # Cleaned HTML
        print(result.markdown)     # Markdown version
        print(result.fit_markdown) # Most relevant content in markdown

        # Check success status
        print(result.success)      # True if crawl succeeded
        print(result.status_code)  # HTTP status code (e.g., 200, 404)

        # Access extracted media and links
        print(result.media)        # Dictionary of found media (images, videos, audio)
        print(result.links)        # Dictionary of internal and external links

if __name__ == "__main__":
    asyncio.run(main())
