import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    # Example schema for extracting product data from an e-commerce site
    schema = {
        "name": "Products", 
        "baseSelector": ".thumbnail",  # Base selector for product cards
        "fields": [
            {
                "name": "product_name",
                "selector": ".title",  # Product title selector
                "type": "text"
            },
            {
                "name": "price",
                "selector": ".price",  # Price selector 
                "type": "text"
            },
            {
                "name": "description",
                "selector": ".description", # Description selector
                "type": "text"
            },
            {
                "name": "image_url",
                "selector": ".img-responsive", # Product image selector
                "type": "attribute",
                "attribute": "src"
            }
        ]
    }

    config = CrawlerRunConfig(
        # Content filtering
        excluded_tags=["nav", "footer"],
        
        # CSS selection for products container
        css_selector=".row",  # Main products grid container
        
        # No caching
        cache_mode=CacheMode.BYPASS,
        
        # Use our extraction strategy
        extraction_strategy=JsonCssExtractionStrategy(schema)
    )

    async with AsyncWebCrawler() as crawler:
        # Crawl the test e-commerce site
        result = await crawler.arun(
            url="https://webscraper.io/test-sites/e-commerce/allinone", 
            config=config
        )
        
        # Parse and print extracted data
        try:
            data = json.loads(result.extracted_content)
            print(f"Found {len(data)} products")
            if data:
                print("\nFirst product details:")
                print(json.dumps(data[0], indent=2))
                print("\nExample fields extracted:")
                print("- Product name:", data[0].get("product_name"))
                print("- Price:", data[0].get("price"))
                print("- Description:", data[0].get("description"))
                print("- Image URL:", data[0].get("image_url"))
        except json.JSONDecodeError:
            print("Failed to parse JSON data")
        except Exception as e:
            print(f"Error processing data: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())