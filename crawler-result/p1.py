from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

config = CrawlerRunConfig(
    markdown_generator=DefaultMarkdownGenerator(
        options={"citations": True, "body_width": 80}  # e.g. pass html2text style options
    )
)
result = await crawler.arun(url="https://example.com", config=config)

md_res = result.markdown_v2  # or eventually 'result.markdown'
print(md_res.raw_markdown[:500])
print(md_res.markdown_with_citations)
print(md_res.references_markdown)