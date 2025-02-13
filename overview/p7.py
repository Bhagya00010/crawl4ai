# Import required libraries
import os  # For file operations
import asyncio  # For async/await functionality
from base64 import b64decode  # For decoding base64 data
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode  # Main components

async def main():
    # 1. Configure browser with proxy and headless mode
    browser_cfg = BrowserConfig(
        proxy_config={
            "server": "http://proxy.example.com:8080",
            "username": "myuser",
            "password": "mypass",
        },
        headless=True,  # Run browser without GUI
    )

    # 2. Configure crawler with various features
    crawler_cfg = CrawlerRunConfig(
        pdf=True,  # Enable PDF capture
        screenshot=True,  # Enable screenshot capture
        fetch_ssl_certificate=True,  # Get SSL certificate
        cache_mode=CacheMode.BYPASS,  # Disable caching
        storage_state="my_storage.json",  # Use saved session data
        verbose=True,  # Enable detailed logging
    )

    # 3. Initialize crawler and execute
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # Attempt to crawl protected page
        result = await crawler.arun(
            url="https://secure.example.com/protected", 
            config=crawler_cfg
        )

        # Process results
        if result.success:
            print("[OK] Crawled the secure page. Links found:", len(result.links.get("internal", [])))

            # Save PDF if available
            if result.pdf:
                with open("result.pdf", "wb") as f:
                    f.write(b64decode(result.pdf))
                    
            # Save screenshot if available
            if result.screenshot:
                with open("result.png", "wb") as f:
                    f.write(b64decode(result.screenshot))

            # Process SSL certificate
            if result.ssl_certificate:
                print("SSL Issuer CN:", result.ssl_certificate.issuer.get("CN", ""))
        else:
            print("[ERROR]", result.error_message)

# Standard Python entry point
if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function
