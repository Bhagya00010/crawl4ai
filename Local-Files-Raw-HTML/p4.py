import os
import sys
import asyncio
from pathlib import Path
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import CrawlerRunConfig

async def main():
    wikipedia_url = "https://en.wikipedia.org/wiki/apple"
    script_dir = Path(__file__).parent
    html_file_path = script_dir / "apple.html"

    async with AsyncWebCrawler() as crawler:
        # Step 1: Crawl the Web URL
        print("\n=== Step 1: Crawling the Wikipedia URL ===")
        web_config = CrawlerRunConfig(bypass_cache=True)
        result = await crawler.arun(url=wikipedia_url, config=web_config)

        if not result.success:
            print(f"Failed to crawl {wikipedia_url}: {result.error_message}")
            return

        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(result.html)
        web_crawl_length = len(result.markdown)
        print(f"Length of markdown from web crawl: {web_crawl_length}\n")

        # Step 2: Crawl from the Local HTML File
        print("=== Step 2: Crawling from the Local HTML File ===")
        file_url = f"file://{html_file_path.resolve()}"
        file_config = CrawlerRunConfig(bypass_cache=True)
        local_result = await crawler.arun(url=file_url, config=file_config)

        if not local_result.success:
            print(f"Failed to crawl local file {file_url}: {local_result.error_message}")
            return

        local_crawl_length = len(local_result.markdown)
        assert web_crawl_length == local_crawl_length, "Markdown length mismatch"
        print("✅ Markdown length matches between web and local file crawl.\n")

        # Step 3: Crawl Using Raw HTML Content
        print("=== Step 3: Crawling Using Raw HTML Content ===")
        with open(html_file_path, 'r', encoding='utf-8') as f:
            raw_html_content = f.read()
        raw_html_url = f"raw:{raw_html_content}"
        raw_config = CrawlerRunConfig(bypass_cache=True)
        raw_result = await crawler.arun(url=raw_html_url, config=raw_config)

        if not raw_result.success:
            print(f"Failed to crawl raw HTML content: {raw_result.error_message}")
            return

        raw_crawl_length = len(raw_result.markdown)
        assert web_crawl_length == raw_crawl_length, "Markdown length mismatch"
        print("✅ Markdown length matches between web and raw HTML crawl.\n")

        print("All tests passed successfully!")
    if html_file_path.exists():
        os.remove(html_file_path)

if __name__ == "__main__":
    asyncio.run(main())