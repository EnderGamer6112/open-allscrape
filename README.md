# AllScrape Backend API

LLM-ready web scraping & search API built with FastAPI.

## Features

- 🔍 Single URL scraping with multiple output formats (HTML, Markdown, Text)
- 🌐 Web search with automatic result scraping
- 🤖 LLM-ready output format
- 📊 Metadata extraction (title, description, author, date)
- ⚡ Fast async processing with httpx
- 🧹 Clean text extraction using trafilatura

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install headless browser for dynamic sites (once)
python -m playwright install chromium
```

## Usage

```bash
# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /scrape
Scrape a single URL

**Request:**
```json
{
  "url": "https://example.com",
  "formats": ["markdown", "html", "text"]
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://example.com",
  "data": {
    "metadata": {
      "title": "Page Title",
      "description": "Page description",
      "author": "Author name",
      "date": "2025-01-01"
    },
    "content": {
      "text": "Clean text content...",
      "markdown": "# Markdown content...",
      "html": "<div>HTML content...</div>"
    },
    "llm_ready": {
      "title": "Page Title",
      "text": "Clean text for LLM...",
      "word_count": 500,
      "source": "https://example.com"
    }
  }
}
```

### POST /search
Search the web and scrape results

**Request:**
```json
{
  "query": "python web scraping",
  "max_results": 5
}
```

**Response:**
```json
{
  "success": true,
  "query": "python web scraping",
  "results_count": 5,
  "data": [...]
}
```

## Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
