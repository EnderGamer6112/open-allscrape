from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import uvicorn
from app.scraper import scrape_url, search_web

app = FastAPI(
    title="AllScrape API",
    description="Web scraping & search API - LLM Ready | Licensed under GPLv3",
    version="1.0.0"
)

# cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScrapeRequest(BaseModel):
    url: HttpUrl
    formats: Optional[List[str]] = ["markdown", "html", "text"]


class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5


@app.get("/")
async def root():
    return {
        "message": "AllScrape API - LLM Ready Web Scraping",
        "version": "1.0.0",
        "endpoints": {
            "/scrape": "POST - Scrape a single URL",
            "/search": "POST - Search the web and scrape results",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    # scrape a single url
    try:
        result = await scrape_url(str(request.url), request.formats)
        return {
            "success": True,
            "url": str(request.url),
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search(request: SearchRequest):
    # search the web and scrape results
    try:
        results = await search_web(request.query, request.max_results)
        return {
            "success": True,
            "query": request.query,
            "results_count": len(results),
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# start the server
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
