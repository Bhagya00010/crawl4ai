import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_structured_data_using_css_extractor():
    print("\n--- Using JsonCssExtractionStrategy Example ---")
    
    # Define schema for product information
    schema = {
        "name": "Product Details",
        "baseSelector": ".product-item",
        "fields": [
            {"name": "title", "selector": ".product-title", "type": "text"},
            {"name": "price", "selector": ".product-price", "type": "text"},
            {"name": "description", "selector": ".product-description", "type": "text"},
            {"name": "image", "selector": "img.product-image", "type": "attribute", "attribute": "src"}
        ]
    }

    # Sample HTML content with product information
    sample_html = """
    <div class="product-item">
        <h2 class="product-title">Laptop Pro X</h2>
        <span class="product-price">$999.99</span>
        <p class="product-description">High performance laptop with latest features</p>
        <img class="product-image" src="laptop.jpg" alt="Laptop Pro X">
    </div>
    <div class="product-item">
        <h2 class="product-title">Smartphone Y</h2>
        <span class="product-price">$599.99</span>
        <p class="product-description">Next generation smartphone</p>
        <img class="product-image" src="phone.jpg" alt="Smartphone Y">
    </div>
    """

    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema)
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="raw://" + sample_html,
            config=crawler_config
        )

        try:
            extracted_content = result.extracted_content.strip()
            if not extracted_content:
                print("No data extracted.")
                return
            
            products = json.loads(extracted_content)
            print(f"Successfully extracted {len(products)} products")
            print("\nExtracted Data:")
            print(json.dumps(products, indent=2))

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

async def main():
    await extract_structured_data_using_css_extractor()

if __name__ == "__main__":
    asyncio.run(main())
