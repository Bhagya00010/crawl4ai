import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    # 1) Browser config: headless, bigger viewport, no proxy
    browser_conf = BrowserConfig(
        headless=True,
        viewport_width=1280,
        viewport_height=720
    )

    # 2) Example extraction strategy for an e-commerce product page
    schema = {
        "name": "Products",
        "baseSelector": ".thumbnail", # Base selector for product cards
        "fields": [
            {"name": "product_name", "selector": ".title", "type": "text"},
            {"name": "price", "selector": ".price", "type": "text"},
            {"name": "description", "selector": ".description", "type": "text"},
            {"name": "image_url", "selector": ".img-responsive", "type": "attribute", "attribute": "src"}
        ]
    }
    extraction = JsonCssExtractionStrategy(schema)

    # 3) Crawler run config: skip cache, use extraction
    run_conf = CrawlerRunConfig(
        extraction_strategy=extraction,
        cache_mode=CacheMode.BYPASS,
        css_selector=".row" # Main products container
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        # 4) Execute the crawl on a test e-commerce site
        result = await crawler.arun(
            url="https://webscraper.io/test-sites/e-commerce/allinone",
            config=run_conf
        )

        if result.success:
            print("Extracted content:", result.extracted_content[:500]) # Print first 500 chars
            print("\nThis example demonstrates:")
            print("- Using JsonCssExtractionStrategy with a schema")
            print("- Extracting structured product data (name, price, description, image)")
            print("- CSS selectors for targeting specific elements")
            print("- Browser configuration for headless crawling")
        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())