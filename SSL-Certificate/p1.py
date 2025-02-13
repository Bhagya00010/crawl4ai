# Import required libraries
import asyncio  # For async/await functionality
import os  # For file/directory operations
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode  # Main crawler components

async def main():
    # Create temporary directory for storing certificates
    tmp_dir = "tmp"
    os.makedirs(tmp_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Configure crawler to fetch SSL certificates
    config = CrawlerRunConfig(
        fetch_ssl_certificate=True,  # Enable SSL certificate fetching
        cache_mode=CacheMode.BYPASS  # Disable caching
    )

    # Initialize crawler and fetch certificate
    async with AsyncWebCrawler() as crawler:
        # Crawl website and get SSL certificate
        result = await crawler.arun("https://www.apnacollege.in", config=config)
        
        # Process certificate if available
        if result.success and result.ssl_certificate:
            cert = result.ssl_certificate
            
            # 1. Print basic certificate information
            print("Issuer CN:", cert.issuer.get("CN", ""))  # Certificate issuer
            print("Valid until:", cert.valid_until)         # Expiration date
            print("Fingerprint:", cert.fingerprint)         # Certificate fingerprint

            # 2. Export certificate in different formats
            cert.to_json(os.path.join(tmp_dir, "certificate.json"))  # JSON format
            cert.to_pem(os.path.join(tmp_dir, "certificate.pem"))   # PEM format
            cert.to_der(os.path.join(tmp_dir, "certificate.der"))   # DER format

# Standard Python entry point
if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function