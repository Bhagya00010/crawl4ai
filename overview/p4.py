import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    # Option 1: Set headers at the crawler strategy level
    crawler1 = AsyncWebCrawler(
        # The underlying strategy can accept headers in its constructor
        crawler_strategy=None  # We'll override below for clarity
    )
    crawler1.crawler_strategy.update_user_agent("MyCustomUA/1.0")
    crawler1.crawler_strategy.set_custom_headers({
        "Accept-Language": "fr-FR,fr;q=0.9"
    })
    result1 = await crawler1.arun("https://bhagya-patel-portfolio.vercel.app")
    print("Example 1 result success:", result1.success)

    # Option 2: Pass headers directly to `arun()`
    crawler2 = AsyncWebCrawler()
    result2 = await crawler2.arun(
        url="https://bhagya-patel-portfolio.vercel.app",
        headers={"Accept-Language": "es-ES,es;q=0.9"}
    )
    print("Example 2 result success:", result2.success)

if __name__ == "__main__":
    asyncio.run(main())