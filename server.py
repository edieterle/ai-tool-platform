import httpx
import os
import re
from dotenv import load_dotenv
from mcp.server import MCPServer
from pathlib import Path

load_dotenv()
mcp = MCPServer("ai-tool-platform")

ALLOWED_EXTENSIONS = [".txt", ".md", ".json", ".csv", ".py", ".log"]
MAX_FILE_SIZE = 1_000_000  # 1 MB

@mcp.tool()
def health_check() -> dict:
    """Check if the AI tool platform is running."""
    return {"status": "ok"}

@mcp.tool()
def word_count(text: str) -> dict:
    """Count the number of words and the number of characters in text."""
    return {
        "words": len(text.split()),
        "characters": len(text),    
    }

@mcp.tool()
def extract_urls(text: str) -> dict:
    """Extract URLs from text, removing trailing punctuation."""
    pattern = r"https?://[^\s]+"
    matches = re.findall(pattern, text)
    urls = [url.rstrip(".,!?;:)]}") for url in matches]
    return {"urls": urls}

@mcp.tool()
def read_file(path: str) -> dict:
    """Read a supported text file and return its contents."""
    file_path = Path(path).resolve()

    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type.")

    if not file_path.is_file():
        raise ValueError("File not found.")

    if file_path.stat().st_size > MAX_FILE_SIZE:
        raise ValueError("File is too large.")
    
    return {
        "filename": file_path.name,
        "content": file_path.read_text(encoding="utf-8"),
    }

@mcp.tool()
async def web_search(query: str, max_results: int = 5) -> dict:
    """Search the web and return relevant results."""
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if not 1 <= max_results <= 10:
        raise ValueError("max_results must be between 1 and 10.")

    api_key = os.getenv("LANGSEARCH_API_KEY")
    if not api_key:
        raise ValueError("LANGSEARCH_API_KEY is not configured.")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.langsearch.com/v1/web-search",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "query": query,
                "count": max_results,
            },
        )
        response.raise_for_status()
        payload = response.json()

    if str(payload.get("code")) != "200":
        raise RuntimeError(
            f"LangSearch failed: {payload.get('message', 'Unknown error')}"
        )

    pages = payload.get("data", {}).get("webPages", {}).get("value", [])

    return {
        "query": query,
        "results": [
            {
                "title": page.get("name", ""),
                "url": page.get("url", ""),
                "snippet": page.get("snippet", ""),
            }
            for page in pages
        ],
    }

# @mcp.tool()
# def fetch_webpage(url: str) -> dict:

if __name__ == "__main__":
    mcp.run()
    