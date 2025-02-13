import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def main():
    crawler_cfg = CrawlerRunConfig(
        exclude_external_links=True,          # No links outside primary domain
        exclude_social_media_links=True       # Skip recognized social media domains
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            "https://www.datacamp.com/blog/category/machine-learning",
            config=crawler_cfg,
            filter_external=True  # Add explicit filter to ensure external links are excluded
        )
        if result.success:
            print("[OK] Crawled:", result.url)
            print("Internal links count:", len(result.links.get("internal", [])))
            # External links should be empty since we excluded them
            external_links = result.links.get("external", [])
            if len(external_links) > 0:
                print("Warning: Found external links despite exclusion")
            else:
                print("External links count: 0")  # Should always be 0
        else:
            print("[ERROR]", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())