# Development Guide

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   └── scraper.py        # Core scraping logic
├── requirements.txt       # Python dependencies
├── README.md             # User documentation
├── CONTRIBUTING.md       # Contribution guidelines
├── SECURITY.md           # Security policy
├── CODE_OF_CONDUCT.md    # Community guidelines
└── LICENSE               # GPLv3 license
```

## Setup for Development

1. Clone the repository:
```bash
git clone https://github.com/EnderGamer6112/allscrape-open.git
cd allscrape-open/backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
python -m playwright install chromium
```

5. Run the development server:
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

6. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key Components

### app/main.py
- FastAPI application setup
- CORS configuration
- API endpoints definition

### app/scraper.py
- Core scraping logic
- Multiple bypass strategies (httpx, cloudscraper, curl_cffi, Playwright)
- Content extraction and formatting

## Core Functions

### fetch_html(url: str) -> str
Fetches HTML content with fallback mechanisms for Cloudflare bypass.

### scrape_url(url: str, formats: List[str]) -> Dict
Main scraping function that returns content in multiple formats.

### search_web(query: str, max_results: int) -> List[Dict]
Performs web search and scrapes results.

## Testing

Before submitting changes, test the code.

## Common Issues

### Module not found error
Ensure you're in the backend directory:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Playwright browser not found
Install Chromium:
```bash
python -m playwright install chromium
```

### Cloudflare bypass fails
The tool attempts multiple bypass methods. Some sites may still require manual intervention or may not be scrapable.

## Performance Considerations

- Playwright-based requests are slower than httpx due to browser overhead
- Use appropriate rate limiting to avoid overwhelming target servers
- Consider caching results when scraping multiple times

## Security Considerations

- Never use this tool to bypass security illegally
- Respect robots.txt and website ToS
- Implement proper rate limiting in production
- Handle scraped data responsibly per privacy regulations

## License

All contributions must be compatible with GPLv3.