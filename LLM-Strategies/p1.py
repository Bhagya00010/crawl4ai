# Import required libraries
import os                  # For accessing environment variables
import asyncio            # For handling asynchronous operations
import json              # For JSON parsing and handling
from pydantic import BaseModel, Field  # For data validation and schema definition
from typing import List  # For type hinting
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode  # Core crawler components
from crawl4ai.extraction_strategy import LLMExtractionStrategy  # LLM-based extraction

# Define the data structure for product information
class Product(BaseModel):
    name: str    # Store product name as string
    price: str   # Store price as string to handle various formats

async def main():
    # 1. Define the LLM extraction strategy with specific parameters
    llm_strategy = LLMExtractionStrategy(
        provider="openai/gpt-4o-mini",    # Specify the LLM provider
        api_token=os.getenv('OPENAI_API_KEY'),  # Get API key from environment
        schema=Product.schema_json(),      # Convert Pydantic model to JSON schema
        extraction_type="schema",          # Use schema-based extraction
        instruction="Extract all product objects with 'name' and 'price' from the content.",  # Guide for LLM
        chunk_token_threshold=1000,        # Split text into 1000-token chunks
        overlap_rate=0.0,                  # No overlap between chunks
        apply_chunking=True,               # Enable text chunking
        input_format="markdown",           # Process markdown formatted input
        extra_args={"temperature": 0.0, "max_tokens": 800}  # LLM generation parameters
    )

    # 2. Build the crawler config
    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS
    )

    # 3. Create a browser config if needed
    browser_cfg = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # 4. Let's say we want to crawl a single page
        result = await crawler.arun(
            url="https://example.com/products",
            config=crawl_config
        )

        if result.success:
            # 5. The extracted content is presumably JSON
            data = json.loads(result.extracted_content)
            print("Extracted items:", data)

            # 6. Show usage stats
            llm_strategy.show_usage()  # prints token usage
        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())