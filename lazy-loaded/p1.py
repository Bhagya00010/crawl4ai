# Import required libraries
import asyncio  # For async/await functionality
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig  # Main crawler components
from crawl4ai.async_configs import CacheMode  # For cache control

async def main():
    # Configure crawler settings for handling lazy-loaded content
    config = CrawlerRunConfig(
        # Enable image loading wait - ensures images are fully loaded before proceeding
        wait_for_images=True,

        # Option 1: Configuration for automatic page scrolling
        scan_full_page=True,  # Enables automatic page scanning/scrolling
        scroll_delay=0.5,     # Waits 0.5 seconds between scroll actions to allow content loading
        
        # Disable caching to always get fresh content
        cache_mode=CacheMode.BYPASS,
        
        # Enable verbose logging for debugging
        verbose=True
    )

    # Initialize crawler with headless browser (no GUI)
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Crawl Pexels website (image hosting site)
        result = await crawler.arun("https://www.pexels.com", config=config)

        # Process the results
        if result.success:
            # Extract images from the result
            images = result.media.get("images", [])
            print("Images found:", len(images))
            # Display first 5 images' details
            for i, img in enumerate(images[:5]):
                print(f"[Image {i}] URL: {img['src']}, Score: {img.get('score','N/A')}")
        else:
            print("Error:", result.error_message)

# Standard Python entry point
if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function