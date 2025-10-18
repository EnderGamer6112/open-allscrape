# AllScrape

**AllScrape**, açık kaynak bir web scraper’dır.
GPLv3 lisansı ile yayınlanmıştır.

PyPI: [pypi.org/project/allscrape/](https://pypi.org/project/allscrape/)

## Kurulum

```bash
pip install allscrape
```

## Örnek Kullanım

```python
import allscrape
    
# Scrape with default settings
result = allscrape.scrape("https://example.com")
    
# Scrape with Cloudflare bypass
result = allscrape.scrape("https://example.com", cfbypass=True)
    
# Get specific content formats
result = allscrape.scrape("https://example.com", formats=["text", "markdown"])
    
# Async scraping
import asyncio
result = asyncio.run(allscrape.scrape_async("https://example.com"))
```
