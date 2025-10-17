# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-18

### Added
- Initial release of AllScrape Backend
- Multi-format content extraction (HTML, Markdown, Text, LLM-ready)
- Cloudflare bypass with fallback mechanisms (httpx → cloudscraper → curl_cffi → Playwright)
- FastAPI-based REST API
- Metadata extraction (title, description, author, date)
- Web search functionality with DuckDuckGo
- Trafilatura integration for high-quality text extraction
- Support for dynamic content via Playwright
- Async/await for high performance
- GPLv3 licensing for open-source distribution

### Features
- `/scrape` endpoint for single URL scraping
- `/search` endpoint for web search with result scraping
- Multiple output formats in a single request
- LLM-optimized content extraction
- Metadata parsing from HTML

### Technical Details
- Built with FastAPI and uvicorn
- BeautifulSoup4 for HTML parsing
- Trafilatura for content extraction
- Playwright for rendering dynamic pages
- curl_cffi for advanced TLS fingerprinting
- cloudscraper for Cloudflare challenge bypass
- httpx for async HTTP requests

## [Unreleased]

### Planned
- Rate limiting improvements
- Advanced domain whitelist/blacklist
- Caching layer
- Metrics and monitoring
- Extended proxy support
- Advanced retry strategies
