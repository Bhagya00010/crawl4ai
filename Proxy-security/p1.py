from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
import asyncio

# List of URLs to scrape
urls = ["https://example.com", "https://example.org", "https://example.net"]

# Function to simulate rotating proxy logic
async def get_next_proxy():
    # This function should return a new proxy configuration each time it is called
    # In real-world scenarios, you can integrate a proxy rotation service or a list of proxies
    proxy_list = [
        {"server": "http://proxy1.example.com:8080"},
        {"server": "socks5://proxy2.example.com:1080"},
        {"server": "http://proxy3.example.com:8080", "username": "user", "password": "pass"}
    ]
    for proxy in proxy_list:
        yield proxy

async def main():
    # Setting up the browser configuration without proxy initially
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig()
    
    # Creating an asynchronous web crawler instance
    async with AsyncWebCrawler(config=browser_config) as crawler:
        proxy_generator = get_next_proxy()
        
        # Iterate through URLs and use different proxies
        for url in urls:
            proxy = await anext(proxy_generator)  # Fetch the next proxy from the generator
            
            # Clone the existing run configuration and update proxy for each request
            current_config = run_config.clone(proxy_config=proxy)
            
            print(f"Fetching {url} using proxy: {proxy}")
            result = await crawler.arun(url=url, config=current_config)  # Run crawler with the new proxy
            print(f"Result for {url}: {result}")  # Print the fetched result

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())