"""
AllScrape Backend - Core Scraping Module

Provides web scraping functionality with multiple fallback mechanisms
for bypassing anti-bot protections (Cloudflare, etc.) and extracting
content in various formats.

Licensed under GPLv3 - https://www.gnu.org/licenses/gpl-3.0.html
"""

import asyncio
import sys
import httpx
from bs4 import BeautifulSoup
import trafilatura
import re
from typing import List, Dict, Optional
import json
import cloudscraper
from curl_cffi import requests as curl_requests


if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except AttributeError:
        pass

# detect cloudflare challenge
def _is_cloudflare_challenge(html: str) -> bool:
    if not html:
        return False
    lower_html = html.lower()
    challenge_markers = [
        "cdn-cgi/challenge-platform",
        "__cf$cv$params",
        "cf_chl_",
        "cf-browser-verification",
        "cf-chl-bypass"
    ]
    return any(marker in lower_html for marker in challenge_markers)


def _has_empty_root(html: str) -> bool:
    if not html:
        return True
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find('div', id='root')
    if not root:
        return False
    text = root.get_text(strip=True)
    return len(text) < 50


def _needs_additional_bypass(html: str) -> bool:
    if not html:
        return True

    if _has_empty_root(html):
        return True

    if not _is_cloudflare_challenge(html):
        return False

    soup = BeautifulSoup(html, 'lxml')
    text = soup.get_text(" ", strip=True)
    lower_text = text.lower()

    # cloudflare challenge title markers

    challenge_text_markers = [
        "just a moment",
        "checking your browser",
        "managed challenge"
    ]

    if any(marker in lower_text for marker in challenge_text_markers):
        return True

    return len(text) < 200

# 1: try fetch with cloudscraper
async def _fetch_with_cloudscraper(url: str, headers: Dict[str, str]) -> str:
    def _blocking_request() -> str:
        scraper = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "windows",
                "desktop": True
            }
        )
        response = scraper.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text

    return await asyncio.to_thread(_blocking_request)

# 2: try fetch with curl_cffi
async def _fetch_with_curl_cffi(url: str, headers: Dict[str, str]) -> str:
    def _blocking_request() -> str:
        session = curl_requests.Session(impersonate="chrome124")
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text

    return await asyncio.to_thread(_blocking_request)

# 3: try fetch with playwright
async def _fetch_with_playwright(url: str, headers: Dict[str, str]) -> str:
    def _blocking_request() -> str:
        from playwright.sync_api import sync_playwright

        user_agent = headers.get("User-Agent")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox"
                ]
            )
            context = browser.new_context(
                user_agent=user_agent,
                locale="tr-TR",
                viewport={"width": 1365, "height": 768},
                ignore_https_errors=True
            )
            page = context.new_page()
            page.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
            )
            page.goto(url, wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(2000)
            content = page.content()
            context.close()
            browser.close()
            return content

    return await asyncio.to_thread(_blocking_request)

# fetch html content from url
async def fetch_html(url: str) -> str:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    }

    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text

    if _needs_additional_bypass(html_content):
        html_content = await _fetch_with_cloudscraper(url, headers)

    if _needs_additional_bypass(html_content):
        html_content = await _fetch_with_curl_cffi(url, headers)

    if _needs_additional_bypass(html_content):
        html_content = await _fetch_with_playwright(url, headers)

    if _needs_additional_bypass(html_content):
        raise Exception("Cloudflare challenge could not be bypassed")

    return html_content


def clean_text(text: str) -> str:

    if not text:
        return ""

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(r'[^\w\s\.,!?;:\-\(\)\'\"\ğüşıöçĞÜŞİÖÇ]+', '', text)
    return text.strip()


def extract_text_from_soup(soup: BeautifulSoup) -> str:
    # extract clean text content from beautifulsoup object

    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'noscript']):
        tag.decompose()
    
    # try to find main content area
    main_content = (
        soup.find('main') or 
        soup.find('article') or 
        soup.find('div', {'class': re.compile(r'content|main|post|article', re.I)}) or
        soup.find('body')
    )
    
    if main_content:

        text_parts = []
        for tag in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th', 'span', 'div', 'a']):
            text = tag.get_text(strip=True)
            if text and len(text) > 10:  # ignore very short texts
                text_parts.append(text)
        
        return '\n'.join(text_parts)
    
    return soup.get_text(strip=True)


def extract_markdown_from_soup(soup: BeautifulSoup) -> str:

    # remove unwanted tags
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'noscript']):
        tag.decompose()
    
    main_content = (
        soup.find('main') or 
        soup.find('article') or 
        soup.find('div', {'class': re.compile(r'content|main|post|article', re.I)}) or
        soup.find('body')
    )
    
    if not main_content:
        return soup.get_text(strip=True)
    
    markdown_parts = []
    
    for element in main_content.descendants:
        if element.name == 'h1':
            markdown_parts.append(f"\n# {element.get_text(strip=True)}\n")
        elif element.name == 'h2':
            markdown_parts.append(f"\n## {element.get_text(strip=True)}\n")
        elif element.name == 'h3':
            markdown_parts.append(f"\n### {element.get_text(strip=True)}\n")
        elif element.name == 'h4':
            markdown_parts.append(f"\n#### {element.get_text(strip=True)}\n")
        elif element.name == 'p':
            text = element.get_text(strip=True)
            if text:
                markdown_parts.append(f"{text}\n")
        elif element.name == 'a' and element.get('href'):
            text = element.get_text(strip=True)
            href = element.get('href')
            if text and href:
                markdown_parts.append(f"[{text}]({href})")
        elif element.name == 'li':
            text = element.get_text(strip=True)
            if text:
                markdown_parts.append(f"- {text}\n")
        elif element.name == 'img' and element.get('src'):
            alt = element.get('alt', 'image')
            src = element.get('src')
            markdown_parts.append(f"![{alt}]({src})\n")
    
    return '\n'.join(markdown_parts)


def extract_metadata(soup: BeautifulSoup, url: str) -> Dict:
    """Extract page metadata"""
    metadata = {
        "url": url,
        "title": "",
        "description": "",
        "author": "",
        "date": ""
    }
    
    # title
    title_tag = soup.find('title')
    if title_tag:
        metadata["title"] = title_tag.get_text().strip()
    
    # meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        metadata["description"] = meta_desc['content'].strip()
    
    # author
    meta_author = soup.find('meta', attrs={'name': 'author'})
    if meta_author and meta_author.get('content'):
        metadata["author"] = meta_author['content'].strip()
    
    # date
    meta_date = soup.find('meta', attrs={'property': 'article:published_time'})
    if meta_date and meta_date.get('content'):
        metadata["date"] = meta_date['content'].strip()
    
    return metadata


async def scrape_url(url: str, formats: List[str] = ["markdown", "html", "text"]) -> Dict:

    try:
        # Fetch HTML
        html_content = await fetch_html(url)
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Extract metadata
        metadata = extract_metadata(soup, url)
        
        result = {
            "metadata": metadata,
            "content": {}
        }
        
        # Try trafilatura first for high-quality extraction
        trafilatura_text = None
        trafilatura_markdown = None
        
        try:
            extracted = trafilatura.extract(
                html_content,
                include_comments=False,
                include_tables=True,
                include_links=True,
                output_format='json'
            )
            
            if extracted:
                extracted_data = json.loads(extracted)
                trafilatura_text = extracted_data.get('text', '')
                
                # Also get markdown format
                trafilatura_markdown = trafilatura.extract(
                    html_content,
                    include_comments=False,
                    include_tables=True,
                    include_links=True,
                    output_format='txt'
                )
        except Exception as e:
            print(f"Trafilatura extraction failed: {str(e)}")
        
        # Extract using BeautifulSoup as fallback or primary method
        bs_text = extract_text_from_soup(soup.find('body') if soup.find('body') else soup)
        bs_markdown = extract_markdown_from_soup(soup.find('body') if soup.find('body') else soup)
        
        # Use trafilatura if it has substantial content, otherwise use BeautifulSoup
        if "text" in formats:
            if trafilatura_text and len(trafilatura_text.strip()) > 100:
                result["content"]["text"] = clean_text(trafilatura_text)
            else:
                result["content"]["text"] = clean_text(bs_text)
        
        if "markdown" in formats:
            if trafilatura_markdown and len(trafilatura_markdown.strip()) > 100:
                result["content"]["markdown"] = trafilatura_markdown
            else:
                result["content"]["markdown"] = bs_markdown
        
        # html format
        if "html" in formats:
            # Remove script and style tags
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            # Get main content
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            if main_content:
                result["content"]["html"] = str(main_content)
            else:
                result["content"]["html"] = str(soup)
        
        # LLM-ready summary - use the best available text
        llm_text = result["content"].get("text", "")
        
        result["llm_ready"] = {
            "title": metadata["title"],
            "text": llm_text,
            "word_count": len(llm_text.split()) if llm_text else 0,
            "source": url
        }
        
        return result
        
    except Exception as e:
        raise Exception(f"Failed to scrape {url}: {str(e)}")


async def search_web(query: str, max_results: int = 5) -> List[Dict]:
    # search the web and scrape top results
    try:
        search_url = f"https://html.duckduckgo.com/html/?q={query}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                search_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            )
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'lxml')
        results = []
        
        # Find search result links
        for result in soup.find_all('a', class_='result__url', limit=max_results):
            url = result.get('href')
            if url and url.startswith('http'):
                try:
                    # Scrape each result
                    scraped_data = await scrape_url(url, formats=["text", "markdown"])
                    results.append(scraped_data)
                except Exception as e:
                    # Skip failed URLs
                    print(f"Failed to scrape {url}: {str(e)}")
                    continue
        
        return results
        
    except Exception as e:
        raise Exception(f"Search failed: {str(e)}")
