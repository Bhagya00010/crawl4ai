# Import required libraries
import asyncio  # For async/await functionality
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig  # Configuration components
import os  # For file/directory operations
from pathlib import Path  # For cross-platform path handling
from crawl4ai import AsyncWebCrawler  # Main crawler component
import aiohttp  # For downloading files
import aiofiles  # For async file operations

async def download_multiple_files(url: str, download_path: str):
    # Configure browser settings
    config = BrowserConfig(headless=True)
    
    # Initialize crawler
    async with AsyncWebCrawler(config=config) as crawler:
        # Configure the crawl operation with longer wait time and retry
        run_config = CrawlerRunConfig(
            wait_for=30,  # Increased wait time to 30 seconds
            retry_count=3,  # Add retries
            verbose=True   # Enable verbose logging
        )
        
        # Execute the crawl to get download links
        result = await crawler.arun(url=url, config=run_config)
        
        # Find all download links
        download_links = []
        if result.success:
            # Get both internal and external links
            all_links = result.links.get("internal", []) + result.links.get("external", [])
            for link in all_links:
                if link.lower().endswith(('.exe', '.msi', '.zip', '.pdf', '.doc', '.docx')):
                    download_links.append(link)
            
            print(f"Found {len(download_links)} files to download")
        else:
            print(f"Failed to crawl {url}: {result.error_message}")
            return
        
        # Download files using aiohttp with timeout and chunk handling
        timeout = aiohttp.ClientTimeout(total=600)  # 10 minute timeout
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for link in download_links:
                filename = os.path.join(download_path, link.split('/')[-1])
                try:
                    async with session.get(link) as response:
                        if response.status == 200:
                            # Download in chunks to handle large files
                            async with aiofiles.open(filename, 'wb') as f:
                                chunk_size = 1024 * 1024  # 1MB chunks
                                while True:
                                    chunk = await response.content.read(chunk_size)
                                    if not chunk:
                                        break
                                    await f.write(chunk)
                            print(f"Successfully downloaded: {filename}")
                        else:
                            print(f"Failed to download {link}: HTTP {response.status}")
                except Exception as e:
                    print(f"Error downloading {link}: {str(e)}")

# Set up download directory in user's home folder
download_path = os.path.join(Path.home(), ".crawl4ai", "downloads")
os.makedirs(download_path, exist_ok=True)  # Create directory if it doesn't exist

# Run the download function
asyncio.run(download_multiple_files("https://www.python.org/downloads/windows/", download_path))
