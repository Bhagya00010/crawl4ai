from crawl4ai.extraction_strategy import CosineStrategy
import json
from typing import Dict, List, Any

# Initialize the base CosineStrategy with optimal parameters for general content extraction
strategy = CosineStrategy(
    semantic_filter="mixed content",          # Filter for any relevant content type
    word_count_threshold=20,                  # Minimum words to consider meaningful content
    sim_threshold=0.5,                        # Balanced similarity threshold
    max_dist=0.3,                            # Allow moderately sized clusters
    linkage_method='ward',                    # Default clustering method for balanced results
    top_k=5,                                 # Get top 5 most relevant clusters
    model_name='sentence-transformers/all-MiniLM-L6-v2',  # Fast and accurate embedding model
    verbose=True                             # Enable logging for monitoring
)

async def extract_content(url: str, content_type: str = None) -> Dict[str, Any]:
    """
    Extract and analyze content from a URL with customized parameters based on content type
    
    Args:
        url: Target webpage URL
        content_type: Type of content to extract (e.g. "reviews", "articles", "technical")
    
    Returns:
        Dictionary containing extracted content and analysis metrics
    """
    
    # Customize strategy based on content type
    if content_type == "reviews":
        strategy.semantic_filter = "customer reviews and ratings"
        strategy.word_count_threshold = 15    # Reviews can be shorter
        strategy.sim_threshold = 0.4          # Allow variety in review content
        strategy.top_k = 10                   # Get multiple reviews
        
    elif content_type == "articles":
        strategy.semantic_filter = "main article content" 
        strategy.word_count_threshold = 100   # Articles typically longer
        strategy.sim_threshold = 0.6          # Stricter matching for article content
        strategy.top_k = 1                    # Usually want single main content
        
    elif content_type == "technical":
        strategy.semantic_filter = "technical specifications"
        strategy.word_count_threshold = 30
        strategy.sim_threshold = 0.7          # Very strict matching for technical content
        strategy.max_dist = 0.2               # Tighter clusters
        
    try:
        # Initialize crawler and extract content
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
                extraction_strategy=strategy
            )
            
            if result.success:
                content = json.loads(result.extracted_content)
                
                # Return extracted content with metrics
                return {
                    'content': content,
                    'num_clusters': len(content),
                    'similarity_scores': [item['score'] for item in content],
                    'content_type': content_type or 'general',
                    'success': True
                }
            else:
                return {
                    'error': result.error_message,
                    'success': False
                }
                
    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }

# Example usage and expected output:
"""
result = await extract_content(
    url="https://example.com/reviews",
    content_type="reviews"
)

Expected output:
{
    'content': [
        {
            'text': 'Great product, highly recommend...',
            'score': 0.85,
            'cluster_id': 1
        },
        ...
    ],
    'num_clusters': 10,
    'similarity_scores': [0.85, 0.82, 0.78, ...],
    'content_type': 'reviews',
    'success': True
}
"""