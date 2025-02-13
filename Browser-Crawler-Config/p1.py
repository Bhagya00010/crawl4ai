import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

crawl_conf = CrawlerRunConfig(
    js_code="document.querySelector('button#loadMore')?.click()",
    wait_for=None,  # Remove wait_for since the selector doesn't exist
    screenshot=True,
    page_timeout=10000  # Reduce timeout to fail faster
)

async def main():
    async with AsyncWebCrawler() as crawler:
        try:
            result = await crawler.arun(url="https://crawl4ai.com", config=crawl_conf)
            if result and result.screenshot:
                print(result.screenshot[:500])  # Base64-encoded PNG snippet
            else:
                print("No screenshot captured")
        except Exception as e:
            print(f"Error during crawling: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())