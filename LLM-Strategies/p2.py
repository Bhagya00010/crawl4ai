# Import required libraries
import os                  # For accessing environment variables
import json               # For JSON handling
import asyncio            # For async operations
from typing import List   # For type hinting
from pydantic import BaseModel, Field  # For data validation
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode  # Core crawler components
from crawl4ai.extraction_strategy import LLMExtractionStrategy  # LLM-based extraction

# Define entity structure for knowledge graph nodes
class Entity(BaseModel):
    name: str          # Name of the entity
    description: str   # Description of the entity

# Define relationship structure for knowledge graph edges
class Relationship(BaseModel):
    entity1: Entity         # Source entity
    entity2: Entity         # Target entity
    description: str        # Description of the relationship
    relation_type: str      # Type of relationship between entities

# Define complete knowledge graph structure
class KnowledgeGraph(BaseModel):
    entities: List[Entity]           # List of all entities
    relationships: List[Relationship] # List of all relationships

async def main():
    # LLM extraction strategy
    llm_strat = LLMExtractionStrategy(
        provider="openai/gpt-4",
        api_token=os.getenv('OPENAI_API_KEY'),
        schema=KnowledgeGraph.schema_json(),
        extraction_type="schema",
        instruction="Extract entities and relationships from the content. Return valid JSON.",
        chunk_token_threshold=1400,
        apply_chunking=True,
        input_format="html",
        extra_args={"temperature": 0.1, "max_tokens": 1500}
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strat,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Example page
        url = "https://www.nbcnews.com/business"
        result = await crawler.arun(url=url, config=crawl_config)

        if result.success:
            with open("kb_result.json", "w", encoding="utf-8") as f:
                f.write(result.extracted_content)
            llm_strat.show_usage()
        else:
            print("Crawl failed:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())