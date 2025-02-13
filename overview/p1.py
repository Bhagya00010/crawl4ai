import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def main():
    browser_cfg = BrowserConfig(
        proxy_config={
            "server": "http://proxy.example.com:8080",
            "username": "myuser",
            "password": "mypass",
        },
        headless=True
    )
    crawler_cfg = CrawlerRunConfig(
        verbose=True
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url="https://www.whatismyip.com/",
            config=crawler_cfg
        )
        if result.success:
            print("[OK] Page fetched via proxy.")
            print("Page HTML snippet:", result.html[:200])
        else:
            print("[ERROR]", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())