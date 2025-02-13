import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_main_articles(url: str):
    schema = {
        "name": "ArticleBlock",
        "baseSelector": "div.article-block",
        "fields": [
            {"name": "headline", "selector": "h2", "type": "text"},
            {"name": "summary", "selector": ".summary", "type": "text"},
            {
                "name": "metadata",
                "type": "nested",
                "fields": [
                    {"name": "author", "selector": ".author", "type": "text"},
                    {"name": "date", "selector": ".date", "type": "text"}
                ]
            }
        ]
    }

    config = CrawlerRunConfig(
        # Keep only #main-content
        css_selector="#main-content",

        # Filtering
        word_count_threshold=10,
        excluded_tags=["nav", "footer"],  
        exclude_external_links=True,
        exclude_domains=["somebadsite.com"],
        exclude_external_images=True,

        # Extraction
        extraction_strategy=JsonCssExtractionStrategy(schema),

        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        if not result.success:
            print(f"Error: {result.error_message}")
            return None
        return json.loads(result.extracted_content)

async def main():
    articles = await extract_main_articles("https://news.ycombinator.com/newest")
    if articles:
        print("Extracted Articles:", articles[:20])  # Show first 2

if __name__ == "__main__":
    asyncio.run(main())