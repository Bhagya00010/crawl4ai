# While manually crafting schemas is powerful and precise, Crawl4AI now offers a convenient utility to automatically 
# generate extraction schemas using LLM. This is particularly useful when:

# You're dealing with a new website structure and want a quick starting point
# You need to extract complex nested data structures
# You want to avoid the learning curve of CSS/XPath selector syntax
# Using the Schema Generator
# The schema generator is available as a static method on both JsonCssExtractionStrategy and JsonXPathExtractionStrategy. 
# You can choose between OpenAI's GPT-4 or the open-source Ollama for schema generation:

from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, JsonXPathExtractionStrategy

# Sample HTML with product information
html = """
<div class="product-card">
    <h2 class="title">Gaming Laptop</h2>
    <div class="price">$999.99</div>
    <div class="specs">
        <ul>
            <li>16GB RAM</li>
            <li>1TB SSD</li>
        </ul>
    </div>
</div>
"""

# Option 1: Using OpenAI (requires API token)
css_schema = JsonCssExtractionStrategy.generate_schema(
    html,
    schema_type="css",  # This is the default
    llm_provider="openai/gpt-4o",  # Default provider
    api_token="your-openai-token"  # Required for OpenAI
)

# Option 2: Using Ollama (open source, no token needed)
xpath_schema = JsonXPathExtractionStrategy.generate_schema(
    html,
    schema_type="xpath",
    llm_provider="ollama/llama3.3",  # Open source alternative
    api_token=None  # Not needed for Ollama
)

# Use the generated schema for fast, repeated extractions
strategy = JsonCssExtractionStrategy(css_schema)