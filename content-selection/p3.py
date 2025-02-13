import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def main():
    config = CrawlerRunConfig(
        process_iframes=True,
        remove_overlay_elements=True
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://bhagya-patel-portfolio.vercel.app", 
            config=config
        )
        print("Iframe-merged length:", len(result.cleaned_html))

if __name__ == "__main__":
    asyncio.run(main())