import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def quick_parallel_example():
    urls = [
        "https://www.kidspiritonline.com/magazine/ai-and-the-future-of-knowledge/how-can-ai-be-used-ethically/?gad_source=1&gclid=CjwKCAiAh6y9BhBREiwApBLHCx9ByCI2iLQCe9hLaHredHJAqTV5zrHIO4FeeCNSdqf5kp2kq-_qoBoCU_gQAvD_BwE",
        "https://www.codecademy.com/articles/language/javascript",

    ]

    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=True  # Enable streaming mode
    )

    async with AsyncWebCrawler() as crawler:
        # Stream results as they complete
        async for result in await crawler.arun_many(urls, config=run_conf):
            if result.success:
                print(f"[OK] {result.url}, length: {len(result.markdown_v2.raw_markdown)}")
            else:
                print(f"[ERROR] {result.url} => {result.error_message}")

        # Or get all results at once (default behavior)
        run_conf = run_conf.clone(stream=False)
        results = await crawler.arun_many(urls, config=run_conf)
        for res in results:
            if res.success:
                print(res.markdown_v2.raw_markdown)
                print(f"[OK] {res.url}, length: {len(res.markdown_v2.raw_markdown)}")
            else:
                print(f"[ERROR] {res.url} => {res.error_message}")

if __name__ == "__main__":
    asyncio.run(quick_parallel_example())